from pydantic import BaseModel


class DynamicPrompt(BaseModel):
    raw_question: str
