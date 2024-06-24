import time
from textwrap import dedent

import pandas as pd
import streamlit as st

from agentic_blogger.main import run
from agentic_blogger.utils.util import PROJECT_PATH, ArticleDetails

st.set_page_config(
    page_title="LLM-based Blogging",
    page_icon="",
)
ss = st.session_state

for var in ["blog", "user_topic", "user_blog", "selected_agents", "ai_blog"]:
    if var not in st.session_state:
        st.session_state[var] = None


def read_file(file_path: str) -> str:
    with open(file_path, "rb") as file:
        return file.read()


def create_title_container() -> None:
    with st.container():
        st.title("Agentic Blogger")

    return None


def create_agent_selection_sidebar() -> None:
    with st.sidebar:
        st.write(":notes: Select required LLM-Agents:")
        research_agent = st.checkbox("Research Agent", value=False)
        writer_agent = st.checkbox("Writer Agent", value=False)
        seo_agent = st.checkbox("SEO Agent", value=False)
        grammar_style_agent = st.checkbox("Style Agent", value=False)
        fact_checker_agent = st.checkbox("Fact Checker Agent", value=False)
        visual_content_agent = st.checkbox("Visual Content Agent", value=False)

    selected_agents = []

    if research_agent:
        selected_agents.append("Research Agent")
    if writer_agent:
        selected_agents.append("Writer Agent")
    if seo_agent:
        selected_agents.append("SEO Agent")
    if grammar_style_agent:
        selected_agents.append("Style Agent")
    if fact_checker_agent:
        selected_agents.append("Fact Checker Agent")
    if visual_content_agent:
        selected_agents.append("Visual Content Agent")

    ss["selected_agents"] = selected_agents

    return None


def display_blog_files() -> None:
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            file_name = "articles.json"
            file_path = PROJECT_PATH / "output" / "articles.json"
            file_data = read_file(file_path)
            st.download_button(
                label="Source Files",
                data=file_data,
                file_name=file_name,
                mime="application/json",
                help="Download the file containing sources for the article",
            )

        with col2:
            file_name = "initial draft.md"
            file_path = PROJECT_PATH / "output" / "initial_draft.md"
            file_data = read_file(file_path)
            st.download_button(
                label="Initial Draft",
                data=file_data,
                file_name=file_name,
                mime="text/markdown",
                help="Initial draft by the writer",
            )
        with col3:
            file_name = "final draft.md"
            file_path = PROJECT_PATH / "output" / "final_draft.md"
            file_data = read_file(file_path)
            st.download_button(
                label="Final Draft",
                data=file_data,
                file_name=file_name,
                mime="text/markdown",
                help="Final article by the editor",
            )

    return None


def create_blogging_container() -> None:
    with st.container():
        ss["user_topic"] = st.text_input(
            "Enter your blog topic:", placeholder="What do you want to write about?"
        )
        col1, col2 = st.columns(2)
        with col1:
            ss["user_blog"] = st.text_area(
                "Original Blog",
                value=dedent(
                    "The citye parkk is a grate plaice for familys to spennd time \
                    togethur and enjoing the outdors, it has a playgrouns, picknik areas, \
                    and walking trales. Howevver, itt is ofen crowdd especially on weakends \
                    wen evryone wants to enjooy the nice wether and there can bee a lot of noize. \
                    The parkk is well-maintayned, but sum of the benches are in need of reppair \
                    and ther is somtimes litter that hasnt been picked upp. Despit these minur isues, \
                    itt still a populer spot for bothe locals and vistors alike."
                ),
                height=500,
            )

        with col2:
            ss["ai_blog"] = st.text_area(
                "Updated Blog", value=st.session_state["ai_blog"], height=500
            )

        if st.button("Work Your Squad!"):
            if not ss["user_blog"]:
                st.error("Please provide a blog input!")
            elif not ss["selected_agents"]:
                st.error("Please select required agents")
            else:
                with st.spinner(text="Processing..."):
                    time.sleep(5)
                    ss["ai_blog"] = run(
                        inputs={
                            "topic_name": ss["user_topic"],
                            "blog_article": ss["user_blog"],
                        },
                        selected_agent_list=ss["selected_agents"],
                    )

        if ss["ai_blog"]:
            display_blog_files()

    return None


def app() -> None:
    create_title_container()
    create_agent_selection_sidebar()
    create_blogging_container()

    return None


if __name__ == "__main__":
    # poetry run streamlit run src/agentic_blogger/app.py
    app()
