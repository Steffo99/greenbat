import sqlalchemy as s
import sqlalchemy.orm as so
import sqlalchemy.dialects.postgresql as sp
import greenbat.database.types as gt
import uuid
from greenbat.database.tables._base import Base


class Element(Base):
    __tablename__ = "elements"

    id = s.Column(s.BigInteger, primary_key=True)

    owner_id = s.Column(s.String, s.ForeignKey("users.sub"), nullable=False)
    game_id = s.Column(s.BigInteger, s.ForeignKey("games.id"), nullable=False)

    owner = so.relationship("User", back_populates="elements")
    game = so.relationship("Game", back_populates="elements")
