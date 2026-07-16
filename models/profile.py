from dataclasses import dataclass, field
from typing import List


@dataclass
class Profile:

    name: str

    email: str

    phone: str

    linkedin: str

    github: str

    resume: str

    preferred_roles: List[str] = field(default_factory=list)

    preferred_locations: List[str] = field(default_factory=list)

    skills: List[str] = field(default_factory=list)

    years_experience: int = 0

    expected_salary: str = ""

    industries: List[str] = field(default_factory=list)