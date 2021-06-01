import sqlalchemy as s
import sqlalchemy.orm as so
import sqlalchemy.dialects.postgresql as sp
import greenbat.database.types as gt
import uuid
from greenbat.database.tables._base import Base


class Game(Base):
    """
    A game.
    """
    __tablename__ = "games"

    uuid = s.Column(sp.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = s.Column(s.String, nullable=False)

    elements = so.relationship("Element", back_populates="game")
