import token
from typing import Optional
import math
import requests
from scipy.stats import f_oneway, shapiro  # teste
from utils.autenticacao_nutes import token
from dotenv import load_dotenv

load_dotenv()

id_paciente = "65b92c778b12f3255eec1529" # Alan Turing 2.0

# Função genérica para fazer requisições à API e funçoes de calculos estatisticos
def api_request(endpoint: str, id_paciente: Optional[str] = None):
    """Realiza uma requisição GET para a API"""
    base_url = 'https://api.nutespb.com.br/v1'
    
    if id_paciente:
        url = f'{base_url}/patients/{id_paciente}/{endpoint}?page=1&limit=20&sort=created_at'

    else:
        url = f'{base_url}/{endpoint}?page=1&limit=20&sort=created_at'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    try:
        return response.json()
    except requests.JSONDecodeError:
        return {"error": "Erro ao decodificar a resposta JSON", "response_text": response.text}
    
    
# Funções para os tools
    
# Função para calcular a mediana
def calcular_mediana(valores):
    n = len(valores)
    if n == 0:
        return 0
    valores.sort()
    meio = n // 2
    if n % 2 == 0:
        return (valores[meio - 1] + valores[meio]) / 2
    return valores[meio]

# Função para calcular o desvio padrão
def calcular_desvio_padrao(valores):
    media = sum(valores) / len(valores)
    variancia = sum((x - media) ** 2 for x in valores) / len(valores)
    return math.sqrt(variancia)

    
def recuperar_passos_atividades(atividades):
    passos_list = []
    total_passos = 0
    for atividade in atividades:
        passos = atividade.get('steps', 0)
        passos_list.append(passos)
        total_passos += passos
    return passos_list, total_passos


def calcular_passos_atividades():
    """Calcular média, mediana e desvio padrão dos passos nas atividades fisicas"""

    atividades = api_request('physicalactivities', id_paciente)
    passos, total_passos = recuperar_passos_atividades(atividades)
    if not passos:
        return "Dados de passos não encontrados."

    media_passos = sum(passos) / len(passos)
    mediana_passos = calcular_mediana(passos)
    desvio_passos = calcular_desvio_padrao(passos)

    return {
        "Total": total_passos,
        "Média": media_passos,
        "Mediana": mediana_passos,
        "Desvio Padrão": desvio_passos
    }

def recuperar_duracao_atividades(atividades):
    duracao_list = []
    total_duracao = 0
    for atividade in atividades:
        duracao = atividade.get('duration', 0) / 60  # convertendo para minutos
        duracao_list.append(duracao)
        total_duracao += duracao
    return duracao_list, total_duracao
    
def calcular_duracao_atividades():
    """Calcular média, mediana e desvio padrão da duração nas atividades fisicas (minutos)"""

    atividades = api_request('physicalactivities', id_paciente)
    duracao, total_duracao = recuperar_duracao_atividades(atividades)
    if not duracao:
        return "Dados de duração não encontrados."

    media_duracao = sum(duracao) / len(duracao)
    mediana_duracao = calcular_mediana(duracao)
    desvio_duracao = calcular_desvio_padrao(duracao)

    return {
        "Total": total_duracao,
        "Média": media_duracao,
        "Mediana": mediana_duracao,
        "Desvio Padrão": desvio_duracao
    }

def recuperar_calorias_atividades(atividades):
    calorias_list = []
    total_calorias = 0
    for atividade in atividades:
        calorias = atividade.get('calories', 0)
        calorias_list.append(calorias)
        total_calorias += calorias
    return calorias_list, total_calorias

def calcular_calorias_atividades():
    """Calcular média, mediana e desvio padrão das calorias nas atividades fisicas"""

    atividades = api_request('physicalactivities', id_paciente)
    calorias, total_calorias = recuperar_calorias_atividades(atividades)
    if not calorias:
        return "Dados de calorias não encontrados."

    media_calorias = sum(calorias) / len(calorias)
    mediana_calorias = calcular_mediana(calorias)
    desvio_calorias = calcular_desvio_padrao(calorias)

    return {
        "Total": total_calorias,
        "Média": media_calorias,
        "Mediana": mediana_calorias,
        "Desvio Padrão": desvio_calorias
    }

# Função para recuperar os dados por tipo, para realizar testes estatísticos
def recuperar_dados_por_tipo():
    atividades = api_request('physicalactivities', id_paciente)

    # Inicialize as listas para cada tipo de atividade
    sport_atividades = []
    walk_atividades = []
    bike_atividades = []

    # Itere sobre as atividades e classifique-as com base no nome
    for atividade in atividades:
        # Verifique o nome da atividade para determinar o tipo
        nome_atividade = atividade.get('name', '').lower()  # Ajuste para o campo correto se necessário

        if 'sport' in nome_atividade:
            sport_atividades.append(atividade)
        elif 'walk' in nome_atividade:
            walk_atividades.append(atividade)
        elif 'bike' in nome_atividade or 'outdoor bike' in nome_atividade:
            bike_atividades.append(atividade)
    
    return sport_atividades, walk_atividades, bike_atividades


