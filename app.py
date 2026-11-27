from pathlib import Path
import pandas as pd

arquivo_excel = Path(__file__).resolve().parent / "Planilha_Exemplo_PowerBI.xlsx"

dados = pd.read_excel(
    arquivo_excel,
    engine="openpyxl"
)
