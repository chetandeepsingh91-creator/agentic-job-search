# database/profile_repository.py

import json

from sqlalchemy.orm import Session

from database.models import ProfileDB
from models.profile import Profile


class ProfileRepository:

    def __init__(self, db: Session):
        self.db = db

    def save(self, profile: Profile):

        existing = self.db.query(ProfileDB).first()

        if existing:
            
            existing.name = profile.name
            existing.email = profile.email
            existing.phone = profile.phone
            existing.linkedin = profile.linkedin
            existing.github = profile.github
            existing.resume = profile.resume

            existing.preferred_roles = json.dumps(profile.preferred_roles)

            existing.preferred_locations = json.dumps(profile.preferred_locations)

            existing.skills = json.dumps(profile.skills)

            existing.years_experience = profile.years_experience

            existing.expected_salary = profile.expected_salary

            existing.industries = json.dumps(profile.industries)

        else:

            print("Creating new profile")
            new_profile = ProfileDB(

                name=profile.name,

                email=profile.email,

                phone=profile.phone,

                linkedin=profile.linkedin,

                github=profile.github,

                resume=profile.resume,

                preferred_roles=json.dumps(profile.preferred_roles),

                preferred_locations=json.dumps(profile.preferred_locations),

                skills=json.dumps(profile.skills),

                years_experience=profile.years_experience,

                expected_salary=profile.expected_salary,

                industries=json.dumps(profile.industries)

            )

            self.db.add(new_profile)

        self.db.commit()

    def load(self):

        profile = self.db.query(ProfileDB).first()

        if not profile:
            return None

        return Profile(

            name=profile.name,

            email=profile.email,

            phone=profile.phone,

            linkedin=profile.linkedin,

            github=profile.github,

            resume=profile.resume,

            preferred_roles=json.loads(profile.preferred_roles or "[]"),

            preferred_locations=json.loads(profile.preferred_locations or "[]"),

            skills=json.loads(profile.skills or "[]"),

            years_experience=profile.years_experience,

            expected_salary=profile.expected_salary,

            industries=json.loads(profile.industries or "[]")

        )