import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# -------------------------
# Configuração da página
# -------------------------
st.set_page_config(
    page_title="Dashboard BI - Vendas",
    page_icon="📊",
    layout="wide",
)

# O arquivo vendas.csv deve ficar na mesma pasta que app.py
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "vendas.csv"


# -------------------------
# Carregamento dos dados
# -------------------------
@st.cache_data
def carregar_dados():
    try:
        df = pd.read_csv(DATA_PATH)
    except FileNotFoundError:
        st.error(f"Arquivo de dados não encontrado em: {DATA_PATH}")
        st.stop()

    colunas_obrigatorias = [
        "Data",
        "Loja",
        "Regiao",
        "Produto",
        "Categoria",
        "Quantidade",
        "ValorUnitario",
        "CustoUnitario",
        "CanalVenda",
    ]

    colunas_ausentes = [coluna for coluna in colunas_obrigatorias if coluna not in df.columns]
    if colunas_ausentes:
        st.error(
            "O arquivo vendas.csv não contém estas colunas: "
            + ", ".join(colunas_ausentes)
        )
        st.stop()

    # Remove espaços extras dos campos de texto, como " Nordeste"
    colunas_texto = df.select_dtypes(include=["object"]).columns
    for coluna in colunas_texto:
        df[coluna] = df[coluna].str.strip()

    # Ajusta os tipos dos dados
    df["Data"] = pd.to_datetime(df["Data"], errors="coerce")
    df["Quantidade"] = pd.to_numeric(df["Quantidade"], errors="coerce")
    df["ValorUnitario"] = pd.to_numeric(df["ValorUnitario"], errors="coerce")
    df["CustoUnitario"] = pd.to_numeric(df["CustoUnitario"], errors="coerce")

    # Remove linhas com dados inválidos
    df = df.dropna(
        subset=["Data", "Quantidade", "ValorUnitario", "CustoUnitario"]
    ).copy()

    if df.empty:
        st.error("O arquivo vendas.csv não contém linhas de venda válidas.")
        st.stop()

    # Calcula os indicadores
    df["Receita"] = df["Quantidade"] * df["ValorUnitario"]
    df["CustoTotal"] = df["Quantidade"] * df["CustoUnitario"]
    df["Lucro"] = df["Receita"] - df["CustoTotal"]
    df["Margem"] = df["Lucro"].div(df["Receita"].where(df["Receita"] != 0))
    df["Mes"] = df["Data"].dt.to_period("M").astype(str)

    return df


df = carregar_dados()


# -------------------------
# Filtros
# -------------------------
st.sidebar.title("🧰 Filtros")

min_date = df["Data"].min().date()
max_date = df["Data"].max().date()

start_date = st.sidebar.date_input(
    "Data inicial",
    min_value=min_date,
    max_value=max_date,
    value=min_date,
)

end_date = st.sidebar.date_input(
    "Data final",
    min_value=min_date,
    max_value=max_date,
    value=max_date,
)

regioes = ["Todos"] + sorted(df["Regiao"].dropna().unique().tolist())
regiao = st.sidebar.selectbox("Região", regioes)

categorias = ["Todos"] + sorted(df["Categoria"].dropna().unique().tolist())
categoria = st.sidebar.selectbox("Categoria", categorias)

canais = ["Todos"] + sorted(df["CanalVenda"].dropna().unique().tolist())
canal = st.sidebar.selectbox("Canal de venda", canais)

lojas = ["Todos"] + sorted(df["Loja"].dropna().unique().tolist())
loja = st.sidebar.selectbox("Loja", lojas)


# -------------------------
# Aplicação dos filtros
# -------------------------
df_filtrado = df[
    (df["Data"].dt.date >= start_date)
    & (df["Data"].dt.date <= end_date)
].copy()

if regiao != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Regiao"] == regiao]

if categoria != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Categoria"] == categoria]

if canal != "Todos":
    df_filtrado = df_filtrado[df_filtrado["CanalVenda"] == canal]

if loja != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Loja"] == loja]


# -------------------------
# Título
# -------------------------
st.title("📊 Dashboard de Vendas")
st.caption("Painel executivo de análise de desempenho comercial")

if df_filtrado.empty:
    st.warning("Nenhuma venda encontrada para os filtros selecionados.")
    st.stop()


