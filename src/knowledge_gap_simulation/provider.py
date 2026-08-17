import os
from typing import TypeVar

from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_exponential

Schema = TypeVar("Schema", bound=BaseModel)


class GoogleProvider:
    def __init__(self, model_name: str) -> None:
        if not os.getenv("GOOGLE_API_KEY"): raise RuntimeError("GOOGLE_API_KEY is required for generation.")
        self.model = ChatGoogleGenerativeAI(model=model_name, temperature=0)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=15), reraise=True)
    def structured(self, prompt: str, schema: type[Schema]) -> Schema:
        return self.model.with_structured_output(schema).invoke(prompt)
