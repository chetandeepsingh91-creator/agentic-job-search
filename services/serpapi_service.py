import requests
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

SERP_API_KEY = os.getenv("SERPAPI_KEY")

def fetch_jobs(query, location):
    url = "https://serpapi.com/search.json"

    params = {
        "engine": "google_jobs",
        "q": f"{query} {location}",
        "api_key": SERP_API_KEY
    }

    print("query: ",params["q"])
    response = requests.get(url, params=params)
    data = response.json()
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
            "thumbnail": job.get("thumbnail")
        })

    return jobs