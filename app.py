from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Meu Dashboard", page_icon="📊")

arquivo_csv = Path(__file__).resolve().parent / "vendas.csv"

st.title("📊 Meu Dashboard de Vendas")
st.write(f"Procurando o CSV em: `{arquivo_csv}`")

if not arquivo_csv.exists():
    st.error("Não encontrei vendas.csv na mesma pasta que app.py.")
else:
    dados = pd.read_csv(arquivo_csv)
    st.success("CSV carregado!")
    st.write(f"Linhas encontradas: {len(dados)}")
    st.dataframe(dados, use_container_width=True)
