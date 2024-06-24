from typing import Dict, List

from crewai import Agent

from agentic_blogger.crew.crew import SequentialBloggingCrew
from agentic_blogger.utils.util import PROJECT_PATH


def run(
    inputs: Dict[str, str] = {"topic_name": "", "blog_article": ""},
    selected_agent_list: List[Agent] = [],
) -> str:
    blog_crew = SequentialBloggingCrew().crew(selected_agent_list=selected_agent_list)
    result = blog_crew.kickoff(inputs=inputs)
    return result


if __name__ == "__main__":
    # SequentialBloggingCrew().crew()
    SequentialBloggingCrew().crew(selected_agent_list=["SEO Agent", "Style Agent"])
