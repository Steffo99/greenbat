import sqlalchemy as s
import sqlalchemy.orm as so
import sqlalchemy.dialects.postgresql as sp
import greenbat.database.types as gt
import uuid
from greenbat.database.tables._base import Base


class AccountSteam(Base):
    __tablename__ = "accounts_steam"

    steamid = s.Column(gt.SteamID, primary_key=True)

    owner_id = s.Column(s.String, s.ForeignKey("users.sub"), nullable=False)
    last_update = s.Column(s.DateTime, nullable=False)

    owner = so.relationship("User", back_populates="accounts_steam")
