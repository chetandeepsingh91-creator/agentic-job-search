import requests
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

SERP_API_KEY = os.getenv("SERPAPI_KEY")

def fetch_jobs(role="Product Manager", location="Noida"):
    url = "https://serpapi.com/search.json"

    params = {
        "engine": "google_jobs",
        "q": f"{role} {location}",
        "api_key": SERP_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()
    jobs = []

    for job in data.get("jobs_results", [])[:5]:
        jobs.append({
            "title": job.get("title"),
            "company": job.get("company_name"),
            "location": job.get("location"),
            "description": job.get("description")
        })

    return jobs