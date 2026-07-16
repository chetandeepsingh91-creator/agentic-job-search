import json

from services.prompt_service import load_prompt
from services.llm_service import call_llm


class ProfileExtractor:

    @staticmethod
    def extract(resume_text):

        prompt = load_prompt(
            "profile_extraction_prompt.md",
            resume=resume_text
        )

        response = call_llm(prompt)

        response = response.replace("```json", "")
        response = response.replace("```", "")

        return json.loads(response)