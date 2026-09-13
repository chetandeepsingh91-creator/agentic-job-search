from dotenv import load_dotenv

from services.linkedin_discovery_service import (
    LinkedInDiscoveryService
)

load_dotenv()


service = LinkedInDiscoveryService()


results = service.search_people(
    search_query=(
        "Senior Product Manager AI Search "
        "Agoda Bangkok"
    ),
    target_type="Hiring Manager",
    max_results=5
)


print("\nDiscovered People\n")


for person in results:

    print("--------------------------------")
    print("Name:", person.name)
    print("Title:", person.title)
    print("LinkedIn:", person.linkedin_url)
    print("Target:", person.target_type)
    print("Snippet:", person.snippet)