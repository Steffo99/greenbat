import sqlalchemy as s
import sqlalchemy.orm as so
import sqlalchemy.dialects.postgresql as sp
import greenbat.database.types as gt
import uuid
from greenbat.database.tables._base import Base


class User(Base):
    __tablename__ = "users"

    sub = s.Column(s.String, primary_key=True)

    last_update = s.Column(s.DateTime, nullable=False)
    name = s.Column(s.String, nullable=False)
    picture = s.Column(s.String, nullable=False)

    elements = so.relationship("Element", back_populates="owner")
    accounts_steam = so.relationship("AccountSteam", back_populates="owner")

    def __str__(self):
        return self.name
