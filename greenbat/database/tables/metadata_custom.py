import sqlalchemy as s
import sqlalchemy.orm as so
import sqlalchemy.dialects.postgresql as sp
import greenbat.database.types as gt
import uuid
from greenbat.database.tables._base import Base


class MetadataCustom(Base):
    __tablename__ = "metadata_custom"

    game_id = s.Column(s.Integer, s.ForeignKey("games.id"), primary_key=True)

    creator_sub = s.Column(s.String, s.ForeignKey("users.sub"), nullable=False)
    title = s.Column(s.String, nullable=False)
    url = s.Column(s.String)

    game = so.relationship("Game", back_populates="metadata_custom", uselist=False)
    creator = so.relationship("User", back_populates="metadata_custom_owned")
