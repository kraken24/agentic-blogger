# Multi-Agent LLM System for Blogging

Multi-Agent LLM System for Blogging using Crew AI

## Getting Started

To set up your local development environment, please run:

    poetry install

Behind the scenes, this creates a virtual environment and installs `agentic_blogger` along with its dependencies into a new virtualenv.
Whenever you run `poetry run <command>`, that `<command>` is actually run inside the virtualenv managed by poetry.

You can now import functions and classes from the module with `import agentic_blogger`.

## Multi-Agent System for Blog Writing

Large Language Models (LLMs) have revolutionized the field of Natural Language Processing (NLP) in recent years. The models, such as GPT4,Llama, BERT, RoBERTa, and XLNet, are trained on vast amounts of text data and can perform a wide range of NLP tasks with unprecedented accuracy. At their core, LLMs are powerful language understanding machines that can be fine-tuned for specific applications like question answering, sentiment analysis, and text generation.

**Agentic Systems with CrewAI**

I recently studied about the multi-agent framework by [Crew AI](https://www.crewai.com) so I wanted to test how effective it is in utilizing its various capabilities to write a blog by simply providing it with a topic for the blog article. In this repository, you will find the first implementation of the multi-agent system to write a blog.

The multi-agent system comprises of four important parts:
1. `Agent`: An agent is an autonomous unit programmed to perform tasks, make decisions, and communicate with other agents.
2. `Task`: Tasks are specific assignments completed by agents. They provide all necessary details for execution, such as a description, the agent responsible, required tools, and more, facilitating a wide range of action complexities.
3. `Crew`: A crew in crewAI represents a collaborative group of agents working together to achieve a set of tasks. Each crew defines the strategy for task execution, agent collaboration, and the overall workflow.
4. `Process`: It is the strategy to complete a given task, similar to project management in human teams. It could be sequential, hierarchial or consensual execution style.

**Multi-Agent System Code Overview**

- `config`: Contains the definitions for `Agents` and `Tasks`
- `output`: Contains the output of the multi-agent system. It contains the final blog article.
- `src`: Contains the source code for the multi-agent system.
- `src/main.py`: Update the topic in line 5 `inputs = {"topic_name": "LLM agents in production systems"}`

To execute the code, run the following command in the terminal: `poetry run python src/agentic_blogger/main.py`. This will run the multi-agent system to generate a blog article for you.

## Contact

Brijesh Modasara (kraken2404@gmail.com)

## License

© Brijesh Modasara
