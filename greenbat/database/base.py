import uuid
import sqlalchemy as s
import sqlalchemy.orm as so
import sqlalchemy.dialects.postgresql as sp
import greenbat.database.types as gt


Base = so.declarative_base()


class User(Base):
    """
    An user, as returned by Auth0.
    """
    __tablename__ = "users"

    sub = s.Column(s.String, primary_key=True)

    last_update = s.Column(s.DateTime, nullable=False)
    name = s.Column(s.String, nullable=False)
    nickname = s.Column(s.String, nullable=False)
    avatar = s.Column(s.String, nullable=False)
    email = s.Column(s.String, nullable=False)

    games_owned = so.relationship("User", back_populates="owner")

    def __str__(self):
        return self.name


class Steam(Base):
    """
    An user's Steam account.
    """
    __tablename__ = "steam"

    steamid = s.Column(gt.SteamID, primary_key=True)

    owner_id = s.Column(s.String, s.ForeignKey("users.sub"), nullable=False)

    owner = so.relationship("User", back_populates="steam_accounts")


class Element(Base):
    """
    A single instance of a game owned by an user.
    """
    __tablename__ = "elements"

    uuid = s.Column(sp.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    owner_id = s.Column(s.String, s.ForeignKey("users.sub"), nullable=False)
    game_id = s.Column(sp.UUID(as_uuid=True), s.ForeignKey("games.uuid"), nullable=False)

    owner = so.relationship("User", back_populates="games_owned")


class Game(Base):
    """
    A game.
    """
    __tablename__ = "games"

    uuid = s.Column(sp.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = s.Column(s.String, nullable=False)
