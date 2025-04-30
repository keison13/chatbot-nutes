import pandas as pd
from tkinter import filedialog
from tkinter import Tk
from docx import Document  # Biblioteca para manipular arquivos .docx
from PyPDF2 import PdfReader  # Biblioteca para manipular arquivos PDF
from dotenv import load_dotenv

load_dotenv()

# Função para abrir o explorador e selecionar arquivos selecionados
def abrir_explorador_documentos():
    root = Tk()
    root.withdraw()  # Oculta a janela principal do Tkinter
    filepath = filedialog.askopenfilename(
        title="Selecione um arquivo",
        filetypes=[
            ("Documentos Word", "*.docx"),
            ("Documentos de Texto", "*.txt"),
            ("PDF", "*.pdf"),
            ("Planilhas Excel", "*.xlsx"),
            ("Arquivos CSV", "*.csv"),
        ]
    )
    return filepath

# Função para ler o conteúdo de arquivos selecionados
def ler_documento(filepath):
    if filepath.endswith(".docx"):
        # Para arquivos .docx
        doc = Document(filepath)
        texto = "\n".join([paragrafo.text for paragrafo in doc.paragraphs])
    elif filepath.endswith(".txt"):
        # Para arquivos .txt
        with open(filepath, "r", encoding="utf-8") as file:
            texto = file.read()
    elif filepath.endswith(".pdf"):
        # Para arquivos .pdf
        reader = PdfReader(filepath)
        texto = "\n".join([page.extract_text() for page in reader.pages])
    elif filepath.endswith(".xlsx"):
        # Para arquivos .xlsx
        df = pd.read_excel(filepath, engine="openpyxl")
        texto = df.to_string()  # Converte o DataFrame em string legível
    elif filepath.endswith(".csv"):
        # Para arquivos .csv
        df = pd.read_csv(filepath)
        texto = df.to_string()  # Converte o DataFrame em string legível
    else:
        texto = "Formato de arquivo não suportado."
    return texto