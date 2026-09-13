# services/search_query_builder.py
from models.job_search_request import JobSearchRequest

class SearchQueryBuilder:

    @staticmethod
    def build(profile):

        # Preferred Roles — use primary role for SerpAPI Google Jobs compatibility
        roles = profile.preferred_roles or []

        if roles:
            role_query = roles[0]
        else:
            role_query = "Product Manager"

        # Preferred Locations — use primary location as SerpAPI location param
        locations = profile.preferred_locations or []

        if locations:
            location_query = locations[0]
        else:
            location_query = "India"

        # Experience
        """ experience = ""
        if profile.years_experience:
            experience = f"{profile.years_experience}+ years"
 """
        # Industries
        industries = ""

        if profile.industries:
            industries = " ".join(profile.industries)

        query = f"{role_query}" # {industries}" # {experience}"

        return JobSearchRequest(
            query=query.strip(),
            location=location_query
        )