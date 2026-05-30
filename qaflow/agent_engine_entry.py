from vertexai.preview.reasoning_engines import AdkApp

from qaflow.agent import root_agent

agent_engine = AdkApp(
    agent=root_agent,
    enable_tracing=False,
)
