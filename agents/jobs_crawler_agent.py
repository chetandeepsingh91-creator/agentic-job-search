from services.serpapi_service import fetch_jobs
from services.search_query_builder import SearchQueryBuilder

def run(search_request):
    
    jobs = fetch_jobs(search_request.query, location = search_request.location)
    
    return jobs
