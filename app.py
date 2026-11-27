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

# Título
st.title("📊 BI Analytics Dashboard")
st.markdown(
    "Dashboard interativo para análise de vendas e desempenho comercial."
)

# Caminho do CSV
arquivo_csv = Path(__file__).resolve().parent / "vendas.csv"

if not arquivo_csv.exists():
    st.error("Arquivo vendas.csv não encontrado.")
    st.stop()

# Leitura do CSV sem cabeçalho
dados = pd.read_csv(
    arquivo_csv,
    header=None,
    names=[
        "Data",
        "Loja",
        "Regiao",
        "Produto",
        "Categoria",
        "Quantidade",
        "Faturamento",
        "Lucro",
        "Canal"
    ]
)

# Sidebar
st.sidebar.header("Filtros")

categoria = st.sidebar.multiselect(
    "Categoria",
    options=dados["Categoria"].unique(),
    default=dados["Categoria"].unique()
)

dados_filtrados = dados[
    dados["Categoria"].isin(categoria)
]

# KPIs
faturamento_total = dados_filtrados["Faturamento"].sum()
lucro_total = dados_filtrados["Lucro"].sum()
quantidade_total = dados_filtrados["Quantidade"].sum()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "💰 Faturamento Total",
        f"R$ {faturamento_total:,.0f}"
    )

with col2:
    st.metric(
        "📦 Quantidade Vendida",
        f"{quantidade_total:,.0f}"
    )

with col3:
    st.metric(
        "📈 Lucro Total",
        f"R$ {lucro_total:,.0f}"
    )

st.divider()

# Gráfico de barras
fig1 = px.bar(
    dados_filtrados,
    x="Produto",
    y="Faturamento",
    color="Categoria",
    title="Faturamento por Produto",
    text_auto=True
)

st.plotly_chart(fig1, use_container_width=True)

# Gráfico de pizza
fig2 = px.pie(
    dados_filtrados,
    names="Produto",
    values="Lucro",
    title="Participação do Lucro por Produto"
)

st.plotly_chart(fig2, use_container_width=True)

# Tabela
st.subheader("📋 Dados Detalhados")

st.dataframe(
    dados_filtrados,
    use_container_width=True
)
