import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# -------------------------
# Configuração da página
# -------------------------
st.set_page_config(
    page_title="Dashboard de Vendas",
    page_icon="📊",
    layout="wide",
)

# -------------------------
# Carregamento dos dados
# -------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "vendas.csv"

@st.cache_data
def carregar_dados():
    try:
        df = pd.read_csv(DATA_PATH)
    except FileNotFoundError:
        st.error("Arquivo de dados não encontrado em: data/vendas.csv")
        st.stop()

    # Ajustar colunas
    df["Data"] = pd.to_datetime(df["Data"], errors="coerce")
    df["Quantidade"] = pd.to_numeric(df["Quantidade"], errors="coerce")
    df["ValorUnitario"] = pd.to_numeric(df["ValorUnitario"], errors="coerce")
    df["CustoUnitario"] = pd.to_numeric(df["CustoUnitario"], errors="coerce")

    # Cálculos principais
    df["Receita"] = df["Quantidade"] * df["ValorUnitario"]
    df["CustoTotal"] = df["Quantidade"] * df["CustoUnitario"]
    df["Lucro"] = df["Receita"] - df["CustoTotal"]
    df["Margem"] = df["Lucro"] / df["Receita"]
    df["Mes"] = df["Data"].dt.to_period("M").astype(str)

    return df

df = carregar_dados()

# -------------------------
# Filtros
# -------------------------
st.sidebar.title("Filtros")

# Data
min_date = df["Data"].min().date()
max_date = df["Data"].max().date()

start_date = st.sidebar.date_input("Data inicial", value=min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("Data final", value=max_date, min_value=min_date, max_value=max_date)

# Regiões
regioes = ["Todos"] + sorted(df["Regiao"].dropna().unique().tolist())
regiao = st.sidebar.selectbox("Região", regioes)

categorias = ["Todos"] + sorted(df["Categoria"].dropna().unique().tolist())
categoria = st.sidebar.selectbox("Categoria", categorias)

canais = ["Todos"] + sorted(df["CanalVenda"].dropna().unique().tolist())
canal = st.sidebar.selectbox("Canal de venda", canais)

lojas = ["Todos"] + sorted(df["Loja"].dropna().unique().tolist())
loja = st.sidebar.selectbox("Loja", lojas)

# Aplicar filtros
df_filtrado = df.copy()
df_filtrado = df_filtrado[(df_filtrado["Data"] >= pd.Timestamp(start_date)) & (df_filtrado["Data"] <= pd.Timestamp(end_date))]

if regiao != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Regiao"] == regiao]

if categoria != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Categoria"] == categoria]

if canal != "Todos":
    df_filtrado = df_filtrado[df_filtrado["CanalVenda"] == canal]

if loja != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Loja"] == loja]

# -------------------------
# KPIs
# -------------------------
receita_total = df_filtrado["Receita"].sum()
custo_total = df_filtrado["CustoTotal"].sum()
lucro_total = df_filtrado["Lucro"].sum()
quantidade_total = df_filtrado["Quantidade"].sum()
ticket_medio = receita_total / quantidade_total if quantidade_total > 0 else 0
margem_media = lucro_total / receita_total if receita_total > 0 else 0

# ------------ Título
st.title("📊 Dashboard de Vendas")
st.caption("Análise de desempenho por período, loja, categoria, região e canal de venda.")

# ------------ KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Receita total", f"R$ {receita_total:,.2f}")
col2.metric("Lucro total", f"R$ {lucro_total:,.2f}")
col3.metric("Quantidade vendida", f"{quantidade_total:,.0f}")
col4.metric("Ticket médio", f"R$ {ticket_medio:,.2f}")

# -------------------------
# Gráficos principais
# -------------------------
# Receita por mês
vendas_mes = (
    df_filtrado.groupby("Mes", as_index=False)
    .agg(Receita=("Receita", "sum"), Lucro=("Lucro", "sum"))
    .sort_values("Mes")
)

fig_linha = px.line(
    vendas_mes,
    x="Mes",
    y="Receita",
    markers=True,
    title="Receita por mês",
    color_discrete_sequence=["#1f77b4"],
)

fig_linha.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    title_x=0.5
)

# Receita por categoria
vendas_categoria = (
    df_filtrado.groupby("Categoria", as_index=False)
    .agg(Receita=("Receita", "sum"))
    .sort_values("Receita", ascending=False)
)

fig_categoria = px.bar(
    vendas_categoria,
    x="Categoria",
    y="Receita",
    title="Receita por categoria",
    color="Categoria",
    color_discrete_sequence=px.colors.qualitative.Set2,
)

# Receita por loja
vendas_loja = (
    df_filtrado.groupby("Loja", as_index=False)
    .agg(Receita=("Receita", "sum"))
    .sort_values("Receita", ascending=False)
)

fig_loja = px.bar(
    vendas_loja,
    x="Loja",
    y="Receita",
    title="Receita por loja",
    color="Loja",
    color_discrete_sequence=px.colors.qualitative.Pastel,
)

# Receita por região
vendas_regiao = (
    df_filtrado.groupby("Regiao", as_index=False)
    .agg(Receita=("Receita", "sum"))
    .sort_values("Receita", ascending=False)
)

fig_regiao = px.pie(
    vendas_regiao,
    names="Regiao",
    values="Receita",
    title="Participação por região",
    hole=0.4
)

# Top 10 produtos
top_produtos = (
    df_filtrado.groupby("Produto", as_index=False)
    .agg(Receita=("Receita", "sum"))
    .sort_values("Receita", ascending=False)
    .head(10)
)

fig_produtos = px.bar(
    top_produtos,
    x="Produto",
    y="Receita",
    title="Top 10 produtos por receita",
    color="Receita",
    color_continuous_scale="Blues",
)

# -------------------------
# Layout com gráficos
# -------------------------
st.plotly_chart(fig_linha, use_container_width=True)

col5, col6 = st.columns(2)
with col5:
    st.plotly_chart(fig_categoria, use_container_width=True)
with col6:
    st.plotly_chart(fig_regiao, use_container_width=True)

col7, col8 = st.columns(2)
with col7:
    st.plotly_chart(fig_loja, use_container_width=True)
with col8:
    st.plotly_chart(fig_produtos, use_container_width=True)

# -------------------------
# Tabela detalhada
# -------------------------
st.subheader("Dados detalhados")

tabela = df_filtrado[[
    "Data",
    "Loja",
    "Regiao",
    "Produto",
    "Categoria",
    "Quantidade",
    "ValorUnitario",
    "Receita",
    "CustoTotal",
    "Lucro",
    "CanalVenda"
]].sort_values("Data", ascending=False)

st.dataframe(tabela, use_container_width=True)

# -------------------------
# Resumo textual
# -------------------------
st.subheader("Resumo executivo")

st.write(
    f"Neste período, a empresa gerou receita total de "
    f"R$ {receita_total:,.2f}, com lucro de "
    f"R$ {lucro_total:,.2f} e margem de "
    f"{margem_media * 100:.2f}%. "
    f"A categoria e a região com maior participação foram analisadas nos gráficos acima."
)
