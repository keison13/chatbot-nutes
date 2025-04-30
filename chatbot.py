from utils.agent import create_agent_with_memory
from tools.tools import tools
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
import os
import openai
from dotenv import load_dotenv

load_dotenv()

# Verifique se a chave foi carregada corretamente
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("A chave da OpenAI não foi encontrada no arquivo .env ou nas Secrets do Streamlit.")

# Configura a chave da API no OpenAI
openai.api_key = api_key

# Agente

model = ChatOpenAI(
    model="gpt-4o-mini", # menor modelo e mais barato, bom para avaliar a capacidade do agente com menos recursos, outras opções gpt-3.5-turbo, gpt-4o, gpt-4
    temperature = 0,
    max_tokens = None,
    timeout = None,
    max_retries = 2,
)


# Prompt base do agente
prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="""
Você é um assistente especializado em analisar e fornecer informações sobre dados de saúde, em específico atividades físicas.
Analise cuidadosamente os dados obtidos e responda às perguntas do usuário de forma precisa e concisa.
Responda estritamente de acordo com a solicitação do usuário.
Se o usuário pedir apenas um tipo específico de dado, não inclua informações adicionais.
"""),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    MessagesPlaceholder(variable_name="agent_scratchpad", optional=True),
])


# Iniciar o agente com memória
agent = create_agent_with_memory(model, tools, prompt)


