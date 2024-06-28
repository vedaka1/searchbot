from dataclasses import dataclass


@dataclass
class Website:
    index: int
    long_name: str
    short_name: str
    domain: str
    contacts_1: str
    contacts_2: str
