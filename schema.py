from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class ClassificationOptions(str, Enum):
    POLITICAL_CORRESPONDENCE = "Political Correspondence"
    OFFICIAL_RECORDS = "Official Records"
    PRINTED_MATERIAL = "Printed Material"
    LEGAL_DOCUMENTS = "Legal Documents"


class LanguageOptions(str, Enum):
    GERMAN = "German"
    ITALIAN = "Italian"


class MetadataSchema(BaseModel):
    classification: str
    language: str
    issue_date: str
    places: str | List[str]
    signature: str
    summary: str

    # Wir können auch striktere Typen verwenden, um die möglichen Werte einzuschränken:
    # classification: ClassificationOptions
    # language: LanguageOptions  # German or italian
    # issue_date: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$", description="Date in the format YYYY-MM-DD")
    # places: List[str]
