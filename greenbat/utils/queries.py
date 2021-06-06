import royalnet.royaltyping as t
import fastapi as f
import sqlalchemy as s
import sqlalchemy.exc
import sqlalchemy.sql as ss
import sqlalchemy.orm as so
import greenbat.config as gc
import pydantic


RowType = t.TypeVar("RowType")


def check_limit(value) -> None:
    max_limit = gc.cfg["api.list.maxlimit"]
    if value > max_limit:
        raise f.HTTPException(400, f"Max limit of {max_limit} exceeded, try a lower value")


def list_(session: so.Session, table: t.Type[RowType], limit: int, offset: int, condition=None, order=None) -> list[RowType]:
    """
    List all objects in a table.

    :param session: The :class:`sqlalchemy.orm.Session` to use.
    :param table: The table to list the objects of.
    :param limit: The maximum number of items to retrieve. Must be lower than ``api.list.maxlimit``.
    :param offset: The position of the first item to retrieve.
    :param condition: A filtering condition that returned objects should satisfy.
    :param order: The order to use when listing objects.
    :return: A :class:`list` of objects.
    """

    check_limit(limit)

    qy = ss.select(table)
    qy = qy.where(condition) if condition else qy
    qy = qy.order_by(order) if order else qy
    qy = qy.limit(limit)
    qy = qy.offset(offset)

    return session.execute(qy).all()


def list_joined(session: so.Session, tables: list[t.Type[RowType]], limit: int, offset: int, order=None) -> list[RowType]:
    """
    List all objects in joined tables.

    :param session: The :class:`sqlalchemy.orm.Session` to use.
    :param tables: The tables to list the objects of, in join order.
    :param limit: The maximum number of items to retrieve. Must be lower than ``api.list.maxlimit``.
    :param offset: The position of the first item to retrieve.
    :param order: The order to use when listing objects.
    :return: A :class:`list` of objects.
    """

    check_limit(limit)

    qy = ss.select(tables[0])
    for table in tables[1:]:
        qy = qy.join(table)
    qy = qy.order_by(order) if order else qy
    qy = qy.limit(limit)
    qy = qy.offset(offset)

    return list(session.execute(qy).scalars())


def retrieve(session: so.Session, table: t.Type[RowType], condition) -> RowType:
    """
    Retrieve the object satisfying the requested condition.

    :param session: The :class:`sqlalchemy.orm.Session` to use.
    :param table: The table to retrieve the objects from.
    :param condition: The condition to check when retrieving the object.
    :return: The retrieved object.
    """

    try:
        return session.execute(
            ss.select(table).where(condition)
        ).scalar()

    except sqlalchemy.exc.NoResultFound:
        raise f.HTTPException(404, f"Not found")

    except sqlalchemy.exc.MultipleResultsFound:
        raise f.HTTPException(500, f"Multiple found (this is a bug, please report it!)")


def create(session: so.Session, table: t.Type[RowType], model_data: pydantic.BaseModel, **additional_data: t.Kwargs) -> RowType:
    """
    Create a new object with the passed data, **committing the session** in the process.

    :param session: The :class:`sqlalchemy.orm.Session` to use.
    :param table: The table to create the object in.
    :param model_data: The data the object should have, as a :class:`pydantic.BaseModel`.
    :param additional_data: Additional data the object should have, as kwargs.
    :return: The created object.
    """

    obj = table(**model_data.dict(), **additional_data)

    session.add(obj)
    session.commit()
    return obj


def merge(session: so.Session, table: t.Type[RowType], condition, model_data: pydantic.BaseModel, **additional_data: t.Kwargs) -> tuple[RowType, bool]:
    """
    Create or update the object matching the condition, **committing the session** in the process.

    :param session: The :class:`sqlalchemy.orm.Session` to use.
    :param table: The table to create the object in.
    :param condition: The condition to check.
    :param model_data: The data the object should use, as a :class:`pydantic.BaseModel`.
    :param additional_data: Additional data the object should have, as kwargs.
    :return: A tuple containing the object and a bool determining if a new object was created.
    """

    try:
        obj = session.execute(
            ss.select(table).where(condition)
        ).scalar()

    except sqlalchemy.exc.NoResultFound:
        obj = table(**model_data.dict(), **additional_data)
        session.add(obj)
        session.commit()
        return obj, True

    except sqlalchemy.exc.MultipleResultsFound:
        raise f.HTTPException(500, f"Multiple found (this is a bug, please report it!)")

    else:
        for key, val in {**model_data.dict(), **additional_data}.items():
            obj.__setattr__(key, val)
        session.commit()
        return obj, False


def edit(session: so.Session, table: t.Type[RowType], condition, model_data: pydantic.BaseModel, **additional_data: t.Kwargs) -> RowType:
    """
    Edit the object satisfying the requested condition with the passed data, **committing the session** in the process.

    :param session: The :class:`sqlalchemy.orm.Session` to use.
    :param table: The table to retrieve the objects from.
    :param model_data: The new data the object should have, as a :class:`pydantic.BaseModel`.
    :param additional_data: Additional data the object should have, as kwargs.
    :param condition: The condition to check when selecting the object.
    :return: The retrieved object.
    """

    obj = retrieve(session, table, condition)

    for key, val in {**model_data.dict(), **additional_data}.items():
        obj.__setattr__(key, val)
    session.commit()

    return obj


def destroy(session: so.Session, table, condition) -> None:
    """
    Delete the object satisfying the condition, **committing the session** in the process.

    :param session: The :class:`sqlalchemy.orm.Session` to use.
    :param table: The table to retrieve the objects from.
    :param condition: The condition to check when selecting the object.
    :return: The retrieved object.
    """

    try:
        obj = session.execute(
            ss.select(table).where(condition)
        ).scalar()
        session.delete(obj)
        session.commit()

    except sqlalchemy.exc.NoResultFound:
        raise f.HTTPException(404, f"Not found")

    except sqlalchemy.exc.MultipleResultsFound:
        raise f.HTTPException(500, f"Multiple found (this is a bug, please report it!)")
