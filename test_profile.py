from services.profile_service import ProfileService
from models.profile import Profile

service = ProfileService()

profile = Profile(

    name="Chetandeep Singh",

    email="test@test.com",

    phone="9999999999",

    linkedin="linkedin.com/in/test",

    github="github.com/test",

    resume="Senior Product Manager with AI experience.",

    preferred_roles=[
        "Senior Product Manager",
        "AI Product Manager"
    ],

    preferred_locations=[
        "Remote",
        "Bangalore"
    ],

    skills=[
        "Python",
        "LLM",
        "Azure AI Search"
    ],

    years_experience=10,

    expected_salary="55 LPA",

    industries=[
        "AI",
        "SaaS"
    ]

)

service.save_profile(profile)

loaded = service.get_profile()

print(loaded)