from typing import List

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import tool
from langchain.agents import Tool
from langchain_community.llms import Ollama
from langchain_community.tools import DuckDuckGoSearchRun

from agentic_blogger.utils.util import PROJECT_PATH, ArticleDetails

OUTPUT_DIR = PROJECT_PATH / "output"


@CrewBase
class SequentialBloggingCrew:
    agents_config = PROJECT_PATH / "config/agents.yaml"
    tasks_config = PROJECT_PATH / "config/tasks.yaml"

    def __init__(self) -> None:
        self.llama3 = Ollama(
            base_url="http://localhost:11434",
            model="llama3",
            temperature=0,
        )
        self.search_tool = DuckDuckGoSearchRun()
        self.research_agent = False
        # Tool(
        #     name="Intermediate Answer",
        #     func=DuckDuckGoSearchRun().run,
        #     description="Useful for search-based queries",
        # )

    @agent
    def blog_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["researcher_agent"],
            llm=self.llama3,
        )

    @agent
    def blog_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["writer_agent"],
            llm=self.llama3,
        )

    @agent
    def editor_in_chief(self) -> Agent:
        return Agent(
            config=self.agents_config["chief_editor_agent"],
            llm=self.llama3,
        )

    @task
    def research_blog(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"],
            agent=self.blog_researcher(),
            output_json=ArticleDetails,
            output_file=(OUTPUT_DIR / "articles.json").as_posix(),
            tools=[self.search_tool],
        )

    @task
    def write_blog(self) -> Task:
        return Task(
            config=self.tasks_config["write_task"],
            agent=self.blog_writer(),
            output_file=(OUTPUT_DIR / "initial_draft.md").as_posix(),
        )

    @task
    def refine_blog(self) -> Task:
        return Task(
            config=self.tasks_config["chief_editor_task"],
            agent=self.editor_in_chief(),
            output_file=(OUTPUT_DIR / "final_draft.md").as_posix(),
        )

    @crew
    def crew(
        self,
        autoselect: bool = True,
        selected_agents: List[str] = [
            "Content Writer",
            "Editor-in-Chief",
        ],
    ) -> Crew:
        """Create the Blogging Crew

        Process Flow :
        - Research Blog
        - Write Blog
        - Refine Blog
        """
        if not autoselect:
            print("?" * 100)
            print(self.agents[0])
            all_agents = {agent.role: agent for agent in self.agents}
            from pprint import pprint

            pprint(all_agents)
            self.agents = [all_agents[role] for role in selected_agents]
            print("#" * 100)
            print(self.agents)

            if self.research_agent:
                self.agents += [self.research_agent]
                self.tasks += [self.research_blog]

            return Crew(
                agents=self.agents,
                tasks=self.tasks,
                process=Process.sequential,
                verbose=2,
            )

        return Crew(
            # automatically provides a list due to decorators
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=2,
        )
