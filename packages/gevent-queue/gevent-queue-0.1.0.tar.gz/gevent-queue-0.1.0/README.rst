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



Usage Example
-------------

.. code-block:: python

    import redis
    import gevent-queue

    r = redis.Redis()
    q = gevent_queue.Queue(r, "myqueue")

    q.put("foo")
    q.put("bar")

    print(q.get())
    q.task_done()

    print(q.get())
    q.task_done()



.. _pip: https://pip.pypa.io/en/stable/quickstart/
