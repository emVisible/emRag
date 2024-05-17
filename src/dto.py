from pydantic import BaseModel, EmailStr, Field


class CompletionDto(BaseModel):
    prompt: str
