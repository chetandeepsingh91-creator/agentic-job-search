from typing import List

from models.networking import DiscoveredPerson, NetworkingResult
from services.linkedin_discovery_service import LinkedInDiscoveryService


def _job_field(job, key: str) -> str:
    if not isinstance(job, dict):
        return ""
    return (job.get(key) or "").strip()


def _join_parts(*parts: str) -> str:
    return " ".join(part for part in parts if part)


class NetworkingService:

    def __init__(self):

        try:
            self.discovery = LinkedInDiscoveryService()
        except ValueError:
            self.discovery = None

    def find_people(
        self,
        job,
        discover_people: bool = True,
        max_people_per_target: int = 3,
        max_discovery_queries: int = 3,
    ):

        title = _job_field(job, "title")
        company = _job_field(job, "company")
        location = _job_field(job, "location")

        queries = [
            ("Role", _join_parts(title, company, location)),
            ("Recruiter", _join_parts("recruiter", company, location)),
            ("Hiring Manager", _join_parts("hiring manager", company, location)),
        ]

        people = []
        seen_urls = set()
        discovery_error = ""

        if discover_people and self.discovery is not None:
            queried = 0
            for target_type, search_query in queries:
                if queried >= max_discovery_queries:
                    break
                if not search_query:
                    continue
                try:
                    found = self.discovery.search_people(
                        search_query=search_query,
                        target_type=target_type,
                        company=company,
                        max_results=max_people_per_target,
                    )
                    queried += 1
                    people.extend(
                        self._unique_people(found, seen_urls)
                    )
                except Exception as e:
                    discovery_error = str(e)
                    print(
                        f"LinkedIn discovery failed for "
                        f"'{search_query}': {e}"
                    )

        return NetworkingResult(
            people=people,
            discovery_available=self.discovery is not None,
            discovery_error=discovery_error,
        )

    @staticmethod
    def _unique_people(found, seen_urls) -> List[DiscoveredPerson]:
        unique = []
        for person in found:
            if person.linkedin_url in seen_urls:
                continue
            seen_urls.add(person.linkedin_url)
            unique.append(person)
        return unique
