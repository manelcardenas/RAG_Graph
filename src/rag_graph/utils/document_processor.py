from langchain_community.document_loaders import TextLoader
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_and_split_documents(file_path, chunk_size=1000, chunk_overlap=200):
    """Load and split documents from a text file.

    Args:
        file_path: Path to the text file
        chunk_size: Size of each document chunk
        chunk_overlap: Overlap between consecutive chunks

    Returns:
        list: List of document chunks
    """
    # Load the text file
    loader = TextLoader(file_path)
    docs = loader.load()

    # Split the documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_documents(docs)


def convert_to_graph_documents(llm, documents):
    """Convert documents to graph documents using LLM.

    Args:
        llm: Language model to use for conversion
        documents: Documents to convert

    Returns:
        list: List of graph documents
    """
    llm_transformer = LLMGraphTransformer(llm=llm)
    return llm_transformer.convert_to_graph_documents(documents)
