# Codigo para um Chat conversacional no proprio terminal

'''
# app.py
import streamlit as st
from chatbot import agent
from utils.arquivos import abrir_explorador_documentos, ler_documento
from utils.embeddings import verificar_relevancia
from utils.historico import salvar_historico
from dotenv import load_dotenv

load_dotenv()

# Chat conversacional
while True:
    print("\nDigite sua pergunta, 'a' para abrir um documento, ou 'x' para sair.")
    entrada = input("Sua entrada: ")

    if entrada.lower() in ['sair', 'x']:
        print("Encerrando o chat.")
        salvar_historico(agent.memory.chat_memory.messages)
        break

    elif entrada.lower() == 'a':
        print("Abrindo o explorador de arquivos para selecionar um documento...")
        filepath = abrir_explorador_documentos()
        if filepath:
            print(f"Carregando documento do arquivo: {filepath}")
            conteudo = ler_documento(filepath)
            print(f"Conteúdo do documento:\n{conteudo[:500]}")  # muda esse parametro de acordo com o tamanho do arquivo
            # Opcional: Adiciona o conteúdo como mensagem no chat
            agent.memory.chat_memory.add_user_message(f"Conteúdo do documento carregado:\n{conteudo[:500]}")
        else:
            print("Nenhum arquivo selecionado.")
        continue
    
    # Verifica a relevância da pergunta do usuario
    relevancia = verificar_relevancia(entrada)

    # Se a pergunta for irrelevante
    if relevancia == 0:
        print("Desculpe, só posso responder perguntas sobre a plataforma Senior.")
        continue  # Retorna ao início do loop sem processar a pergunta nem gerar resposta
    # Se a pergunta for relevante, processa a resposta
    else:
        # Adiciona a pergunta à memória
        agent.memory.chat_memory.add_user_message(entrada)
    
        # Obtém a resposta do agente
        result = agent.invoke({"input": entrada})
    
        # Adiciona a resposta à memória
        agent.memory.chat_memory.add_ai_message(result.get("output", "Sem resposta"))
    
        # Exibe a pergunta e resposta final
        print("Pergunta:", entrada)
        print("Resposta:", result.get("output", "Sem resposta"))

'''
