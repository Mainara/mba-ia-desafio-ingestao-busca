import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")
DATABASE_URL = os.getenv("DATABASE_URL")
COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME", "document_embeddings")

def get_embeddings_model():
    if os.getenv("OPENAI_API_KEY"):
        print("Usando OpenAI")
        return OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"))
    elif os.getenv("GOOGLE_API_KEY"):
        print("Usando Google Generative AI")
        return GoogleGenerativeAIEmbeddings(model=os.getenv("GOOGLE_EMBEDDING_MODEL", "models/embedding-001"))
    else:
        raise ValueError("Nenhuma API KEY encontrada (OPENAI_API_KEY ou GOOGLE_API_KEY).")

def ingest_pdf():
    if not PDF_PATH or not os.path.exists(PDF_PATH):
        print(f"Erro: Arquivo PDF não encontrado em '{PDF_PATH}'")
        return

    print(f"Iniciando ingestão do arquivo: {PDF_PATH}")
    
    # 1. Load PDF
    loader = PyPDFLoader(PDF_PATH)
    docs = loader.load()
    print(f"PDF carregado. Páginas: {len(docs)}")

    # 2. Split Text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )
    splits = text_splitter.split_documents(docs)
    print(f"Texto dividido em {len(splits)} chunks.")

    # 3. Initialize Embeddings and Vector Store
    embeddings = get_embeddings_model()
    
    print("Conectando ao banco de dados e salvando vetores... (isso pode demorar)")
    PGVector.from_documents(
        documents=splits,
        embedding=embeddings,
        connection=DATABASE_URL,
        collection_name=COLLECTION_NAME,
        use_jsonb=True,
    )
    print("Ingestão concluída com sucesso!")

if __name__ == "__main__":
    ingest_pdf()