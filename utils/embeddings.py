from sklearn.metrics import accuracy_score
from sklearn.metrics.pairwise import cosine_similarity
import openai
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv

# load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("A chave da OpenAI não foi encontrada nas variáveis de ambiente ou nas Secrets do Streamlit.")

openai.api_key = openai_api_key  # Configura a chave para o openai

# DataFrame com perguntas relevantes/irrelevantes
dados = {
    "pergunta": [
        "Como agendar uma consulta na plataforma Sênior Móvel?",
        "A Senior Móvel permite telemedicina?",
        "Quais são os profissionais cadastrados na Senior Móvel?",
        "Como acessar o prontuário do paciente na Senior Móvel?",
        "Qual foi a duração total do sono do paciente?",
        "Quantos passos o paciente deu ao longo do dia?",
        "Me informe a média da duração de sono dos pacientes.",
        "Qual a lista de cuidadores cadastrados na plataforma?",
        "Me dê as estatísticas de passos do paciente.",
        "Me dê as estatísticas de duração do paciente.",
        "Me dê as estatísticas de calorias do paciente.",
        "Execute o teste ANOVA para comparar passos do paciente.",
        "Execute o teste ANOVA para comparar duração do paciente.",
        "Execute o teste ANOVA para comparar calorias do paciente.",
        "Como IA generativa é usada na plataforma da Senior Móvel?",
        "Qual o tema dessa planilha com dados de pacientes da Senior Móvel?",
        "Qual o tema desse documento sobre pacientes da Senior Móvel?",
        "Faça um resumo sobre a plataforma da Senior",
        "Qual é o melhor smartphone do momento?",
        "Como funciona a tecnologia 5G?",
        "Quem ganhou o Oscar de Melhor Filme este ano?",
        "Como aprender inglês rapidamente?",
        "Qual é a capital da Austrália?",
        "Quais são as músicas mais tocadas no Spotify atualmente?",
        "Como configurar o Google Drive para backup automático?",
        "O que é economia circular e por que é importante?",
        "Quem é o presidente do Brasil atualmente?",
        "Resolva essa expressão matemática: x = (10 * 30) + (40 + 20)",
        "Quanto é 30 + 30?",
        "Onde será transmitido o jogo do Brasil?",
        "Qual o tema desse documento bancario?",
        "Esse curriculo esta bom?",
        "Como fazer um TCC?",
        "Faça um breve resumo sobre IA generativa.",
        "Me passe uma dieta para emagrecimento",
        "Com funciona o teste ANOVA?"
    ],
    "relevante": [
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    ]
}

# Criar DataFrame com os dados
df = pd.DataFrame(dados)

# Função para obter embeddings da OpenAI
def get_embedding(text):
    response = openai.embeddings.create(
        input=text, 
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

# Gerar embeddings para todas as perguntas
df["embedding"] = df["pergunta"].apply(get_embedding)

# Função para verificar relevância com embeddings
def verificar_relevancia(pergunta, threshold=0.75):
    """Classifica a pergunta como relevante (1) ou irrelevante (0) baseado na similaridade de cosseno."""
    pergunta_emb = np.array(get_embedding(pergunta)).reshape(1, -1)  # Vetor da nova pergunta
    embeddings_db = np.vstack(df["embedding"].values)  # Matriz de embeddings existentes
    
    # Calcular similaridade de cosseno entre a nova pergunta e as existentes
    similaridades = cosine_similarity(pergunta_emb, embeddings_db)[0]
    
    # Pega a maior similaridade encontrada
    max_sim = np.max(similaridades)
    indice_max = np.argmax(similaridades)
    
    # Se a similaridade for alta, retorna a classificação do item mais próximo
    if max_sim >= threshold:
        return df.iloc[indice_max]["relevante"]
    return 0  # Considera irrelevante se a similaridade for baixa

# Avaliar a precisão do modelo
y_pred = df["pergunta"].apply(verificar_relevancia)
acuracia = accuracy_score(df["relevante"], y_pred)
print(f"Acurácia do modelo: {acuracia * 100:.2f}%")