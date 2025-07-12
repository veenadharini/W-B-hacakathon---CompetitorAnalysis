from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool

@CrewBase
class ConfiguringAThreeAgentCompetitiveIntelligenceCrewCrew():
    """ConfiguringAThreeAgentCompetitiveIntelligenceCrew crew"""

    @agent
    def web_crawl_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['web_crawl_specialist'],
            tools=[ScrapeWebsiteTool()],
        )

    @agent
    def swot_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['swot_analyst'],
            tools=[],
        )

    @agent
    def strategy_developer(self) -> Agent:
        return Agent(
            config=self.agents_config['strategy_developer'],
            tools=[],
        )


    @task
    def scrape_competitor_website(self) -> Task:
        return Task(
            config=self.tasks_config['scrape_competitor_website'],
            tools=[ScrapeWebsiteTool()],
        )

    @task
    def generate_swot_analysis(self) -> Task:
        return Task(
            config=self.tasks_config['generate_swot_analysis'],
            tools=[],
        )

    @task
    def develop_strategic_action_items(self) -> Task:
        return Task(
            config=self.tasks_config['develop_strategic_action_items'],
            tools=[],
        )


    @crew
    def crew(self) -> Crew:
        """Creates the ConfiguringAThreeAgentCompetitiveIntelligenceCrew crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
