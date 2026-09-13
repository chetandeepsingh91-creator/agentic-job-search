import os
import requests

from dotenv import load_dotenv

from models.networking import DiscoveredPerson


load_dotenv()


class LinkedInDiscoveryService:

    def __init__(self):

        self.api_key = os.getenv("SERPAPI_KEY")

        if not self.api_key:
            raise ValueError(
                "SERPAPI_KEY is not configured."
            )

    def search_people(
        self,
        search_query: str,
        target_type: str,
        company: str = "",
        max_results: int = 5
    ):

        url = "https://serpapi.com/search.json"

        terms = [search_query]
        if company and company.lower() not in search_query.lower():
            terms.append(company)

        query = "site:linkedin.com/in/ " + " ".join(
            term for term in terms if term
        )

        params = {
            "engine": "google",
            "q": query,
            "api_key": self.api_key,
            "num": max_results
        }

        response = requests.get(
            url,
            params=params,
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        people = []
        seen_urls = set()

        for result in data.get("organic_results", []):

            linkedin_url = result.get("link", "")

            if "linkedin.com/in/" not in linkedin_url:
                continue

            if "/dir/" in linkedin_url or "/pub/dir/" in linkedin_url:
                continue

            if linkedin_url in seen_urls:
                continue

            seen_urls.add(linkedin_url)

            title = result.get("title", "")
            snippet = result.get("snippet", "")

            people.append(
                DiscoveredPerson(
                    name=self._extract_name(title),
                    title=title,
                    linkedin_url=linkedin_url,
                    snippet=snippet,
                    target_type=target_type,
                    search_query=search_query
                )
            )

            if len(people) >= max_results:
                break

        return people

    @staticmethod
    def _extract_name(title: str):

        if not title:
            return ""

        # Typical Google result:
        # "John Smith - Product Manager - LinkedIn"

        name = title.split(" - ")[0].strip()
        name = name.replace(" | LinkedIn", "").replace(" - LinkedIn", "")
        return name.strip()
