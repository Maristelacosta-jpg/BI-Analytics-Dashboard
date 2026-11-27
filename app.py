from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="BI Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Carregar arquivo
arquivo_csv = Path(__file__).resolve().parent / "vendas.csv"

st.title("📊 BI Analytics Dashboard")
st.markdown("Dashboard interativo para análise de vendas e desempenho comercial.")

if not arquivo_csv.exists():
    st.error("Arquivo vendas.csv não encontrado.")
    st.stop()

dados = pd.read_csv(arquivo_csv)

# Exibir nomes das colunas
st.subheader("Colunas identificadas")
st.write(dados.columns.tolist())

# Ajuste os nomes caso sejam diferentes no seu CSV
col_data = dados.columns[0]
col_loja = dados.columns[1]
col_regiao = dados.columns[2]
col_produto = dados.columns[3]
col_categoria = dados.columns[4]
col_quantidade = dados.columns[5]
col_vendas = dados.columns[6]
col_lucro = dados.columns[7]

# KPIs
faturamento_total = dados[col_vendas].sum()
lucro_total = dados[col_lucro].sum()
quantidade_total = dados[col_quantidade].sum()

col1, col2, col3 = st.columns(3)

col1.metric(
    "💰 Faturamento Total",
    f"R$ {faturamento_total:,.0f}"
)

col2.metric(
    "📦 Quantidade Vendida",
    f"{quantidade_total:,.0f}"
)

col3.metric(
    "📈 Lucro Total",
    f"R$ {lucro_total:,.0f}"
)

st.divider()

# Filtro
categorias = st.sidebar.multiselect(
    "Categoria",
    options=dados[col_categoria]
