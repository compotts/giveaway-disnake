from dataclasses import dataclass


@dataclass
class ConvertedUrl:
    hostname: str
    port: int
    user: str
    password: str
    db: str
