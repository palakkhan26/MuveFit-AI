from typing import List, Optional
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    user_id: int = Field(..., description="ID of the user interacting with the coach")
    message: str = Field(..., min_length=1, description="User's query or prompt")


class ChatResponse(BaseModel):
    answer: str = Field(..., description="AI-generated coaching response")
    context_used: List[str] = Field(
        default_factory=list,
        description="List of context sources retrieved for this response"
    )