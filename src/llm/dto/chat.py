from typing import List, Optional

from pydantic import BaseModel
from typing_extensions import NotRequired, TypedDict


class ChatCompletionMessage(TypedDict):
    role: str
    content: Optional[str]
    user: NotRequired[str]
    tool_calls: NotRequired[List]


class LLMChatDto(BaseModel):
    prompt: str
    system_prompt: Optional[str] = None
    chat_history: Optional[List["ChatCompletionMessage"]] = []
class RAGChatDto(BaseModel):
    prompt: str
    collection_name: str
    system_prompt: Optional[str] = None
    chat_history: Optional[List["ChatCompletionMessage"]] = []