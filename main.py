from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from chatbot import generate_chat_response
from models import ChatRequest, ChatResponse

app = FastAPI(
    title="MuveFit AI Coach API",
    description="Context-aware AI coach for MuveFit workout analysis",
)

# Enable CORS for hackathon development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    """Health check endpoint."""
    return {"status": "MuveFit AI Coach API is running"}


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    """Process a user query with context-aware movement analysis coaching."""
    try:
        result = generate_chat_response(
            user_id=request.user_id,
            message=request.message,
        )
        return ChatResponse(**result)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing the chat request: {str(exc)}",
        )