from sqlalchemy import select, func, case, desc
from sqlalchemy.orm import Session

from models import Team, Match


def db_empty(session):
    num_teams = session.execute(select(func.count(Team.id))).scalar()
    if num_teams == 0:
        return True


def insert_WC2022GroupC(session: Session):
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


def two_best_teams(session: Session):

    scores_as_first_team = select(
        Team,
        Match.first_team_score.label("scored"),
        Match.second_team_score.label("conceded")
    ).join(Team.in_first_team)

    scores_as_second_team = select(
        Team,
        Match.second_team_score.label("scored"),
        Match.first_team_score.label("conceded")
    ).join(Team.in_second_team)

    results = scores_as_first_team.union_all(scores_as_second_team)

    standings = \
        select(
            results.c.id,
            results.c.name,
            func.sum(
                case(
                    (results.c.scored > results.c.conceded, 3),
                    (results.c.scored == results.c.conceded, 1),
                    else_=0
                )
            ).label("points"),
            func.sum((results.c.scored - results.c.conceded)).label("goal_diff"),
            func.sum(results.c.scored).label("scored")
        )\
        .group_by(results.c.id, results.c.name)\
        .order_by(desc("points"), desc("goal_diff"), desc("scored"))

    two_teams = select(
        standings.c.id,
        standings.c.name
    ).limit(2)

    return session.execute(two_teams).all()


def max_points(session: Session):
    pass

def worst_team_name(session: Session):
    pass
