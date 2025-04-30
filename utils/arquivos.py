import pandas as pd
from docx import Document
from PyPDF2 import PdfReader
from dotenv import load_dotenv

load_dotenv()

# Função segura que só usa tkinter se estiver disponível
def abrir_explorador_documentos():
    try:
        from tkinter import filedialog, Tk
        root = Tk()
        root.withdraw()
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
    except ImportError:
        print("⚠️ tkinter não está disponível neste ambiente.")
        return None

def ler_documento(filepath):
    if filepath is None:
        return "Nenhum arquivo foi selecionado."

    if filepath.endswith(".docx"):
        doc = Document(filepath)
        texto = "\n".join([p.text for p in doc.paragraphs])
    elif filepath.endswith(".txt"):
        with open(filepath, "r", encoding="utf-8") as file:
            texto = file.read()
    elif filepath.endswith(".pdf"):
        reader = PdfReader(filepath)
        texto = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif filepath.endswith(".xlsx"):
        df = pd.read_excel(filepath, engine="openpyxl")
        texto = df.to_string()
    elif filepath.endswith(".csv"):
        df = pd.read_csv(filepath)
        texto = df.to_string()
    else:
        texto = "Formato de arquivo não suportado."
    return texto
