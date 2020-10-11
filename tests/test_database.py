from helpers import vaishnadb

"""
    FUNCTIONS TO TEST
"""

db = vaishnadb.VaishnaDB()


def get_ekadasi_by_year(year):
    events = db.get_ekadasi_events(year, fetch_by="year")
    return events


def get_ekadasi_by_month(month):
    events = db.get_ekadasi_events(month, fetch_by="month")
    return events


def get_ekadasi_by_year_and_month(year, month):
    events = db.get_ekadasi_events([year, month], fetch_by="year&month")
    return events


def get_iskcon_by_year(year):
    events = db.get_iskcon_events(year, fetch_by="year")
    return events


def get_iskcon_by_month(month):
    events = db.get_iskcon_events(month, fetch_by="month")
    return events


def get_iskcon_by_year_and_month(year, month):
    events = db.get_iskcon_events([year, month], fetch_by="year&month")
    return events



"""
    TEST FUNCTIONS
"""


def test_ekadasi_by_year():
    events = get_ekadasi_by_year(2020)
    assert type(events) == list
    assert len(events[0]) == 9


def test_ekadasi_by_month():
    events = get_ekadasi_by_month(3)
    assert type(events) == list
    assert len(events[0]) == 9


def test_ekadasi_by_year_and_month():
    events = get_ekadasi_by_year_and_month(2020, 4)
    assert type(events) == list
    assert len(events[0]) == 9


def test_isckon_by_year():
    events = get_iskcon_by_year(2020)
    assert type(events) == list
    assert len(events[0]) == 4


def test_isckon_by_month():
    events = get_iskcon_by_month(3)
    assert type(events) == list
    assert len(events[0]) == 4


def test_isckon_by_year_and_month():
    events = get_iskcon_by_year_and_month(2020, 4)
    assert type(events) == list
    assert len(events[0]) == 4