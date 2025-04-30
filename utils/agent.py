from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.memory import ConversationBufferWindowMemory
from utils.historico import carregar_historico
from dotenv import load_dotenv

load_dotenv()


# Função para criar o agente com memória
def create_agent_with_memory(model, tools, prompt):
    
    memory = ConversationBufferWindowMemory(k=5, memory_key="chat_history", return_messages=True)

    # Carregar histórico existente (caso haja)
    mensagens_anteriores = carregar_historico("historico_chat.json")
    for message in mensagens_anteriores:
        if message['role'] == 'assistant':
            memory.chat_memory.add_ai_message(message['content'])
        else:
            memory.chat_memory.add_user_message(message['content'])

    return AgentExecutor(agent=create_openai_functions_agent(model, tools, prompt), tools=tools, memory=memory, verbose=False)