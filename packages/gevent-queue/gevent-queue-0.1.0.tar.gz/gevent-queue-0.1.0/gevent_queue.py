#!/usr/bin/env python3
import pickle
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
