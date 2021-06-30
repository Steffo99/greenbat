import sqlalchemy as s
import sqlalchemy.orm as so
import sqlalchemy.dialects.postgresql as sp
from greenbat.database.tables._base import Base


class Game(Base):
    __tablename__ = "games"

    id = s.Column(s.Integer, primary_key=True)

    elements = so.relationship("Element", back_populates="game", cascade="all, delete-orphan")
    metadata_steam = so.relationship("MetadataSteam", back_populates="game", uselist=False, cascade="all, delete-orphan")
    metadata_custom = so.relationship("MetadataCustom", back_populates="game", uselist=False, cascade="all, delete-orphan")
