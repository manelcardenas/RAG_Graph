import argparse
import os

from rag_graph.graph_builder import GraphBuilder


def main():
    """Entry point for the rag-graph command."""
    parser = argparse.ArgumentParser(description="RAG Graph - Knowledge Graph tool using Neo4j and LLMs")

    parser.add_argument(
        "--file",
        "-f",
        type=str,
        default="data/dummytext.txt",
        help="Path to the text file to process",
    )

    parser.add_argument(
        "--keep-existing",
        "-k",
        action="store_true",
        help="Keep existing data in the database (default: clear everything)",
    )

    parser.add_argument(
        "--model-type",
        "-m",
        type=str,
        choices=["openai", "ollama"],
        help="Type of LLM to use (openai or ollama). Overrides MODEL_TYPE in .env",
    )

    args = parser.parse_args()

    print(f"Processing file: {args.file}")
    print(f"Keep existing data: {args.keep_existing}")

    # If model type is specified, override environment variable
    if args.model_type:
        os.environ["MODEL_TYPE"] = args.model_type
        print(f"Using model type: {args.model_type}")
    else:
        print(f"Using model type from .env: {os.getenv('MODEL_TYPE', 'openai')}")

    try:
        builder = GraphBuilder()
        stats = builder.build_graph(
            file_path=args.file,
            clear_existing=not args.keep_existing,
        )

        print("\nGraph created successfully!")
        print(f"Nodes: {stats['node_count']}")
        print(f"Relationships: {stats['relationship_count']}")

        print("\nNode types:")
        for node_type, count in stats["node_types"]:
            print(f"  {node_type}: {count}")

        print("\nRelationship types:")
        for rel_type, count in stats["relationship_types"]:
            print(f"  {rel_type}: {count}")

    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    main()
