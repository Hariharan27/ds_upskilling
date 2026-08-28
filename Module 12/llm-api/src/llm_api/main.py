from fastapi import (
    Depends,
    FastAPI,
    Header,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
    BackgroundTasks,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from llm_api.jobs import JobManager
from llm_api.limiter import RateLimiter
from llm_api.dependencies import get_llm_client
from llm_api.sessions import SessionManager
from llm_api.llm import LLMClient
from llm_api.models import (
    ChatRequest,
    ChatResponse,
    HealthResponse,
)


session_manager = SessionManager()
job_manager = JobManager()

app = FastAPI(
    title="LLM API",
    description="A simple production-style API for interacting with an LLM.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

rate_limiter = RateLimiter(
    max_requests=5,
    window_seconds=60,
)

async def get_user_id(
    x_user_id: str = Header(...),
) -> str:
    """Extract the user ID from the request header."""

    return x_user_id


def check_rate_limit(
    user_id: str = Depends(get_user_id),
) -> None:
    if not rate_limiter.is_allowed(user_id):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded.",
        )


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Check whether the API is running."""

    return HealthResponse(status="healthy")



@app.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    user_id: str = Depends(get_user_id),
    llm_client: LLMClient = Depends(get_llm_client),
) -> ChatResponse:

    if not rate_limiter.is_allowed(user_id):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Try again later.",
        )

    conversation_id = request.conversation_id

    if conversation_id is None:
        conversation_id = session_manager.create_session(user_id)

    else:
        session = session_manager.get_session(
            conversation_id,
            user_id,
        )

        if session is None:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found or expired.",
            )

    try:
        response = llm_client.generate_response(
            request.message
        )

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail="LLM service is currently unavailable.",
        ) from exc

    return ChatResponse(
        response=response,
        conversation_id=conversation_id,
    )


@app.post("/chat/stream")
async def chat_stream(
    request: ChatRequest,
    llm_client: LLMClient = Depends(get_llm_client),
):
    """Stream the LLM response using Server-Sent Events."""

    def event_stream():
        try:
            for chunk in llm_client.generate_stream(
                request.message
            ):
                yield f"data: {chunk}\n\n"

            yield "data: [DONE]\n\n"

        except Exception:
            yield (
                "event: error\n"
                "data: LLM service is currently unavailable.\n\n"
            )

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
    )


def get_websocket_llm_client() -> LLMClient:
    return get_llm_client()

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """Handle a simple WebSocket chat connection."""

    await websocket.accept()

    llm_client = get_websocket_llm_client()

    try:
        while True:
            message = await websocket.receive_text()

            try:
                response = llm_client.generate_response(message)

                await websocket.send_text(response)

            except Exception:
                await websocket.send_text(
                    "LLM service is currently unavailable."
                )

    except WebSocketDisconnect:
        print("WebSocket client disconnected.")


def process_job(job_id: str, message: str) -> None:
    """Process a job in the background."""

    job_manager.update_job(
        job_id,
        "processing",
    )

    try:
        llm_client = get_llm_client()

        response = llm_client.generate_response(
            message
        )

        job_manager.update_job(
            job_id,
            "completed",
            response,
        )

    except Exception:
        job_manager.update_job(
            job_id,
            "failed",
        )


@app.post("/jobs")
async def create_background_job(
    request: ChatRequest,
    background_tasks: BackgroundTasks,
):
    """Create an asynchronous background LLM job."""

    job_id = job_manager.create_job()

    background_tasks.add_task(
        process_job,
        job_id,
        request.message,
    )

    return {
        "job_id": job_id,
        "status": "pending",
    }

@app.get("/jobs/{job_id}")
async def get_job_status(job_id: str):
    """Return the current status of a background job."""

    job = job_manager.get_job(job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found.",
        )

    return job