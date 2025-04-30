# ChatBot NUTES - Plataforma Senior

Este projeto é um chatbot inteligente(voltado para a aréa/dados de Atividades Físicas) desenvolvido com [Streamlit](https://streamlit.io/) e [LangChain](https://www.langchain.com/) que responde perguntas sobre a **plataforma Senior**, com suporte a arquivos de texto (PDF, DOCX, TXT). O chat faz requisições as APIs da Senior para responder perguntas específicas.

## Funcionalidades

- Interface interativa via navegador
- Upload e análise de arquivos
- Integração com a API da OpenAI (GPT-4o)
- Integração com a API da Senior
- Autenticação automática com a API do NUTES
- Detecção de perguntas irrelevantes
- Calculos estatísticos

---

## Estrutura do Projeto

ChatBot-NUTES/ │ ├── tools/ │ └── funcoes_analise.py │ tools.py ├── utils/ │ └── agent.py │ └── arquivos.py │ └── autenticacao_nutes.py # Gera o token da API NUTES │ └── embeddings.py │ └── historico.py ├── temp/ # pasta para armazenar os arquivos de upload no navegador│ ├── chatbot.py ├── app.py  # Arquivo para execução no terminal ├── streamlit_app.py # Arquivo principal para execução no navegador  ├── requirements.txt ├── .env # chave da API └── README.md

