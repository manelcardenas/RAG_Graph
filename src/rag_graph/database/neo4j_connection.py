import os

from neo4j import GraphDatabase


class Neo4jConnection:
    """Neo4j connection class."""

    def __init__(self):
        """Initialize Neo4j connection."""
        self.uri = os.getenv("NEO4J_URI")
        self.user = os.getenv("NEO4J_USER")
        self.password = os.getenv("NEO4J_PASSWORD")
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))

    def close(self):
        """Close Neo4j connection."""
        self.driver.close()

    def query(self, query, parameters=None):
        """Query Neo4j database."""
        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            return list(result)

    def clear_database(self):
        """Clear all nodes and relationships in the database."""
        return self.query("MATCH (n) DETACH DELETE n")

    def create_node(self, label, node_id, properties):
        """Create a node with the given label, ID and properties."""
        node_data = {"id": node_id, "properties": properties}

        create_node_query = """
        MERGE (n:{label} {{id: $id}})
        SET n += $properties
        """.format(label=label)

        return self.query(create_node_query, node_data)

    def create_relationship(self, source_id, relationship_type, target_id, properties=None):
        """Create a relationship between two nodes."""
        rel_data = {
            "source_id": source_id,
            "target_id": target_id,
            "properties": properties or {},
        }

        create_rel_query = """
        MATCH (source) WHERE source.id = $source_id
        MATCH (target) WHERE target.id = $target_id
        MERGE (source)-[r:{rel_type}]->(target)
        SET r += $properties
        """.format(rel_type=relationship_type)

        return self.query(create_rel_query, rel_data)
