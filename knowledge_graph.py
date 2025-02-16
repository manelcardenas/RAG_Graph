from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import ChatOllama
from langchain_experimental.graph_transformers import LLMGraphTransformer
from neo4j import GraphDatabase
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def get_llm():
    """Initialize LLM based on environment configuration"""
    model_type = os.getenv("MODEL_TYPE", "openai").lower()
    
    if model_type == "openai":
        return ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4o"),
            temperature=float(os.getenv("MODEL_TEMPERATURE", "0")),
            api_key=os.getenv("OPENAI_API_KEY")
        )
    elif model_type == "ollama":
        return ChatOllama(
            model=os.getenv("OLLAMA_MODEL", "llama2"),
            temperature=float(os.getenv("MODEL_TEMPERATURE", "0"))
        )
    else:
        raise ValueError(f"Unsupported model type: {model_type}")

class Neo4jConnection:
    def __init__(self):
        self.uri = os.getenv("NEO4J_URI")
        self.user = os.getenv("NEO4J_USER")
        self.password = os.getenv("NEO4J_PASSWORD")
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
        
    def close(self):
        self.driver.close()
        
    def query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            return [record for record in result]

# Load the text file
loader = TextLoader("data/dummytext.txt")
docs = loader.load()

# Split the documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(docs)

# Initialize LLM based on configuration
llm = get_llm()
llm_transformer = LLMGraphTransformer(llm=llm)
graph_docs = llm_transformer.convert_to_graph_documents(chunks)

# Initialize Neo4j connection
connection = Neo4jConnection()

try:
    # Clear existing database
    connection.query("MATCH (n) DETACH DELETE n")

    # Create nodes from graph_docs
    for doc in graph_docs:
        for node in doc.nodes:
            node_data = {
                "id": node.id,
                "properties": node.properties
            }
            
            create_node_query = """
            MERGE (n:{label} {{id: $id}})
            SET n += $properties
            """.format(label=node.type)
            
            connection.query(
                create_node_query,
                node_data
            )
        
        # Create relationships
        for rel in doc.relationships:
            rel_data = {
                "source_id": rel.source.id,
                "target_id": rel.target.id,
                "properties": rel.properties
            }
            
            create_rel_query = """
            MATCH (source) WHERE source.id = $source_id
            MATCH (target) WHERE target.id = $target_id
            MERGE (source)-[r:{rel_type}]->(target)
            SET r += $properties
            """.format(rel_type=rel.type)
            
            connection.query(
                create_rel_query,
                rel_data
            )

    # Verify graph creation
    print("\nCreated Nodes:")
    result = connection.query("MATCH (n) RETURN n.id, labels(n)")
    for record in result:
        print(f"ID: {record[0]}, Labels: {record[1]}")

    print("\nCreated Relationships:")
    result = connection.query("MATCH ()-[r]->() RETURN type(r), count(r)")
    for record in result:
        print(f"Type: {record[0]}, Count: {record[1]}")

    print("\nRelationship Details:")
    result = connection.query("""
    MATCH (p)-[r]->(m)
    RETURN p.id, type(r), m.id
    """)
    for record in result:
        print(f"{record[0]} -{record[1]}-> {record[2]}")

finally:
    connection.close()