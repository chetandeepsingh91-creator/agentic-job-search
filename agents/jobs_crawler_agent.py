from services.serpapi_service import fetch_jobs
def run(role):
    jobs = fetch_jobs(role)
    
    return jobs
