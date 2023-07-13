from sqlalchemy import select, func, case, desc, asc
from sqlalchemy.orm import Session

from models import Team, Match

__scores_as_first_team = select(
    Team,
    Match.first_team_score.label("scored"),
    Match.second_team_score.label("conceded")
).join(Team.in_first_team)

__scores_as_second_team = select(
    Team,
    Match.second_team_score.label("scored"),
    Match.first_team_score.label("conceded")
).join(Team.in_second_team)

__results = __scores_as_first_team.union_all(__scores_as_second_team)

__standings = \
    select(
        __results.c.id,
        __results.c.name,
        func.sum(
            case(
                (__results.c.scored > __results.c.conceded, 3),
                (__results.c.scored == __results.c.conceded, 1),
                else_=0
            )
        ).label("points"),
        func.sum((__results.c.scored - __results.c.conceded)).label("goal_diff"),
        func.sum(__results.c.scored).label("scored")
    ) \
    .group_by(__results.c.id, __results.c.name) \
    .order_by(desc("points"), desc("goal_diff"), desc("scored"))

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

    two_teams = select(
        __standings.c.id,
        __standings.c.name
    ).limit(2)

    return session.execute(two_teams).all()


def max_points(session: Session):
    return session.scalar(select(func.max(__standings.c.points)))


def worst_team_name(session: Session):
    q = select(__standings.c.name).order_by(asc(__standings.c.points), asc(__standings.c.goal_diff), asc(__standings.c.scored))
    return session.scalar(q)
