# database/models.py

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from .database import Base


class ProfileDB(Base):

    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True)

    name = Column(String)

    email = Column(String)

    phone = Column(String)

    linkedin = Column(String)

    github = Column(String)

    resume = Column(Text)

    preferred_roles = Column(Text)

    preferred_locations = Column(Text)

    skills = Column(Text)

    years_experience = Column(Integer)

    expected_salary = Column(String)

    industries = Column(Text)