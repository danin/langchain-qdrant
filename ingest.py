# Import necessary modules
from langchain_community.vectorstores import Qdrant
from langchain_huggingface import HuggingFaceEmbeddings  # Corrected import
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter  # Corrected import

# Load PDF document
loader = PyPDFLoader("document.pdf")
documents = loader.load()

# Split text into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = text_splitter.split_documents(documents)

# Load HuggingFace embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-large-en",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': False}
)

print("Embedding model loaded successfully!")

# Qdrant setup
url = 'http://localhost:6333'
collection_name = "gpt_db"

# Corrected `ftom_documents` → `from_documents`
qdrant = Qdrant.from_documents(
    chunks,
    embeddings,
    url=url,
    prefer_grpc=False,
    collection_name=collection_name
)

print("Qdrant index created")
