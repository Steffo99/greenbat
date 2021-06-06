import sqlalchemy as s
import sqlalchemy.orm as so
import sqlalchemy.dialects.postgresql as sp
import greenbat.database.types as gt
import uuid
from greenbat.database.tables._base import Base
from greenbat.database.enums import Rating, Completition


class Element(Base):
    __tablename__ = "elements"

    id = s.Column(s.BigInteger, primary_key=True)

    owner_id = s.Column(s.String, s.ForeignKey("users.sub"), nullable=False)
    game_id = s.Column(s.BigInteger, s.ForeignKey("games.id"), nullable=False)

    rating = s.Column(s.Enum(Rating))
    completition = s.Column(s.Enum(Completition))

    owner = so.relationship("User", back_populates="elements")
    game = so.relationship("Game", back_populates="elements")
