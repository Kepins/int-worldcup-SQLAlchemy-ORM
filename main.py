import os

from sqlalchemy.orm import Session

from models import Base
from sqlalchemy import create_engine
from dotenv import load_dotenv

from queries import *

if __name__ == '__main__':
    load_dotenv()
    user = os.environ['POSTGRESQL_USER']
    passwd = os.environ['POSTGRESQL_PASSWD']
    hostname = os.environ['POSTGRESQL_HOSTNAME']
    db_name = os.environ['POSTGRESQL_DB_NAME']
    engine = create_engine(f'postgresql+psycopg2://{user}:{passwd}@{hostname}/{db_name}')

    Base.metadata.create_all(engine)
    with Session(engine) as session:
        if db_empty(session):
            insert_WC2022GroupC(engine)


