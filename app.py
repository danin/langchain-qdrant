"""
Qdrant-Based Document Retrieval Script

This script performs the following tasks:
1. Connects to a Qdrant vector database.
2. Uses a Hugging Face embedding model (`BAAI/bge-large-en`) for similarity-based search.
3. Executes a similarity search query in Qdrant to retrieve the most relevant documents.
4. Displays the retrieved results along with their similarity scores.

Requirements:
- Qdrant must be running locally (`docker run -p 6333:6333 qdrant/qdrant`).
- Required dependencies: langchain, qdrant-client, langchain-community, langchain-huggingface.
"""

# Import necessary modules
from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings import HuggingFaceEmbeddings
from qdrant_client import QdrantClient

# Constants
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "gpt_db"
QUERY_TEXT = "What are some limitations of GPT-4?"

def initialize_embeddings():
    """Loads Hugging Face BGE embeddings model for vector search."""
    print("Initializing embedding model...")
    return HuggingFaceEmbeddings(
        model_name="BAAI/bge-large-en",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': False}
    )

def connect_to_qdrant():
    """Initializes and connects to the Qdrant vector database client."""
    print(f"Connecting to Qdrant at {QDRANT_URL}...")
    qdrant_client = QdrantClient(
        url=QDRANT_URL,
        prefer_grpc=False,
    )
    print("✅ Connected to Qdrant successfully!")
    return qdrant_client

def search_qdrant(qdrant_client, embeddings, query_text, top_k=5):
    """Performs similarity search on Qdrant and returns the top results."""
    print(f"Performing similarity search for query: '{query_text}'")

    # Connect Qdrant to LangChain's Qdrant wrapper
    db = Qdrant(
        client=qdrant_client,
        embeddings=embeddings,
        collection_name=COLLECTION_NAME
    )

    # Execute similarity search
    results = db.similarity_search_with_score(query=query_text, k=top_k)

    print("🔍 Search completed! Displaying results:\n")
    for doc, score in results:
        print({
            'score': score,
            'metadata': doc.metadata,
            'content': doc.page_content
        })

# Execution Flow
if __name__ == "__main__":
    # Initialize embeddings
    embeddings = initialize_embeddings()

    # Connect to Qdrant
    qdrant_client = connect_to_qdrant()

    # Perform similarity search and display results
    search_qdrant(qdrant_client, embeddings, QUERY_TEXT)

    print("🚀 Document retrieval pipeline completed successfully!")
