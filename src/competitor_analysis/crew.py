from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List, Dict, Any
from crewai_tools import ScrapeWebsiteTool
import weave


# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators
# Initialize Weave with your project name
weave.init(project_name="competitor_analysis")
@CrewBase
class CompetitorAnalysis():
    """CompetitorAnalysis crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def web_crawl_specialist(self) -> Agent:
        # config contains: role, goal, backstory
        return Agent(
            config=self.agents_config['web_crawl_specialist'],  # type: ignore
            tools=[ScrapeWebsiteTool()],
        )

    @agent
    def swot_analyst(self) -> Agent:
        # config contains: role, goal, backstory
        return Agent(
            config=self.agents_config['swot_analyst'],  # type: ignore
            tools=[],
        )

    @agent
    def strategy_developer(self) -> Agent:
        # config contains: role, goal, backstory
        return Agent(
            config=self.agents_config['strategy_developer'],  # type: ignore
            tools=[],
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def scrape_competitor_website(self) -> Task:
        # config contains: description, expected_output
        return Task(
            config=self.tasks_config['scrape_competitor_website'],  # type: ignore
            tools=[ScrapeWebsiteTool()],
        )

    @task
    def generate_swot_analysis(self) -> Task:
        # config contains: description, expected_output
        return Task(
            config=self.tasks_config['generate_swot_analysis'],  # type: ignore
            tools=[],
        )

    @task
    def develop_strategic_action_items(self) -> Task:
        # config contains: description, expected_output
        return Task(
            config=self.tasks_config['develop_strategic_action_items'],  # type: ignore
            tools=[],
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the CompetitorAnalysis crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
