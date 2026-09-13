import os
import re

import requests
from dotenv import load_dotenv

load_dotenv()

SERP_API_KEY = os.getenv("SERPAPI_KEY")
SERPAPI_URL = "https://serpapi.com/search.json"


def _simplify_query(query: str) -> str:
    cleaned = re.sub(r'["\']', "", query or "")
    cleaned = re.sub(r"\s+OR\s+", " ", cleaned, flags=re.IGNORECASE)
    return cleaned.strip()


def _simplify_location(location: str) -> str:
    if not location:
        return ""
    return location.split(" OR ")[0].strip()


def _parse_jobs(data):
    jobs = []
    for job in data.get("jobs_results", [])[:5]:
        jobs.append({
            "title": job.get("title"),
            "company": job.get("company_name"),
            "location": job.get("location"),
            "description": job.get("description"),
            "apply_link": job.get("apply_options", [{}])[0].get("link"),
            "posted_at": job.get("detected_extensions", {}).get("posted_at"),
            "schedule": job.get("detected_extensions", {}).get("schedule_type"),
            "via": job.get("via"),
            "thumbnail": job.get("thumbnail"),
        })
    return jobs


def _fetch_jobs_once(query, location):
    params = {
        "engine": "google_jobs",
        "q": query,
        "api_key": SERP_API_KEY,
    }
    if location:
        params["location"] = location

    response = requests.get(SERPAPI_URL, params=params, timeout=30)
    data = response.json()
    return response.status_code, data, _parse_jobs(data)


def fetch_jobs(query, location):
    attempts = [
        (query, location),
        (_simplify_query(query), _simplify_location(location)),
    ]

    seen = set()
    last_error = ""

    for attempt_query, attempt_location in attempts:
        key = (attempt_query, attempt_location)
        if not attempt_query or key in seen:
            continue
        seen.add(key)

        print(f"SerpAPI job search: q={attempt_query!r} location={attempt_location!r}")
        status_code, data, jobs = _fetch_jobs_once(
            attempt_query, attempt_location
        )
        last_error = data.get("error") or ""

        if jobs:
            return jobs

    if last_error:
        print(f"SerpAPI job search failed: {last_error}")

    return []
