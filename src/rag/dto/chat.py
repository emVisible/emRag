from pydantic import BaseModel, EmailStr, Field

class ChatDto(BaseModel):
    prompt: str
    system_prompt: str
    chat_history: list[str]

