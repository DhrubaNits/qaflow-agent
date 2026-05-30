import traceback
import uuid
from pathlib import Path
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from qaflow.agent import create_agent, root_agent

APP_NAME = "qaflow_web_app"
USER_ID = "qa_user"

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"
INDEX_FILE = FRONTEND_DIR / "index.html"

app = FastAPI(
    title="QAFlow Agent Web App",
    description="QAFlow Agent API for UI and Google Cloud Agent Builder integration",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session_service = InMemorySessionService()


class RunRequest(BaseModel):
    prompt: str
    model: Optional[str] = None


class AgentBuilderRunRequest(BaseModel):
    user_request: str
    model: Optional[str] = "gemini-2.5-flash"


async def execute_qaflow_agent(prompt: str, model: Optional[str] = None):
    """
    Common runner used by both:
    1. QAFlow UI endpoint: /api/run
    2. Agent Builder endpoint: /api/agent-builder/run
    """
    if not prompt or not prompt.strip():
        return {
            "success": False,
            "error": "Prompt is empty",
            "details": "Please provide a valid QAFlow instruction.",
        }

    selected_model = model.strip() if model and model.strip() else None
    session_id = str(uuid.uuid4())

    try:
        await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=session_id,
        )

        agent = create_agent(selected_model)

        runner = Runner(
            agent=agent,
            app_name=APP_NAME,
            session_service=session_service,
        )

        message = types.Content(
            role="user",
            parts=[types.Part(text=prompt)],
        )

        final_response_parts = []

        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=session_id,
            new_message=message,
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    text = getattr(part, "text", None)
                    if text:
                        final_response_parts.append(text)

        final_response = "".join(final_response_parts).strip()

        if not final_response:
            final_response = "Agent completed the action, but no text response was returned."

        return {
            "success": True,
            "session_id": session_id,
            "model": getattr(agent, "model", selected_model or "default"),
            "response": final_response,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "details": traceback.format_exc(),
        }


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "app": "QAFlow Agent",
        "default_agent": root_agent.name,
        "default_model": getattr(root_agent, "model", "unknown"),
        "dynamic_model_supported": True,
    }


@app.get("/api/agent-builder/health")
async def agent_builder_health():
    return {
        "status": "ok",
        "app": "QAFlow Agent",
        "integration": "Google Cloud Agent Builder",
        "default_agent": root_agent.name,
        "default_model": getattr(root_agent, "model", "unknown"),
        "dynamic_model_supported": True,
        "endpoint": "/api/agent-builder/run",
    }


@app.get("/")
async def home():
    if not INDEX_FILE.exists():
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "error": "frontend/index.html not found",
            },
        )

    response = FileResponse(INDEX_FILE)
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.post("/api/run")
async def run_agent(request: RunRequest):
    return await execute_qaflow_agent(
        prompt=request.prompt,
        model=request.model,
    )


@app.post("/api/agent-builder/run")
async def run_agent_builder(request: AgentBuilderRunRequest):
    """
    Endpoint for Google Cloud Agent Builder OpenAPI tool integration.
    Agent Builder should call this endpoint with user_request.
    """
    return await execute_qaflow_agent(
        prompt=request.user_request,
        model=request.model,
    )


if FRONTEND_DIR.exists():
    app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")