def realizar_teste_anova_passos():
    """Realiza o teste ANOVA e Shapiro-Wilk para comparar passos entre 'Sport', 'Walk' e 'Outdoor Bike'."""
    sport, walk, bike = recuperar_dados_por_tipo()
    
    # Extrair os passos para cada grupo
    sport_passos, _ = recuperar_passos_atividades(sport)
    walk_passos, _ = recuperar_passos_atividades(walk)
    bike_passos, _ = recuperar_passos_atividades(bike)
    
     # Verificar a normalidade de cada grupo usando o teste Shapiro-Wilk
    normalidade_sport = shapiro(sport_passos)
    normalidade_walk = shapiro(walk_passos)
    normalidade_bike = shapiro(bike_passos)
    
    # Verificando se algum grupo não segue a normalidade
    normalidade_resultado = {
        "Sport": "Normal" if normalidade_sport[1] > 0.05 else "Não Normal",
        "Walk": "Normal" if normalidade_walk[1] > 0.05 else "Não Normal",
        "Outdoor Bike": "Normal" if normalidade_bike[1] > 0.05 else "Não Normal"
    }

    # Realizar o teste ANOVA nos dados dos três grupos
    stat, p_value = f_oneway(sport_passos, walk_passos, bike_passos)
    
    # Concluir se há diferença significativa entre os grupos
    conclusao = "Com base na média dos grupos, há diferença significativa entre os grupos" if p_value < 0.05 else "Com base na média dos grupos, não há diferença significativa entre os grupos"
    
    # Retorno com as informações
    return {
        "Estatística F": stat,
        "Valor-p": p_value,
        "Conclusão": conclusao,
        "Normalidade dos grupos": normalidade_resultado,
        f"Passos de cada grupo: Sport = {sport_passos}, Walk = {walk_passos}, Outdoor Bike = {bike_passos}": None
    }

def realizar_teste_anova_calorias():
    """Realiza o teste ANOVA e Shapiro-Wilk para comparar calorias entre 'Sport', 'Walk' e 'Outdoor Bike'."""
    sport, walk, bike = recuperar_dados_por_tipo()
    
    # Extrair as calorias para cada grupo
    sport_calorias, _ = recuperar_calorias_atividades(sport)
    walk_calorias, _ = recuperar_calorias_atividades(walk)
    bike_calorias, _ = recuperar_calorias_atividades(bike)
    
     # Verificar a normalidade de cada grupo usando o teste Shapiro-Wilk
    normalidade_sport = shapiro(sport_calorias)
    normalidade_walk = shapiro(walk_calorias)
    normalidade_bike = shapiro(bike_calorias)
    
    # Verificando se algum grupo não segue a normalidade
    normalidade_resultado = {
        "Sport": "Normal" if normalidade_sport[1] > 0.05 else "Não Normal",
        "Walk": "Normal" if normalidade_walk[1] > 0.05 else "Não Normal",
        "Outdoor Bike": "Normal" if normalidade_bike[1] > 0.05 else "Não Normal"
    }

    # Realizar o teste ANOVA nos dados dos três grupos
    stat, p_value = f_oneway(sport_calorias, walk_calorias, bike_calorias)
    
    # Concluir se há diferença significativa entre os grupos
    conclusao = "Com base na média dos grupos, há diferença significativa entre os grupos" if p_value < 0.05 else "Com base na média dos grupos, não há diferença significativa entre os grupos"
    
    # Retorno com as informações
    return {
        "Estatística F": stat,
        "Valor-p": p_value,
        "Conclusão": conclusao,
        "Normalidade dos grupos": normalidade_resultado,
        f"Calorias de cada grupo: Sport = {sport_calorias}, Walk = {walk_calorias}, Outdoor Bike = {bike_calorias}": None
    }

def realizar_teste_anova_duracao():
    """Realiza o teste ANOVA e Shapiro-Wilk para comparar duração entre 'Sport', 'Walk' e 'Outdoor Bike'."""
    # Recupera os dados das atividades divididas por tipo
    sport_atividades, walk_atividades, bike_atividades = recuperar_dados_por_tipo()
    
    # Extrair a duração para cada grupo
    sport_duracao, _ = recuperar_duracao_atividades(sport_atividades)
    walk_duracao, _ = recuperar_duracao_atividades(walk_atividades)
    bike_duracao, _ = recuperar_duracao_atividades(bike_atividades)
    
    # Verificar a normalidade de cada grupo usando o teste Shapiro-Wilk
    normalidade_sport = shapiro(sport_duracao)
    normalidade_walk = shapiro(walk_duracao)
    normalidade_bike = shapiro(bike_duracao)
    
    # Verificando se algum grupo não segue a normalidade
    normalidade_resultado = {
        "Sport": "Normal" if normalidade_sport[1] > 0.05 else "Não Normal",
        "Walk": "Normal" if normalidade_walk[1] > 0.05 else "Não Normal",
        "Outdoor Bike": "Normal" if normalidade_bike[1] > 0.05 else "Não Normal"
    }

    # Realizar o teste ANOVA nos dados dos três grupos
    stat, p_value = f_oneway(sport_duracao, walk_duracao, bike_duracao)
    
    # Concluir se há diferença significativa entre os grupos
    conclusao = "Com base na média dos grupos, há diferença significativa entre os grupos" if p_value < 0.05 else "Com base na média dos grupos, não há diferença significativa entre os grupos"
    
    # Retorno com as informações
    return {
        "Estatística F": stat,
        "Valor-p": p_value,
        "Conclusão": conclusao,
        "Normalidade dos grupos": normalidade_resultado,
        f"Duração de cada grupo: Sport = {sport_duracao}, Walk = {walk_duracao}, Outdoor Bike = {bike_duracao}": None
    }

