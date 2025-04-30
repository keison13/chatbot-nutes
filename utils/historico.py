import json
from dotenv import load_dotenv

load_dotenv()

# Função para carregar histórico salvo em JSON e restaurar na memória (caso queira)
def carregar_historico(filepath="historico_chat.json"):
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            mensagens = json.load(file)
    except FileNotFoundError:
        # Se o arquivo não existir, retorna uma lista vazia
        mensagens = []
    
    # Retorna as mensagens carregadas
    return mensagens

# Função para salvar o histórico de conversação em um arquivo JSON
def salvar_historico(chat_messages):
    historico = []
    mensagens_adicionadas = set()  # Usado para rastrear mensagens 
    
    for message in chat_messages:
        role = message.__class__.__name__.replace("Message", "").lower()
        conteudo_mensagem = message.content
        
        # Cria um identificador único para cada mensagem
        identificador_mensagem = f"{role}:{conteudo_mensagem}"
        
        # Adiciona ao histórico somente se a mensagem ainda não estiver no conjunto
        if identificador_mensagem not in mensagens_adicionadas:
            historico.append({
                "role": role,
                "content": conteudo_mensagem
            })
            mensagens_adicionadas.add(identificador_mensagem)
    
    # Salva o histórico em um arquivo JSON
    with open("historico_chat.json", "w", encoding="utf-8") as file:
        json.dump(historico, file, indent=4, ensure_ascii=False)