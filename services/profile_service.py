from database.database import SessionLocal
from database.profile_repository import ProfileRepository


class ProfileService:

    def __init__(self):

        self.db = SessionLocal()

        self.repository = ProfileRepository(self.db)

    def get_profile(self):

        return self.repository.load()

    def save_profile(self, profile):

        self.repository.save(profile)