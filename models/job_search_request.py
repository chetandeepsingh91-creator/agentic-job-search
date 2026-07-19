from dataclasses import dataclass


@dataclass
class JobSearchRequest:
    query: str
    location: str