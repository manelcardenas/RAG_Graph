from dotenv import load_dotenv

from rag_graph.database.neo4j_connection import Neo4jConnection
from rag_graph.models.llm import get_llm
from rag_graph.utils.document_processor import convert_to_graph_documents, load_and_split_documents


class GraphBuilder:
    """Main class for building knowledge graphs from documents."""

    def __init__(self):
        """Initialize GraphBuilder with necessary components."""
        # Load environment variables
        load_dotenv()

        # Initialize components
        self.connection = Neo4jConnection()
        self.llm = get_llm()

    def build_graph(self, file_path, clear_existing=True):
        """Build a knowledge graph from the given text file.

        Args:
            file_path: Path to the text file
            clear_existing: Whether to clear existing data in the database

        Returns:
            dict: Statistics about the created graph
        """
        # Process document
        chunks = load_and_split_documents(file_path)
        graph_docs = convert_to_graph_documents(self.llm, chunks)

        try:
            # Clear existing database if requested
            if clear_existing:
                self.connection.clear_database()

            # Create nodes and relationships
            for doc in graph_docs:
                self._add_document_to_graph(doc)

            # Return graph statistics
            return self._collect_graph_statistics()

        finally:
            self.connection.close()

    def _add_document_to_graph(self, doc):
        """Add a graph document to the Neo4j database.

        Args:
            doc: Graph document to add
        """
        # Create nodes
        for node in doc.nodes:
            self.connection.create_node(node.type, node.id, node.properties)

        # Create relationships
        for rel in doc.relationships:
            self.connection.create_relationship(rel.source.id, rel.type, rel.target.id, rel.properties)

    def _collect_graph_statistics(self):
        """Collect statistics about the created graph.

        Returns:
            dict: Graph statistics
        """
        node_count = self.connection.query("MATCH (n) RETURN count(n) as count")[0][0]
        rel_count = self.connection.query("MATCH ()-[r]->() RETURN count(r) as count")[0][0]

        node_types = self.connection.query("MATCH (n) RETURN DISTINCT labels(n) as type, count(*) as count")

        rel_types = self.connection.query("MATCH ()-[r]->() RETURN DISTINCT type(r) as type, count(*) as count")

        return {
            "node_count": node_count,
            "relationship_count": rel_count,
            "node_types": [(r[0], r[1]) for r in node_types],
            "relationship_types": [(r[0], r[1]) for r in rel_types],
        }
