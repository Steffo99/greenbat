import sqlalchemy.orm
import greenbat.config


engine = sqlalchemy.create_engine(greenbat.config.cfg["database.uri"])
Session = sqlalchemy.orm.sessionmaker(bind=engine)


def dep_database():
    with Session(future=True) as session:
        yield session
