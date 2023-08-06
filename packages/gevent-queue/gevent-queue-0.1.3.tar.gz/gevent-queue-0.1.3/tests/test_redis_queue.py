import gevent_queue


def test_basic(redisdb):
    q = gevent_queue.Queue(redisdb, "myqueue")

    q.put("foo")
    q.put("bar")

    assert q.get() == "foo"
    assert q.get() == "bar"
