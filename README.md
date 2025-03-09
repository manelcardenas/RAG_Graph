# Rag Graph Project

## Overview

This project is a knowledge graph that uses LLMs to create a graph of entities and their relationships.

## Features

- Extraction of entities and relationships from text using LLMs
- Storage of knowledge in Neo4j graph database
- Query capabilities through Neo4j's Cypher query language

## Project Structure

```
project_root/
├── src/              # Source code
│   ├── rag_graph/    # Main package
│   │   ├── database/ # Database operations
│   │   ├── models/   # LLM and graph models
│   │   └── utils/    # Utility functions
│   └── main.py       # Alternative entry point
├── data/             # Data files
│   └── dummytext.txt # Sample data
└── setup.sh          # Setup script
```

## Development Setup

### Prerequisites

- Python 3.11 or higher
- Neo4j database (local or cloud)
- OpenAI API key (or other supported LLM API)

### Quick Setup (Recommended)

Run the setup script to create a virtual environment and install all dependencies:

```bash
./setup.sh
```

### Manual Setup

1. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

2. Activate the virtual environment:

   ```bash
   source .venv/bin/activate
   ```

3. Install the package with development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

### Using `uv` (Faster Alternative)

1. Create a virtual environment and install dependencies:
   ```bash
   uv venv && source .venv/bin/activate && uv pip install -e ".[dev]"
   ```

### Set up pre-commit hooks (optional):

```bash
pre-commit install
```

## Environment Configuration

1. Copy the example environment file:

   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your configuration:

   ```
   NEO4J_URI=bolt://localhost:7687
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=your_password

   # Choose your LLM provider
   MODEL_TYPE=openai  # or ollama

   # For OpenAI
   OPENAI_API_KEY=your_api_key
   OPENAI_MODEL=gpt-4o

   # For Ollama
   OLLAMA_MODEL=llama2
   ```

## Usage

### Command Line

After installation, you can use the `rag-graph` command:

```bash
rag-graph
```

## Querying the Neo4j Database

Open Neo4j Browser and run:

```cypher
MATCH (n)-[r]->(m)
RETURN n, r, m
```

## Development

### Code Formatting and Linting

```bash
ruff check . && ruff format .
```
