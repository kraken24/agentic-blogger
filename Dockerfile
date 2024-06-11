FROM python:3.10.14-slim-bookworm
LABEL maintainer="Brijesh Modasara"

# Install Poetry
RUN pip install poetry && poetry config virtualenvs.create false

# Set the working directory in the container
WORKDIR /app

COPY pyproject.toml poetry.lock* /app/
RUN poetry install --no-root --no-interaction && \
    poetry cache clear pypi --all

# Copy necessary files
COPY . /app

EXPOSE 8501

ENTRYPOINT ["poetry", "run", "streamlit", "run", \
    "/app/src/agentic_blogger/app.py", "--server.port=8501", \
    "--server.address=0.0.0.0"]
