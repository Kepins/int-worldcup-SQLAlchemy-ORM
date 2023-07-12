from models import Base, Team, Match
from sqlalchemy import create_engine

if __name__ == '__main__':
    engine = create_engine("sqlite://", echo=True)

    Base.metadata.create_all(engine)

