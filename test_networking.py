from dotenv import load_dotenv

from services.networking_service import NetworkingService


load_dotenv()


job = {
    "title": "Senior Technical Product Manager - AI Search",
    "company": "Agoda",
    "location": "Bangkok",
    "description": """
We are looking for a Technical Product Manager to lead
AI-powered search and recommendation experiences.

Requirements:
- Product management experience
- Search and recommendation systems
- Machine learning
- Generative AI
- Cross-functional leadership
""",
}

service = NetworkingService()

result = service.find_people(job=job)

print("\nDiscovered People:\n")

if not result.discovery_available:
    print("SERPAPI_KEY is not configured. Skipping people search.")
elif not result.people:
    print("No public profiles found.")
    if result.discovery_error:
        print("Discovery error:", result.discovery_error)
else:
    for person in result.people:
        print("--------------------------------")
        print("Name:", person.name)
        print("Title:", person.title)
        print("LinkedIn:", person.linkedin_url)
        print("Target:", person.target_type)
