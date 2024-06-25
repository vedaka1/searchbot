from dataclasses import dataclass


@dataclass
class Document:
    """The domain model of the document"""

    index: int
    id: int
    department: str
    document_type: str
    first_publishing: str
    publishing_date: str
    lvl_1: str
    queue_1: str
    lvl_2: str
    queue_2: str
    lvl_3: str
    queue_3: str
    lvl_4: str
    queue_4: str
    credentials: str
    title: str
    link_text: str
