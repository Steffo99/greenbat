import sqlalchemy as s
import sqlalchemy.orm as so
import sqlalchemy.dialects.postgresql as sp
import greenbat.database.types as gt
import uuid
from greenbat.database.tables._base import Base


class Element(Base):
    """
    A single instance of a game owned by an user.
    """
    __tablename__ = "elements"

    uuid = s.Column(sp.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    owner_id = s.Column(s.String, s.ForeignKey("users.sub"), nullable=False)
    game_id = s.Column(sp.UUID(as_uuid=True), s.ForeignKey("games.uuid"), nullable=False)

    owner = so.relationship("User", back_populates="elements")
    game = so.relationship("Game", back_populates="elements")
