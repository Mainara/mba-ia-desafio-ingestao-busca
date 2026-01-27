import os
from dotenv import load_dotenv
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME", "document_embeddings")

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def get_embeddings_model():
    if os.getenv("OPENAI_API_KEY"):
        return OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"))
    elif os.getenv("GOOGLE_API_KEY"):
        return GoogleGenerativeAIEmbeddings(model=os.getenv("GOOGLE_EMBEDDING_MODEL", "models/embedding-001"))
    else:
        raise ValueError("Nenhuma API KEY encontrada.")

def get_llm():
    if os.getenv("OPENAI_API_KEY"):
        return ChatOpenAI(model="gpt-5-nano", temperature=0)
    elif os.getenv("GOOGLE_API_KEY"):
        return ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0)
    else:
        raise ValueError("Nenhuma API KEY encontrada.")

def search_prompt(question):
    if not question:
        return "Por favor, faça uma pergunta."

    try:
        embeddings = get_embeddings_model()
        vector_store = PGVector(
            embeddings=embeddings,
            collection_name=COLLECTION_NAME,
            connection=DATABASE_URL,
            use_jsonb=True,
        )
        
        # Buscar os 10 resultados mais relevantes
        docs_with_scores = vector_store.similarity_search_with_score(question, k=10)
        
        # Concatenar o conteúdo dos documentos
        contexto = "\n\n".join([doc.page_content for doc, _ in docs_with_scores])
        
        prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)
        llm = get_llm()
        
        chain = prompt | llm | StrOutputParser()
        
        response = chain.invoke({"contexto": contexto, "pergunta": question})
        return response

    except Exception as e:
        return f"Erro ao processar sua pergunta: {str(e)}"