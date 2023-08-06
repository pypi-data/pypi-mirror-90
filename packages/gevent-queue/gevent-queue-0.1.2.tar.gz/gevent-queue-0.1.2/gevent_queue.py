#!/usr/bin/env python3
import datetime
import pickle
import re
import threading
import time
import uuid

from redis.exceptions import ResponseError


class Queue:
    def __init__(
        self,
        redis,
        name="default",
        prefix="gevent-queue",
        stuck_timeout=5,
        stuck_check_interval=10,
    ):
        self.stream_name = prefix + ":" + name
        self.consumer_group = prefix + ":" + name
        self.redis = redis
        self.stuck_timeout = stuck_timeout * 1000
        self.stuck_check_interval = stuck_check_interval * 1000

        self.threadlocal = threading.local()

        try:
            redis.xgroup_create(self.stream_name, self.consumer_group, mkstream=True)
        except ResponseError as ex:
            if "BUSYGROUP" not in str(ex):
                raise ex

    def get_consumer_name(self):
        if "consumer_name" not in self.threadlocal.__dict__:
            self.threadlocal.consumer_name = str(uuid.uuid4())

        return self.threadlocal.consumer_name

    def get_current_message_id(self):
        if "message_id" not in self.threadlocal.__dict__:
            return None

        return self.threadlocal.message_id

    def set_current_message_id(self, message_id):
        self.threadlocal.message_id = message_id

    def get_last_stuck_checked(self):
        if "last_stuck_checked" not in self.threadlocal.__dict__:
            return 0

        return self.threadlocal.last_stuck_checked

    def set_last_stuck_checked(self, timestamp):
        self.threadlocal.last_stuck_checked = timestamp

    def put(self, data):
        message_content = self.encode_message(data)

        self.redis.xadd(self.stream_name, message_content)

    def encode_message(self, data):
        message_content = {"data": pickle.dumps(data)}

        return message_content

    def decode_message(self, message_content):
        return pickle.loads(message_content[b"data"])

    def get_message(self, timeout=None):
        streams = {}
        streams[self.stream_name] = ">"

        consumer_name = self.get_consumer_name()

        response = self.redis.xreadgroup(
            groupname=self.consumer_group,
            consumername=consumer_name,
            streams=streams,
            count=1,
            block=timeout,
        )

        if len(response) > 1:
            raise RuntimeError("Can't read from multiple streams")

        if len(response) == 0:
            return None

        messages = response[0][1]

        if len(messages) == 0:
            return None

        return messages[0]

    def increment_message_id(self, message_id):
        timestamp, counter = message_id.split(b"-")
        counter = int(counter) + 1
        return timestamp.decode() + "-" + str(counter)

    def get_stuck(self, batch_size=10):
        last_message_id = "-"

        while True:
            unprocessed = self.redis.xpending_range(
                self.stream_name, self.consumer_group, last_message_id, "+", batch_size
            )

            if len(unprocessed) == 0:
                return None

            consumer_name = self.get_consumer_name()

            for entry in unprocessed:
                message_id = entry["message_id"]
                time_since_delivered = entry["time_since_delivered"]
                last_message_id = message_id

                if time_since_delivered < self.stuck_timeout:
                    continue

                messages = self.redis.xclaim(
                    self.stream_name,
                    self.consumer_group,
                    consumer_name,
                    0,
                    [message_id],
                )

                if len(messages) == 0:
                    continue

                return messages[0]

            last_message_id = self.increment_message_id(last_message_id)

    def get(self, block=True, timeout=None):
        self.task_done()

        if block and timeout is None:
            timeout = 0

        start_time = int(time.time() * 1000)

        while True:
            last_stuck_checked = self.get_last_stuck_checked()
            current_time = int(time.time() * 1000)

            message = None
            if current_time - last_stuck_checked > self.stuck_check_interval:
                message = self.get_stuck()

                if message is None:
                    self.set_last_stuck_checked(current_time)

            if message is None:
                get_timeout = None
                if block:
                    stuck_check_timeout = max(
                        0, last_stuck_checked + self.stuck_check_interval - current_time
                    )
                    block_timeout = max(0, start_time + timeout * 1000 - current_time)

                    get_timeout = min(block_timeout, stuck_check_timeout)

                if get_timeout == 0:
                    get_timeout = None
                message = self.get_message(get_timeout)

            if message is not None:
                message_id = message[0]
                message_content = message[1]
                self.set_current_message_id(message_id)
                return self.decode_message(message_content)

                return message

            if not block:
                return None

            if timeout is not None and current_time - start_time > timeout:
                return None

    def task_done(self):
        message_id = self.get_current_message_id()

        if message_id is None:
            return

        self.redis.xack(self.stream_name, self.consumer_group, message_id)
        self.set_current_message_id(None)


class Lock:
    def __init__(
        self, redis, name, prefix="gevent-queue:lock", timeout=30, retry_wait=1
    ):
        self.redis = redis

        self.lock_name = prefix + ":" + name

        self.threadlocal = threading.local()

        safe_release_lua = """
            if redis.call("get",KEYS[1]) == ARGV[1] then
                return redis.call("del",KEYS[1])
            else
                return 0
            end
        """

        self.safe_release = redis.register_script(safe_release_lua)
        self.timeout = timeout
        self.retry_wait = retry_wait

    def get_lock_value(self):
        if "lock_value" not in self.threadlocal.__dict__:
            return None

        return self.threadlocal.lock_value

    def set_lock_value(self, value):
        self.threadlocal.lock_value = value

    def acquire(self, block=True, timeout=None):
        start_time = int(time.time() * 1000)

        while True:
            self.set_lock_value(str(uuid.uuid4()))

            res = self.redis.set(
                self.lock_name,
                self.get_lock_value(),
                nx=True,
                px=int(self.timeout * 1000),
            )

            if res:
                return True

            if not block:
                return False

            current_time = int(time.time() * 1000)
            if timeout is not None and current_time - start_time > timeout * 1000:
                return False

            time.sleep(self.retry_wait)

    def release(self):
        lock_value = self.get_lock_value()

        self.safe_release(keys=[self.lock_name], args=[lock_value])

    def __enter__(self):
        self.acquire()

    def __exit__(self, exc_type, exc_value, traceback):
        self.release()


def cron_part_matches(expr_part, dt_part):
    if "," in expr_part:
        return any([cron_part_matches(e, dt_part) for e in expr_part.split(",")])

    if expr_part == "*":
        return True

    if expr_part.isdigit() and int(expr_part) == dt_part:
        return True

    match = re.match(r"^(\d+)-(\d+)/?(\d+)?$", expr_part)
    if match:
        start, end, step = [int(g or 1) for g in match.groups()]

        if dt_part in range(start, end + 1, step):
            return True

    match = re.match(r"^\*/(\d+)$", expr_part)
    if match:
        step = int(match[1])

        if dt_part % step == 0:
            return True

    return False


def cron_matches(expr, dt):
    expr_parts = [part.strip() for part in expr.split(" ")]
    dt_parts = [dt.minute, dt.hour, dt.day, dt.month, dt.isoweekday() % 7]

    return all([cron_part_matches(e, d) for e, d in zip(expr_parts, dt_parts)])


def cron_occurs_between(expr, start, end=None):
    if end is None:
        end = datetime.now(tz=start.tzinfo)

    while start <= end:
        if cron_matches(expr, start):
            return True
        start += datetime.timedelta(minutes=1)

    return False
