import json
import os
from dataclasses import asdict

from models.profile import Profile


PROFILE_FILE = "data/profile.json"


def save_profile(profile: Profile):

    os.makedirs("data", exist_ok=True)

    with open(PROFILE_FILE, "w", encoding="utf-8") as f:

        json.dump(asdict(profile), f, indent=4)


def load_profile():

    if not os.path.exists(PROFILE_FILE):

        return None

    with open(PROFILE_FILE, "r", encoding="utf-8") as f:

        data = json.load(f)

    return Profile(**data)