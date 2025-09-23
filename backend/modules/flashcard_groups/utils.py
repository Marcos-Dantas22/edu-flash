import enum

class LevelEnum(enum.Enum):
    DIFFICULT = "D"
    MEDIUM = "M"
    EASY = "E"


class TypePermissionEnum(enum.Enum):
    GROUP_PUBLIC = "GPUBLIC"
    GROUP_PRIVATE = "GPRIVATE"