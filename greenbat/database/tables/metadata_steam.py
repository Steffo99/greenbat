import sqlalchemy as s
import sqlalchemy.orm as so
import sqlalchemy.dialects.postgresql as sp
import greenbat.database.types as gt
import uuid
from greenbat.database.tables._base import Base


class MetadataSteam(Base):
    __tablename__ = "metadata_steam"

    game_id = s.Column(s.Integer, s.ForeignKey("games.id"), primary_key=True)

    appid = s.Column(s.BigInteger, nullable=False)
    title = s.Column(s.String, nullable=False)

    game = so.relationship("Game", back_populates="metadata_steam", uselist=False)

    @property
    def url_store(self) -> str:
        return f"https://store.steampowered.com/app/{self.appid}/"

    @property
    def url_community(self) -> str:
        return f"https://steamcommunity.com/app/{self.appid}"
