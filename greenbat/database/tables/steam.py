import sqlalchemy as s
import sqlalchemy.orm as so
import sqlalchemy.dialects.postgresql as sp
import greenbat.database.types as gt
import uuid
from greenbat.database.tables._base import Base


class Steam(Base):
    """
    An user's Steam account.
    """
    __tablename__ = "steam"

    steamid = s.Column(gt.SteamID, primary_key=True)

    owner_id = s.Column(s.String, s.ForeignKey("users.sub"), nullable=False)

    owner = so.relationship("User", back_populates="steams")
