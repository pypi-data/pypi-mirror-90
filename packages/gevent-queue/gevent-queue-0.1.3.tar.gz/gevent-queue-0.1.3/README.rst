gevent-queue
============

gevent-queue is a lightweight, stateful multi-producer and multi-consumer queue. It was
designed to work inside gevent-based web apps (especially Flask) so that you only need a
single process. If you later wish to scale, you can easily spawn separate worker
processes.

gevent-queue supports Redis to persist enqueued messages.

Installing
----------

Install and update using `pip`_:

.. code-block:: text

    pip install -U gevent-queue


Usage Examples
--------------

Using workers:

.. code-block:: python

    import gevent_queue
    import redis

    r = redis.Redis()
    worker = gevent_queue.Worker(r, "myqueue")

    @worker.job
    def myjob(arg):
        print("foo", arg)

    @worker.schedule("*/2 * * * *")
    def every_2_minutes():
        print("bar")

    myjob.delay("myarg")

    while True:
        worker.step()



Using queues:

.. code-block:: python

    import redis
    import gevent_queue

    r = redis.Redis()
    q = gevent_queue.Queue(r, "myqueue")

    q.put("foo")
    q.put("bar")

    print(q.get())
    q.task_done()

    print(q.get())
    q.task_done()


Using locks:

.. code-block:: python

    import redis
    import time
    import gevent_queue
    import threading

    r = redis.Redis()
    l = gevent_queue.Lock(r, "mylock")

    def do_work():
        with l:
            print("begin")
            time.sleep(1)
            print("end")

    worker1 = threading.Thread(target=do_work)
    worker2 = threading.Thread(target=do_work)

    worker1.start()
    worker2.start()

    worker1.join()
    worker2.join()

Using cron expressions:

.. code-block:: python

    import gevent_queue
    import datetime

    date = datetime.datetime(2021, 1, 23, 11, 54)

    assert gevent_queue.cron_matches("* * * * *", date)
    assert gevent_queue.cron_matches("40-59 * * * *", date)
    assert gevent_queue.cron_matches("* 9-16/2 * * *", date)


    start = datetime.datetime(2021, 1, 23, 11, 54)
    end = datetime.datetime(2021, 1, 28, 0, 0)

    assert gevent_queue.cron_occurs_between("54 11 23 01 6", start, end)


.. _pip: https://pip.pypa.io/en/stable/quickstart/
