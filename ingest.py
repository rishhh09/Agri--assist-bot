import sys
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma

# Directories
DB_DIRECTORY = "db"
DATA_DIRECTORY = "data/"

# --------- LOAD PDF DOCUMENTS ---------
def load_documents(directory_path=DATA_DIRECTORY):
    print(f"📄 Loading PDFs from: {directory_path}")

    loader = PyPDFDirectoryLoader(directory_path)
    documents = loader.load()

    if not documents:
        print(f"❌ No PDFs found in '{directory_path}'")
        print("👉 Add PDFs to the /data folder and try again.")
        sys.exit(1)

    print(f"✅ Loaded {len(documents)} pages.")
    return documents

# --------- SPLIT DOCUMENTS INTO CHUNKS (OPTIMIZED) ---------
def split_documents_into_chunks(documents):
    print("✂️ Splitting into optimized chunks...")

    # Smaller chunks = MUCH better results for FLAN-T5
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=50
    )

    chunks = text_splitter.split_documents(documents)
    print(f"✅ Created {len(chunks)} chunks.")
    return chunks

# --------- CREATE + SAVE VECTOR DATABASE ---------
def create_vector_database(chunks):
    print("🔍 Creating vector database...")

    embedding_model = SentenceTransformerEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    db = Chroma.from_documents(
        chunks,
        embedding_model,
        persist_directory=DB_DIRECTORY
    )

    print(f"✅ Vector DB saved to '{DB_DIRECTORY}'")
    return db

# --------- MAIN EXECUTION ---------
if __name__ == "__main__":
    docs = load_documents()
    chunks = split_documents_into_chunks(docs)
    create_vector_database(chunks)

    print("\n🎉 DONE — Your database is ready!")
