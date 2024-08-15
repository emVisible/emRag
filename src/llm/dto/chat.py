from typing import List, Optional

from pydantic import BaseModel
from typing_extensions import NotRequired, TypedDict


class ChatCompletionMessage(TypedDict):
    role: str
    content: Optional[str]
    user: NotRequired[str]
    tool_calls: NotRequired[List]


class ChatDto(BaseModel):
    prompt: str
    system_prompt: Optional[str] = None
    chat_history: Optional[List["ChatCompletionMessage"]] = []