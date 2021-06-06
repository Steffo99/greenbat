import enum


class Rating(str, enum.Enum):
    DISLIKED = "DISLIKED"
    MIXED = "MIXED"
    LIKED = "LIKED"
    LOVED = "LOVED"


class Completition(str, enum.Enum):
    UNPLAYED = "UNPLAYED"
    STARTED = "STARTED"
    BEATEN = "BEATEN"
    COMPLETED = "COMPLETED"
    MASTERED = "MASTERED"
    NOT_APPLICABLE = "NOT_APPLICABLE"
