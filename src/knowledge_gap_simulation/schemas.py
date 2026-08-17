from pydantic import BaseModel, Field


class Annotation(BaseModel):
    subject_area: str
    difficulty: int = Field(ge=1, le=5)
    reasoning: str


class ConceptItem(BaseModel):
    name: str
    description: str


class ConceptExtraction(BaseModel):
    concepts: list[ConceptItem] = Field(min_length=1, max_length=3)


class SimulationResponse(BaseModel):
    answer: str
    reasoning: str
    confidence: float = Field(ge=0, le=1)


class NaiveAnswer(BaseModel):
    expected_answer: str
    justification: str


class TheoryOfMindResponse(BaseModel):
    answer: str
    reasoning: str
