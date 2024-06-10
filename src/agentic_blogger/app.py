import time

import pandas as pd
import streamlit as st
from main import run
from util import PROJECT_PATH

st.set_page_config(
    page_title="LLM-based Blogging",
    page_icon="",
)
ss = st.session_state

for var in ["blog", "user_topic", "user_blog"]:
    if var not in st.session_state:
        st.session_state.blog = None


def read_file(file_path: str) -> str:
    with open(file_path, "rb") as file:
        return file.read()


def create_title_container() -> None:
    with st.container():
        st.title("Agentic Blogger")

    return None


def create_agent_selection_sidebar() -> None:
    with st.sidebar:
        st.write(":control_knobs: Select required LLM-Agents:")
        writer_agent = st.checkbox("Writer Agent", value=True, disabled=True)
        editor_agent = st.checkbox("Editor Agent", value=True, disabled=True)
        research_agent = st.checkbox("Research Agent", value=True)
        seo_agent = st.checkbox("SEO Agent", value=True)
        style_agent = st.checkbox("Style Agent", value=True)
        plagiarism_agent = st.checkbox("Plagiarism Agent", value=True)

        with st.expander(label="Agent Workflow"):
            st.write(":control_knobs:")
            st.write(":control_knobs:")
            st.write(":control_knobs:")
            st.write(":control_knobs:")
            st.write(":control_knobs:")

    return None


def create_crew_container() -> None:
    with st.container():
        ss["user_topic"] = st.text_input(
            "Enter your blog topic:", placeholder="What do you want to write about?"
        )

        ss["user_blog"] = st.text_area("Write your blog here:", value=None)

        if st.button("Work Your Squad!"):
            if not ss["user_topic"] and not ss["user_blog"]:
                st.error("Please enter a topic or provide a blog input!")
            else:
                with st.spinner(text="Processing..."):
                    ss["blog"] = run(
                        inputs={
                            "topic_name": ss["user_topic"] + ss["user_blog"],
                            "user_blog": ss["user_blog"],
                        }
                    )
    return None


def display_blog_container() -> None:
    if not ss["blog"]:
        return None

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

    with st.container():
        st.write(ss["blog"])

    return None


def app() -> None:
    create_title_container()
    create_agent_selection_sidebar()
    create_crew_container()
    display_blog_container()

    return None


if __name__ == "__main__":
    # poetry run streamlit run src/agentic_blogger/app.py
    app()
