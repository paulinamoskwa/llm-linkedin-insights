from openai import OpenAI
from pydantic import BaseModel

from src.system_msgs import *


MODEL_NAME = "gpt-4.1-nano-2025-04-14"
API_KEY = ""


class LanguagesRequirements(BaseModel):
    required_languages: list[str]
    preferable_languages: list[str]


class LLM:
    def __init__(self, model_name: str = MODEL_NAME):
        self.model_name = model_name
        self.client = OpenAI(api_key=API_KEY)

    def extract_skills(self, content: str) -> str:
        response = self.client.responses.create(
            model=MODEL_NAME,
            input=[
                {"role": "system", "content": EXTRACT_SKILLS_MSG},
                {"role": "user", "content": content}
            ]
        )
        return response.output_text

    def extract_languages_requirements(self, content: str) -> LanguagesRequirements:
        response = self.client.responses.parse(
            model=MODEL_NAME,
            input=[
                {"role": "system", "content": EXTRACT_LANGUAGE_REQUIREMENTS_MSG},
                {"role": "user", "content": content}
            ],
            text_format=LanguagesRequirements,
        )
        return response.output_parsed

    def detect_text_language(self, content: str) -> str:
        response = self.client.responses.parse(
            model=MODEL_NAME,
            input=[
                {"role": "system", "content": DETECT_TEXT_LANGUAGE_MSG},
                {"role": "user", "content": content}
            ],
        )
        return response.output_text

    def summarize_collection_of_skills(self, content: str) -> str:
        response = self.client.responses.create(
            model=MODEL_NAME,
            input=[
                {"role": "system", "content": SUMMARIZE_ALL_SKILLS_MSG},
                {"role": "user", "content": content}
            ]
        )
        return response.output_text