from typing import Dict

from agentic_blogger.crew.crew import SequentialBloggingCrew
from agentic_blogger.utils.util import PROJECT_PATH


def run(inputs: Dict[str, str] = {"topic_name": "LLMs in Healthcare"}) -> str:
    result = SequentialBloggingCrew().crew().kickoff(inputs=inputs)
    return result


if __name__ == "__main__":
    topic_name = input(
        "Enter the topic name (or leave blank for default 'LLMs in Healthcare'): "
    )
    if not topic_name:
        inputs = {"topic_name": "LLMs in Healthcare"}
    else:
        inputs = {"topic_name": topic_name}

    # result = run(inputs=inputs)
    SequentialBloggingCrew().crew()
