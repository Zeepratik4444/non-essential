import logging
from typing import Any

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from src.config.settings import settings
from src.tools import SkillsManagerTool

logger = logging.getLogger(__name__)


@CrewBase
class SkillsCrew:
    """
    Skills-driven CrewAI crew.

    Agents load skill instructions progressively via SkillsManagerTool
    before executing any task — preventing hallucination and ensuring
    every action follows a defined protocol.

    Skills directory is scanned dynamically at runtime — add a new
    skill folder and it is available immediately without code changes.
    """

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self) -> None:
        settings.validate()
        logger.info("SkillsCrew initialized. Skills dir: %s", settings.SKILLS_DIR)

    @agent
    def skills_operator(self) -> Agent:
        return Agent(
            config=self.agents_config["skills_operator"],  # type: ignore[index]
            tools=[SkillsManagerTool()],
            verbose=True,
            memory=True,
            cache=True,
            respect_context_window=True,
            max_iter=25,
            max_retry_limit=3,
        )

    @task
    def execute_task(self) -> Task:
        return Task(
            config=self.tasks_config["execute_task"],  # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )


    def run(self, task_description: str, **extra_inputs: Any) -> str:
        """
        Kick off the crew with a task description.
        Extra inputs are merged and passed to task interpolation.

        Usage:
            result = SkillsCrew().run("Find papers on LLM memory.")
            result = SkillsCrew().run("Analyse data", context="extra detail")
        """
        inputs = {"task_description": task_description, **extra_inputs}
        logger.info("Kicking off SkillsCrew with inputs: %s", inputs)

        result = self.crew().kickoff(inputs=inputs)

        logger.info("SkillsCrew completed. Output length: %d chars", len(result.raw))
        return result.raw
