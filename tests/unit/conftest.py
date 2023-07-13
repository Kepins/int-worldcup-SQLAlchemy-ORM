import os

import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models import Base, Team, Match


@pytest.fixture
def engine():
    load_dotenv()
    user = os.environ['TEST_POSTGRESQL_USER']
    passwd = os.environ['TEST_POSTGRESQL_PASSWD']
    hostname = os.environ['TEST_POSTGRESQL_HOSTNAME']
    db_name = os.environ['TEST_POSTGRESQL_DB_NAME']
    engine = create_engine(f'postgresql+psycopg2://{user}:{passwd}@{hostname}/{db_name}')
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture
def session(engine):
    session = Session(engine)
    yield session
    session.rollback()
    session.close()


@pytest.fixture
def session_exemplary(session):
    portugal = Team(name="Portugal")
    south_korea = Team(name="South Korea")
    uruguay = Team(name="Uruguay")
    ghana = Team(name="Ghana")

    session.add_all([portugal, south_korea, uruguay, ghana])
    session.commit()

    match_0 = Match(first_team_id=uruguay.id, second_team_id=south_korea.id, first_team_score=0, second_team_score=0)
    match_1 = Match(first_team_id=portugal.id, second_team_id=ghana.id, first_team_score=3, second_team_score=2)
    match_2 = Match(first_team_id=south_korea.id, second_team_id=ghana.id, first_team_score=2, second_team_score=3)
    match_3 = Match(first_team_id=portugal.id, second_team_id=uruguay.id, first_team_score=2, second_team_score=0)
    match_4 = Match(first_team_id=south_korea.id, second_team_id=portugal.id, first_team_score=2, second_team_score=1)
    match_5 = Match(first_team_id=ghana.id, second_team_id=uruguay.id, first_team_score=0, second_team_score=2)
    session.add_all([match_0, match_1, match_2, match_3, match_4, match_5])
    session.commit()

    yield session


