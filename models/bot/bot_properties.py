from dataclasses import dataclass


@dataclass
class Bot:
    token: str
    database_url: str