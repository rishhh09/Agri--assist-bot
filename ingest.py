# ingest.py
import sys
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma

# --- Define the path for the database ---
DB_DIRECTORY = "db"
DATA_DIRECTORY = "data/"

# --- Part A: Load the PDFs ---
def load_documents(directory_path=DATA_DIRECTORY):
    print(f"Loading documents from {directory_path}...")
    loader = PyPDFDirectoryLoader(directory_path)
    documents = loader.load()
    
    if not documents:
        print(f"Error: No PDF files found in the '{directory_path}' folder.")
        print("Please make sure you have downloaded the PDF and placed it in the 'data' folder.")
        sys.exit(1)
        
    print(f"Loaded {len(documents)} document pages.")
    return documents

# --- Part B: Chunk the Documents ---
def split_documents_into_chunks(documents):
    print("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks.")
    return chunks

# --- Part C: Create and SAVE the Vector Database ---
def create_vector_database(chunks):
    print("Creating vector database... (This may take a moment)")
    embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # This now SAVES the database to the "db" folder
    db = Chroma.from_documents(
        chunks, 
        embedding_model, 
        persist_directory=DB_DIRECTORY
    )
    print(f"Vector database created and saved to '{DB_DIRECTORY}' folder.")
    return db

# --- This is the main part that runs when you start the script ---
if __name__ == "__main__":
    
    # 1. Load
    documents = load_documents()
    
    # 2. Chunk
    chunks = split_documents_into_chunks(documents)
    
    # 3. Create and Save Database
    db = create_vector_database(chunks)
    
    print("\n--- Process Complete ---")
    print("The database is now built and saved in the 'db' folder.")
    print("You can now share your project. Your team does NOT need to run this script again.")