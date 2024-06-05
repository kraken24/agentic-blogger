from crew import SequentialBloggingCrew


def run() -> None:
    inputs = {"topic_name": "LLMs in Healthcare"}
    SequentialBloggingCrew().crew().kickoff(inputs=inputs)


if __name__ == "__main__":
    run()
