from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="BI Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 BI Analytics Dashboard")
st.markdown("Dashboard interativo para análise de vendas.")

arquivo_csv = Path(__file__).resolve().parent / "vendas.csv"

dados = pd.read_csv(arquivo_csv)

# KPI's
total_vendas = dados["Valor (R$)"].sum()
total_quantidade = dados["Quantidade"].sum()
total_produtos = dados["Produto"].nunique()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("💰 Faturamento Total", f"R$ {total_vendas:,.0f}")

with col2:
    st.metric("📦 Quantidade Vendida", total_quantidade)

with col3:
    st.metric("🛒 Produtos Diferentes", total_produtos)

# Filtro
st.sidebar.header("Filtros")

regiao = st.sidebar.multiselect(
    "Região",
    dados["Região"].unique(),
    default=dados["Região"].unique()
)

dados_filtrados = dados[
    dados["Região"].isin(regiao)
]

st.divider()

# Gráfico 1
fig1 = px.bar(
    dados_filtrados,
    x="Produto",
    y="Valor (R$)",
    color="Produto",
    title="Faturamento por Produto"
)

st.plotly_chart(fig1, use_container_width=True)

# Gráfico 2
fig2 = px.pie(
    dados_filtrados,
    names="Região",
    values="Valor (R$)",
    title="Participação das Regiões"
)

st.plotly_chart(fig2, use_container_width=True)

# Gráfico 3
vendas_regiao = dados_filtrados.groupby(
    "Região",
    as_index=False
)["Valor (R$)"].sum()

fig3 = px.bar(
    vendas_regiao,
    x="Região",
    y="Valor (R$)",
    title="Faturamento por Região"
)

st.plotly_chart(fig3, use_container_width=True)

# Tabela
st.subheader("📋 Dados Detalhados")

st.dataframe(
    dados_filtrados,
    use_container_width=True
)
