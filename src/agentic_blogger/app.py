import time

import pandas as pd
import streamlit as st

from agentic_blogger.main import run
from agentic_blogger.utils.util import PROJECT_PATH, ArticleDetails

st.set_page_config(
    page_title="Agentic Blogger",
    page_icon="🧠",
)
ss = st.session_state
if "blog" not in st.session_state:
    st.session_state.blog = None


def read_file(file_path: str) -> str:
    with open(file_path, "rb") as file:
        return file.read()


def create_title_container() -> None:
    with st.container():
        st.title("Agentic Blogger")

    return None


def crew_container() -> None:
    with st.container():
        user_input_topic = st.text_input(
            "Enter your blog topic:", placeholder="What do you want to write about?"
        )

        if st.button("Ask Crew"):
            if not user_input_topic:
                st.error("Please enter a topic!")
            else:
                with st.spinner(text="Processing..."):
                    ss["blog"] = run(inputs={"topic_name": user_input_topic})

    if ss["blog"]:
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
    crew_container()

    return None


if __name__ == "__main__":
    # poetry run streamlit run src/agentic_blogger/app.py
    app()
