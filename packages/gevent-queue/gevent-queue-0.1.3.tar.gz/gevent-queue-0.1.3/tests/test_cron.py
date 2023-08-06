import datetime

import gevent_queue


def test_cron_part_match():
    matches = gevent_queue.cron_part_matches

    assert matches("*", 14)
    assert matches("*/6", 12)
    assert matches("*/6", 0)
    assert matches("1,2,9", 1)
    assert matches("1,2,9", 2)
    assert matches("1,2,9", 9)
    assert not matches("1,2,9", 3)
    assert not matches("1,2,9", 0)
    assert not matches("1,2,9", 10)
    assert matches("1-5", 3)
    assert matches("1-5", 1)
    assert matches("1-5", 5)
    assert not matches("1-5", 6)
    assert not matches("1-5", 0)
    assert not matches("1-5/2", 0)
    assert matches("1-5/2", 1)
    assert not matches("1-5/2", 2)
    assert matches("1-4/2", 3)
    assert not matches("1-4/2", 4)
    assert not matches("1-4/2", 5)


def test_cron_full_date_match():
    matches = gevent_queue.cron_matches

    date = datetime.datetime(2021, 1, 23, 11, 54)

    assert matches("* * * * *", date)
    assert matches("40-59 * * * *", date)
    assert matches("* 9-16/2 * * *", date)

    assert matches("54 11 23 01 *", date)
    assert matches("54 11 23 01 6", date)
    assert not matches("54 11 23 01 5", date)
    assert not matches("0 11 23 01 6", date)
    assert not matches("54 0 23 01 6", date)
    assert not matches("54 11 0 01 6", date)
    assert not matches("54 11 23 0 6", date)
    assert not matches("54 11 23 01 0", date)
    assert matches("* 11 23 01 6", date)
    assert matches("54 * 23 01 6", date)
    assert matches("54 11 * 01 6", date)
    assert matches("54 11 23 * 6", date)
    assert matches("54 11 23 01 *", date)


def test_cron_occurs_between():
    between = gevent_queue.cron_occurs_between

    start = datetime.datetime(2021, 1, 23, 11, 54)
    end = datetime.datetime(2021, 1, 28, 0, 0)

    assert between("54 11 23 01 6", start, end)
    assert between("54 11 25 01 1", start, end)
    assert between("* * 25 * *", start, end)

    assert not between("54 10 23 01 *", start, end)
    assert not between("54 11 29 01 *", start, end)
    assert not between("* * 30 * *", start, end)
