from dataclasses import dataclass, field
from typing import List


@dataclass
class DiscoveredPerson:

    name: str
    title: str
    linkedin_url: str
    snippet: str
    target_type: str
    search_query: str
    outreach_message: str = ""


@dataclass
class NetworkingResult:

    people: List[DiscoveredPerson] = field(default_factory=list)
    discovery_available: bool = False
    discovery_error: str = ""
