# 📊 Painel de Análise de Vendas

Dashboard interativo de Business Intelligence para explorar dados de vendas, acompanhar indicadores e apoiar a tomada de decisão baseada em dados.

O projeto utiliza Python, Pandas e Streamlit para carregar, tratar e apresentar os dados em uma interface visual.

## 🎯 Objetivos

- Transformar dados de vendas em informações úteis.
- Acompanhar indicadores de desempenho (KPIs).
- Explorar tendências e resultados por meio de visualizações.
- Facilitar a análise dos dados de forma interativa.

## ✅ Funcionalidades

- Carregamento e análise de dados de vendas.
- Visualização de indicadores e gráficos.
- Exploração dos dados disponíveis no arquivo `vendas.csv`.

> As funcionalidades específicas dependem da implementação atual em `app.py`.

## 🏗️ Arquitetura

```mermaid
flowchart LR
    A[Arquivo vendas.csv] --> B[Python]
    B --> C[Pandas]
    C --> D[Tratamento dos dados]
    D --> E[Streamlit]
    E --> F[Dashboard interativo]
```

## 🛠️ Tecnologias

- Python
- Pandas
- Streamlit
- Git e GitHub

## 📁 Estrutura do projeto

```text
.
├── app.py
├── requirements.txt
├── vendas.csv
└── README.md
```

## 🚀 Como executar

1. Clone o repositório:

   ```bash
   git clone https://github.com/Maristelacosta/BI-Analytics-Dashboard.git
   ```

2. Acesse a pasta do projeto:

   ```bash
   cd BI-Analytics-Dashboard
   ```

3. (Opcional) Crie e ative um ambiente virtual:

   ```bash
   python -m venv .venv
   ```

   No Windows:

   ```bash
   .venv\Scripts\activate
   ```

   No macOS ou Linux:

   ```bash
   source .venv/bin/activate
   ```

4. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

5. Inicie o dashboard:

   ```bash
   streamlit run app.py
   ```

## 📊 Dados

O arquivo `vendas.csv` contém os dados utilizados pela aplicação. Para usar outra base, verifique em `app.py` o caminho do arquivo e os nomes das colunas esperados.

## 💡 Conceitos aplicados

- Business Intelligence
- Análise e visualização de dados
- Indicadores de desempenho (KPIs)
- Tratamento de dados com Pandas
- Dashboards interativos
- Tomada de decisão orientada por dados

## 🛣️ Próximas melhorias

- [ ] Aprimorar o dashboard executivo.
- [ ] Adicionar filtros analíticos.
- [ ] Permitir a exportação de relatórios.
- [ ] Automatizar a atualização dos dados.
- [ ] Publicar a aplicação online.

## 👩‍💻 Autora

**Maristela Costa**

Bacharel em Sistemas de Informação  
MBA em Cibersegurança e Proteção de Dados — em andamento  
MBA em Business Intelligence, Big Data e Analytics — em andamento  

GitHub: [@Maristelacosta](https://github.com/Maristelacosta)
