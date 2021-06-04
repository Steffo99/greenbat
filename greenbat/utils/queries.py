import fastapi as f
import sqlalchemy as s
import sqlalchemy.sql as ss
import sqlalchemy.orm as so
import pydantic


def list_(session: so.Session, table):
    objs = session.execute(
        ss.select(table)
    ).scalars()
    return list(objs)


def retrieve(session: so.Session, table, condition):
    obj = session.execute(
        ss.select(table).where(condition)
    ).scalar()
    if obj is None:
        raise f.HTTPException(404, f"{table.__tablename__} not found")
    return obj


def create(session: so.Session, table, data: pydantic.BaseModel):
    obj = table(**data.dict())
    session.add(obj)
    session.commit()
    return obj


def edit(session: so.Session, table, condition, data: pydantic.BaseModel):
    obj = session.execute(
        ss.select(table).where(condition)
    ).scalar()
    if obj is None:
        raise f.HTTPException(404, f"{table.__tablename__} not found")
    for key, val in data.dict().items():
        obj.__setattr__(key, val)
    session.commit()
    return obj


def destroy(session: so.Session, table, condition):
    obj = session.execute(
        ss.select(table).where(condition)
    ).scalar()
    if obj is None:
        raise f.HTTPException(404, f"{table.__tablename__} not found")
    session.delete(obj)
    session.commit()
    return None
