# Tutorials

This repo contains comprehensive projects that I went through to understand and apply concepts helpful for the role of ML Engineer and what goes beyond that (data engineering, devops, data-science, etc...)



## Project Structure

Each project covers a certain topic/concept. The project will contain theoretical notes about the tool or the concept, best-practices and a comprehensive project that will need to be implemented, with its bare scaffold and an evaluation criteria as well as a summary of the concept. My task, will be to complete the project.

the project will be structured as follows:
```
.
├── docs/
├── src/
├── tests/
├── .envrc
├── .env.example
├── .python-version
├── poetry.toml
├── pyproject.toml
└── README.md
```

use the following .envrc
```
VIRTUAL_ENV=".venv"
python_version=$(cat .python-version)
layout pyenv $python_version
layout python
[ -d "$VIRTUAL_ENV" ] && \
    [ ! -e "$VIRTUAL_ENV/bin/poetry" ] && \
    pip install poetry && \
    pip install keyrings-google-artifactregistry-auth==1.1.2
dotenv_if_exists .env
```


## Concepts

Here is a list of the current concepts:
- ab-testing
- airflow
- async
- bytewax
- celery-fastapi
- dagster
- dynamic-batching
- feature-store
- great-expectations
- grpc
- langsmith
- llm-fine-tuning
- llm-serving
- multi-agent-orchestration
- process-mining
- pyspark
- qdrant
- ranking
- ray
- recsys
- socket