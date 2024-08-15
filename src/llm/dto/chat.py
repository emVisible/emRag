from typing import Optional, List
from pydantic import BaseModel

class ChatDto(BaseModel):
    prompt: str
    system_prompt: Optional[str]=None
    chat_history: Optional[List[str]]=[]