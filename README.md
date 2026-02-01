# Ingestão e Busca Semântica com LangChain e Postgres

Este projeto implementa um sistema de RAG (Retrieval-Augmented Generation) capaz de ler um arquivo PDF, armazenar seu conteúdo em um banco de dados vetorial PostgreSQL (com a extensão `pgvector`) e permitir buscas semânticas via linha de comando (CLI).

## Objetivos

1. **Ingestão**: Ler `document.pdf`, dividir em chunks de 1000 caracteres (overlap de 150) e salvar os embeddings no Postgres.
2. **Busca**: Permitir perguntas via terminal com respostas baseadas exclusivamente no documento.

## Tecnologias

- **Linguagem**: Python
- **Framework**: LangChain
- **Banco de Dados**: PostgreSQL + pgVector
- **Embeddings/LLM**: OpenAI (GPT/text-embedding-3-small) ou Google Gemini (models/embedding-001)

## Pré-requisitos

- Docker e Docker Compose instalados.
- Python 3.10+ instalado.
- Chave de API da OpenAI ou Google Gemini.

## Configuração

1. **Clone o repositório:**
   ```bash
   git clone <url-do-repositorio>
   cd <nome-do-diretorio>
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente:**
   Crie um arquivo `.env` na raiz (baseado no `.env.example`) e preencha as chaves:
   ```env
   # Escolha uma das APIs abaixo:
   OPENAI_API_KEY=sua_chave_openai
   # OU
   GOOGLE_API_KEY=sua_chave_google

   # Configurações do Banco de Dados (Padrão docker-compose)
   DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag
   PG_VECTOR_COLLECTION_NAME=document_embeddings

   # Caminho do PDF para ingestão
   PDF_PATH=document.pdf
   ```

   **Detalhes das variáveis:**
   - `DATABASE_URL`: URL de conexão com o PostgreSQL (já configurada para o container padrão).
   - `PG_VECTOR_COLLECTION_NAME`: Nome da "tabela" de vetores dentro do Postgres.
   - `PDF_PATH`: Nome do arquivo PDF que será processado pelo script de ingestão.

## Como Executar

1. **Subir o banco de dados:**
   ```bash
   docker compose up -d
   ```

2. **Executar a ingestão do PDF:**
   Certifique-se de que o arquivo `document.pdf` está na raiz do projeto.
   ```bash
   python src/ingest.py
   ```

3. **Rodar o chat CLI:**
   ```bash
   python src/chat.py
   ```

## Regras do Chat

O sistema segue regras estritas:
- Responde apenas com base no contexto do PDF.
- Se a informação não estiver presente, responde: *"Não tenho informações necessárias para responder sua pergunta."*
- Nunca utiliza conhecimento externo ou inventa informações.
