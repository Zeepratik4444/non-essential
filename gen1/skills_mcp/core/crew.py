import logging
from typing import Any
from pathlib import Path

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import MCPServerAdapter

from core.settings import settings

logger = logging.getLogger(__name__)

@CrewBase
class SkillsCrew:
    """
    Skill-driven CrewAI crew for the MCP Server using MCPServerAdapter (SSE).
    """

    agents_config = "../config/agents.yaml"
    tasks_config = "../config/tasks.yaml"

    def __init__(self) -> None:
        self.llm = LLM(model=settings.LLM_MODEL)
        
        # Configure the MCP Server connection (SSE / streamable-http)
        # Instead of Stdio, we connect to the running server's SSE endpoint.
        self.mcp_adapter = MCPServerAdapter(
            name="SkillsMCPServer",
            server_params={
                "transport": "sse",
                "url": settings.MCP_SSE_URL
            }
        )
        
        logger.info("SkillsCrew initialized for MCP-over-HTTP (SSE) at %s", settings.MCP_SSE_URL)

    @agent
    def skills_operator(self) -> Agent:
        # Load tools from the MCP Server via the adapter
        # This will connect to the SSE endpoint and fetch tool definitions
        mcp_tools = self.mcp_adapter.get_tools()
        
        return Agent(
            config=self.agents_config["skills_operator"],
            tools=mcp_tools,
            llm=self.llm,
            verbose=True,
            memory=True,
            max_iter=30,
        )

    @task
    def execute_task(self) -> Task:
        return Task(
            config=self.tasks_config["execute_task"],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

    def run(self, task_description: str, chat_history: str = "No previous context.", **extra_inputs: Any) -> str:
        inputs = {
            "task_description": task_description,
            "chat_history": chat_history,
            **extra_inputs
        }
        logger.info("Kicking off SkillsCrew (SSE) with inputs: %s", inputs)
        
        result = self.crew().kickoff(inputs=inputs)
        return result.raw
