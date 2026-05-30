import vertexai
from vertexai import agent_engines

from qaflow.agent_engine_entry import agent_engine

PROJECT_ID = "qaflow-agent"
LOCATION = "us-central1"
DISPLAY_NAME = "qaflow-agent-sdk-runtime-v2"

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
    staging_bucket="gs://qaflow-agent-staging-512657306508",
)

remote_agent = agent_engines.create(
    agent_engine=agent_engine,
    display_name=DISPLAY_NAME,
    description="QAFlow Agent Runtime SDK deployment with remote MongoDB MCP.",
    requirements=[
        "google-adk==1.34.1",
        "google-cloud-aiplatform[agent_engines]==1.154.0",
        "google-genai==1.75.0",
        "python-dotenv==1.0.1",
        "mcp==1.27.2",
        "cloudpickle==3.1.2",
        "pydantic==2.12.5",
    ],
    extra_packages=[
        "qaflow",
    ],
    env_vars={
        "QAFLOW_MODEL": "gemini-2.5-flash",
        "GOOGLE_GENAI_USE_VERTEXAI": "TRUE",
        "MONGODB_MCP_URL": "https://mongodb-mcp-server-512657306508.us-central1.run.app",
        "GOOGLE_CLOUD_AGENT_ENGINE_ENABLE_TELEMETRY": "false",
        "OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT": "false",
    },
    min_instances=1,
    max_instances=1,
    resource_limits={
        "cpu": "2",
        "memory": "4Gi",
    },
)

print("Deployment finished.")
print("Resource name:", remote_agent.resource_name)
