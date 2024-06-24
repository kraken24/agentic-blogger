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
        self.agent_task_dict = {}
        self.search_tool = DuckDuckGoSearchRun()

    @agent
    def researcher_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["researcher_agent"],
            llm=self.llama3,
        )

    @agent
    def writer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["writer_agent"],
            llm=self.llama3,
        )

    @agent
    def fact_checker_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["fact_checker_agent"],
            llm=self.llama3,
        )

    @agent
    def visual_content_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["visual_content_agent"],
            llm=self.llama3,
        )

    @agent
    def seo_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["seo_agent"],
            llm=self.llama3,
        )

    @agent
    def grammar_style_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["grammar_style_agent"],
            llm=self.llama3,
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"],
            agent=self.researcher_agent(),
            output_json=ArticleDetails,
            output_file=(OUTPUT_DIR / "articles.json").as_posix(),
            tools=[self.search_tool],
        )

    @task
    def writing_task(self) -> Task:
        return Task(
            config=self.tasks_config["writing_task"],
            agent=self.writer_agent(),
            output_file=(OUTPUT_DIR / "final_draft_writer.md").as_posix(),
        )

    @task
    def fact_checking_task(self) -> Task:
        return Task(
            config=self.tasks_config["fact_checking_task"],
            agent=self.fact_checker_agent(),
            output_file=(OUTPUT_DIR / "final_draft_fact.md").as_posix(),
        )

    @task
    def visual_content_task(self) -> Task:
        return Task(
            config=self.tasks_config["visual_content_task"],
            agent=self.visual_content_agent(),
            output_file=(OUTPUT_DIR / "final_draft_vis.md").as_posix(),
        )

    @task
    def seo_task(self) -> Task:
        return Task(
            config=self.tasks_config["seo_task"],
            agent=self.seo_agent(),
            output_file=(OUTPUT_DIR / "final_draft.md").as_posix(),
        )

    @task
    def grammar_style_task(self) -> Task:
        return Task(
            config=self.tasks_config["grammar_style_task"],
            agent=self.grammar_style_agent(),
            output_file=(OUTPUT_DIR / "final_draft.md").as_posix(),
        )

    @crew
    def crew(
        self,
        selected_agent_list: List[Agent] = [],
    ) -> Crew:
        self.agent_task_dict = {
            "Research Agent": [self.researcher_agent(), self.research_task()],
            "Writer Agent": [self.writer_agent(), self.writing_task()],
            "SEO Agent": [self.seo_agent(), self.seo_task()],
            "Style Agent": [self.grammar_style_agent(), self.grammar_style_task()],
            "Fact Checker Agent": [
                self.fact_checker_agent(),
                self.fact_checking_task(),
            ],
            "Visual Content Agent": [
                self.visual_content_agent(),
                self.visual_content_task(),
            ],
        }
        agent_list, task_list = [], []
        if selected_agent_list:
            for agent in selected_agent_list:
                agent_list.append(self.agent_task_dict[agent][0])
                task_list.append(self.agent_task_dict[agent][1])
        print(agent_list)
        print("#" * 100)
        print(task_list)

        return Crew(
            agents=self.agents if not agent_list else agent_list,
            tasks=self.tasks if not task_list else task_list,
            process=Process.sequential,
            full_output=True,
            verbose=2,
            output_log_file="./crew_logs.txt",
        )
