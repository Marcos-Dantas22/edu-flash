import enum

class GenderEnum(enum.Enum):
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"
    NONE = "N"

class LanguageEnum(enum.Enum):
    PORTUGUESE_BR = "PT_BR"
    ENGLISH = "EN"