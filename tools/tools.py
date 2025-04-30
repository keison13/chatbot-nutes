from tools.funcoes_analise import api_request
from tools.funcoes_analise import id_paciente
from tools.funcoes_analise import realizar_teste_anova_calorias, realizar_teste_anova_duracao, realizar_teste_anova_passos
from tools.funcoes_analise import calcular_calorias_atividades, calcular_duracao_atividades, calcular_passos_atividades
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()

# Tools para serem passados para os agentes

@tool
def responder_teste_anova_passos():
    """Executa o teste ANOVA para comparar passos entre 'Sport', 'Walk' e 'Outdoor Bike'."""
    return realizar_teste_anova_passos()

@tool
def responder_teste_anova_calorias():
    """Executa o teste ANOVA para comparar calorias entre 'Sport', 'Walk' e 'Outdoor Bike'."""
    return realizar_teste_anova_calorias()

@tool
def responder_teste_anova_duracao():
    """Executa o teste ANOVA para comparar duração entre 'Sport', 'Walk' e 'Outdoor Bike'."""
    return realizar_teste_anova_duracao()

@tool
def patients():
    """Consultar a lista de todos os pacientes"""
    return api_request('patients')

@tool
def physicalactivitiespatientes():
   """Consultar a lista das atividades físicas"""
   return api_request('physicalactivities', id_paciente) # Alan Turing 2.0

@tool
def responder_passos_atividadesFisicas():
    """Tool para obter as estatísticas de passos (média, mediana e desvio padrão)."""
    return calcular_passos_atividades()

@tool
def responder_duracao_atividadesFisicas():
    """Tool para obter as estatísticas de duração (média, mediana e desvio padrão em minutos)."""
    return calcular_duracao_atividades()

@tool
def responder_calorias_atividadesFisicas():
    """Tool para obter as estatísticas de calorias (média, mediana e desvio padrão)."""
    return calcular_calorias_atividades()

    
tools = [
    patients, 
    physicalactivitiespatientes, 
    responder_passos_atividadesFisicas, 
    responder_duracao_atividadesFisicas, 
    responder_calorias_atividadesFisicas,
    responder_teste_anova_passos,
    responder_teste_anova_calorias,
    responder_teste_anova_duracao 
]