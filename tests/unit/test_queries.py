from queries import *


def test_db_empty_is_empty(session):
    assert db_empty(session)


def test_db_empty_is_not_empty(session):
    session.add(Team(name="England"))
    assert not(db_empty(session))


def test_two_best_teams(session_exemplary):
    teams = two_best_teams(session_exemplary)

    assert len(teams) == 2
    assert teams[0].name == "Portugal"
    assert teams[1].name == "South Korea"


