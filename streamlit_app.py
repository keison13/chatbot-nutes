# Codigo do chat em Streamlit

import streamlit as st
from utils.agent import create_agent_with_memory
from tools.tools import tools
from utils.embeddings import verificar_relevancia
from utils.arquivos import ler_documento
from chatbot import prompt, model
import os
from dotenv import load_dotenv

# load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("A chave da OpenAI não foi encontrada nas variáveis de ambiente ou nas Secrets do Streamlit.")

# Configura a página
st.set_page_config(page_title="Chat Sênior Móvel", layout="centered")
st.title("🩺 Chat da Sênior Móvel")

# Inicializa o agente e memória na sessão
if "agent" not in st.session_state:
    st.session_state.agent = create_agent_with_memory(model, tools, prompt)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pending_user_input" not in st.session_state:
    st.session_state.pending_user_input = None

# Upload de documentos
st.sidebar.header("Upload de Documentos")
uploaded_file = st.sidebar.file_uploader(
    "Envie um documento (docx, txt, pdf, xlsx, csv):", 
    type=["docx", "txt", "pdf", "xlsx", "csv"]
)

if uploaded_file is not None:
    file_path = f"temp/{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    conteudo = ler_documento(file_path)
    mensagem = f"Conteúdo do documento carregado:\n{conteudo[:500]}"
    st.session_state.agent.memory.chat_memory.add_user_message(mensagem)
    st.sidebar.success("Documento carregado com sucesso!")
    st.sidebar.write(conteudo[:300] + "...")

# Entrada do usuário
user_input = st.chat_input("Digite sua pergunta sobre a plataforma...")

# Se o usuário acabou de enviar uma pergunta, salvamos no estado
if user_input:
    st.session_state.pending_user_input = user_input

# Processa a entrada pendente (só entra aqui 1x por envio)
if st.session_state.pending_user_input:
    pergunta = st.session_state.pending_user_input
    st.session_state.chat_history.append(("user", pergunta))

    if verificar_relevancia(pergunta) == 0:
        resposta = "Desculpe, só posso responder perguntas sobre a plataforma Sênior Móvel."
    else:
        st.session_state.agent.memory.chat_memory.add_user_message(pergunta)
        resposta = st.session_state.agent.invoke({"input": pergunta}).get("output", "Sem resposta")
        st.session_state.agent.memory.chat_memory.add_ai_message(resposta)

    st.session_state.chat_history.append(("assistant", resposta))

    # Limpa a pendência após o processamento
    st.session_state.pending_user_input = None

# Exibe histórico do chat
for role, msg in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(msg)