# -------------------------
# KPIs principais
# -------------------------
receita_total = df_filtrado["Receita"].sum()
custo_total = df_filtrado["CustoTotal"].sum()
lucro_total = df_filtrado["Lucro"].sum()
quantidade_total = df_filtrado["Quantidade"].sum()
ticket_medio = receita_total / quantidade_total if quantidade_total else 0
margem_percentual = (lucro_total / receita_total) * 100 if receita_total else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Receita Total", f"R$ {receita_total:,.2f}")
col2.metric("Lucro Total", f"R$ {lucro_total:,.2f}")
col3.metric("Quantidade Vendida", f"{quantidade_total:,.0f}")
col4.metric("Ticket Médio", f"R$ {ticket_medio:,.2f}")

st.markdown("---")


# -------------------------
# Abas do dashboard
# -------------------------
tab1, tab2, tab3 = st.tabs(
    ["📈 Visão Geral", "📊 Comparativos", "🧾 Dados"]
)


with tab1:
    # Receita por mês
    vendas_mes = (
        df_filtrado.groupby("Mes", as_index=False)
        .agg(Receita=("Receita", "sum"), Lucro=("Lucro", "sum"))
        .sort_values("Mes")
    )

    fig_line = px.line(
        vendas_mes,
        x="Mes",
        y="Receita",
        markers=True,
        title="Evolução da Receita por Mês",
        color_discrete_sequence=["#1f77b4"],
    )
    st.plotly_chart(fig_line, use_container_width=True)

    col_a, col_b = st.columns(2)

    with col_a:
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
            title="Receita por Categoria",
            color="Categoria",
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        st.plotly_chart(fig_categoria, use_container_width=True)

    with col_b:
        # Receita por canal de venda
        vendas_canal = (
            df_filtrado.groupby("CanalVenda", as_index=False)
            .agg(Receita=("Receita", "sum"))
            .sort_values("Receita", ascending=False)
        )

        fig_canal = px.pie(
            vendas_canal,
            names="CanalVenda",
            values="Receita",
            title="Receita por Canal de Venda",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set3,
        )
        st.plotly_chart(fig_canal, use_container_width=True)


with tab2:
    col_a, col_b = st.columns(2)

    with col_a:
        # Receita e lucro por loja
        vendas_loja = (
            df_filtrado.groupby("Loja", as_index=False)
            .agg(Receita=("Receita", "sum"), Lucro=("Lucro", "sum"))
            .sort_values("Receita", ascending=False)
        )

        fig_loja = px.bar(
            vendas_loja,
            x="Loja",
            y="Receita",
            title="Receita por Loja",
            color="Lucro",
            color_continuous_scale="Viridis",
        )
        st.plotly_chart(fig_loja, use_container_width=True)

    with col_b:
        # Receita por região
        vendas_regiao = (
            df_filtrado.groupby("Regiao", as_index=False)
            .agg(Receita=("Receita", "sum"))
            .sort_values("Receita", ascending=False)
        )

        fig_regiao = px.bar(
            vendas_regiao,
            x="Regiao",
            y="Receita",
            title="Receita por Região",
            color="Regiao",
            color_discrete_sequence=px.colors.qualitative.Dark2,
        )
        st.plotly_chart(fig_regiao, use_container_width=True)

    # Dez produtos com maior receita
    top_produtos = (
        df_filtrado.groupby("Produto", as_index=False)
        .agg(Receita=("Receita", "sum"), Quantidade=("Quantidade", "sum"))
        .sort_values("Receita", ascending=False)
        .head(10)
    )

    fig_top_produtos = px.bar(
        top_produtos,
        x="Produto",
        y="Receita",
        title="Top 10 Produtos por Receita",
        color="Quantidade",
        color_continuous_scale="Blues",
    )
    st.plotly_chart(fig_top_produtos, use_container_width=True)


with tab3:
    colunas_tabela = [
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
        "CanalVenda",
    ]

    tabela = df_filtrado[colunas_tabela].sort_values(
        "Data",
        ascending=False,
    )

    st.dataframe(tabela, use_container_width=True)

    st.subheader("Resumo Executivo")
    st.markdown(
        f"""
        - Receita total: **R$ {receita_total:,.2f}**
        - Custo total: **R$ {custo_total:,.2f}**
        - Lucro total: **R$ {lucro_total:,.2f}**
        - Margem: **{margem_percentual:.2f}%**
        - Quantidade vendida: **{quantidade_total:,.0f}**
        - Ticket médio: **R$ {ticket_medio:,.2f}**
        """
    )


# -------------------------
# Rodapé
# -------------------------
st.markdown("---")
st.caption("Dashboard em desenvolvimento — dados do arquivo vendas.csv")
