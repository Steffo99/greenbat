import sqlalchemy.orm
import greenbat.config


engine = sqlalchemy.create_engine(greenbat.config.cfg["database.uri"])
Session = sqlalchemy.orm.sessionmaker(bind=engine)
