# Enterprise AI Assistant

A production-grade Enterprise AI Assistant built incrementally as a
Generative AI capstone project.

## Current Scope

Task 01 establishes the application foundation:

- Canonical project structure
- FastAPI application
- Explicit bootstrap/composition boundary
- Typed environment configuration
- Health endpoint

The following capabilities are intentionally not implemented yet:

- LLM integrations
- Embeddings
- Vector databases
- RAG
- Tools
- Agents
- Memory
- Enterprise integrations

## Requirements

- Python 3.11+

## Local Setup

Create the virtual environment:

```bash
python3.11 -m venv .venv
```

## Activate it:
```
source .venv/bin/activate
```
## Upgrade pip:
```
python -m pip install --upgrade pip
```
## Install the project and its dependencies:
```
pip install -e .
```
## Create the local environment configuration:
```
cp .env.example .env
```
## Run

Start the FastAPI application:
```
uvicorn app.bootstrap.application:app --reload
```

The application runs at:
```
http://127.0.0.1:8000
```


## Health Check

Call the health endpoint:

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "ok",
  "application": "Enterprise AI Assistant",
  "version": "0.1.0",
  "environment": "development"
}
```

## API Documentation

FastAPI automatically exposes Swagger UI at:

```text
http://127.0.0.1:8000/docs
```

The `/health` endpoint can also be tested directly from Swagger UI.

## Architecture

The application follows the dependency direction:

```text
Presentation
     ↓
Application
     ↓
Domain
```

Infrastructure implements contracts required by the inner layers.

The bootstrap layer acts as the application composition root and is responsible for assembling the FastAPI application and registering its routes.

## Configuration

Application configuration is managed using Pydantic Settings and environment variables.

The repository contains:

```text
.env.example
```

as the safe configuration template.

Local configuration is stored in:

```text
.env
```

The `.env` file is excluded from Git and must not contain secrets that are committed to source control.

## Task 01 Boundaries

Task 01 intentionally does not implement:

* LLM providers
* Embeddings
* Vector stores
* Document ingestion
* RAG
* Tools
* Agents
* LangGraph
* Memory
* Multi-agent orchestration
* Enterprise API integrations

These capabilities will be introduced incrementally in later tasks when required by the capstone roadmap.

Task 01 establishes only the production application foundation required for those future capabilities.
