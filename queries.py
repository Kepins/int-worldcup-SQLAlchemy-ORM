from sqlalchemy import select, func
from sqlalchemy.orm import Session

from models import Team, Match


def db_empty(session):
    num_teams = session.execute(select(func.count(Team.id))).scalar()
    if num_teams == 0:
        return True

def insert_WC2022GroupC(session):
    argentina = Team(name="Argentina")
    poland = Team(name="Poland")
    saudi_arabia = Team(name="Saudi Arabia")
    mexico = Team(name="Mexico")
    session.add_all([argentina, poland, saudi_arabia, mexico])
    session.commit()
    match_0 = Match(first_team_id=argentina.id, second_team_id=saudi_arabia.id,
                    first_team_score=1, second_team_score=2)
    match_1 = Match(first_team_id=mexico.id, second_team_id=poland.id,
                    first_team_score=0, second_team_score=0)
    match_2 = Match(first_team_id=poland.id, second_team_id=saudi_arabia.id,
                    first_team_score=2, second_team_score=0)
    match_3 = Match(first_team_id=argentina.id, second_team_id=mexico.id,
                    first_team_score=2, second_team_score=0)
    match_4 = Match(first_team_id=poland.id, second_team_id=argentina.id,
                    first_team_score=0, second_team_score=2)
    match_5 = Match(first_team_id=saudi_arabia.id, second_team_id=mexico.id,
                    first_team_score=1, second_team_score=2)

    session.add_all([match_0, match_1, match_2, match_3, match_4, match_5])

    session.commit()

def two_best_teams(session):
    pass

def max_points(session):
    pass

def worst_team_name(session):
    pass