# Neo4j Project

## Overview

This project is a knowledge graph that uses LLMs to create a graph of entities and their relationships.

## Development Setup

### Using `uv` (Recommended)

1. Install dependencies:

   ```bash
   uv pip install .
   ```

2. Install development dependencies:
   ```bash
   uv pip install ".[dev]"
   ```

### Using `pip`

1. Install dependencies:

   ```bash
   pip install .
   ```

2. Install development dependencies:

   ```bash
   pip install ".[dev]"
   ```

3. Lint and format code:
   ```bash
   ruff check . && ruff format .
   ```

## Setup

1. Clone the repository
2. Install the dependencies
3. Run the script

```bash
python knowledge_graph.py
```

## Usage

Run in p:
neo4j browser

```bash
MATCH (n)-[r]->(m)
RETURN n, r, m
```

## Configuration
