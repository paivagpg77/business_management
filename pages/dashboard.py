import streamlit as st
import pandas as pd
import plotly.express as px
from db import get_connection

st.set_page_config(page_title="Dashboard Financeiro", layout="wide")

st.title("📊 Dashboard Financeiro Interativo")


conn = get_connection()

df = pd.read_sql("""
    SELECT
        e.nome AS empresa,
        l.mes,
        l.receita,
        l.despesas,
        l.impostos,
        (l.receita - l.despesas - l.impostos) AS lucro
    FROM lancamentos l
    JOIN empresas e ON e.id = l.empresa_id
""", conn)

conn.close()

if df.empty:
    st.info("Nenhum dado cadastrado.")
    st.stop()


ordem_meses = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]
df["mes"] = pd.Categorical(df["mes"], categories=ordem_meses, ordered=True)


st.sidebar.header("Filtros")

empresa_sel = st.sidebar.selectbox(
    "Empresa",
    ["Todas"] + sorted(df["empresa"].unique())
)

mes_sel = st.sidebar.multiselect(
    "Mês",
    ordem_meses,
    default=df["mes"].dropna().unique().tolist()
)

metrica = st.sidebar.selectbox(
    "Métrica",
    {
        "Receita": "receita",
        "Despesas": "despesas",
        "Impostos": "impostos",
        "Lucro": "lucro"
    }.items(),
    format_func=lambda x: x[0]
)[1]

grafico = st.sidebar.selectbox(
    "Tipo de gráfico",
    [
        "Barra",
        "Linha",
        "Área",
        "Barra Empilhada",
        "Pizza",
        "Donut",
        "Histograma",
        "Boxplot",
        "Dispersão",
        "Heatmap"
    ]
)


if empresa_sel != "Todas":
    df = df[df["empresa"] == empresa_sel]

df = df[df["mes"].isin(mes_sel)]
df = df.sort_values("mes")

if df.empty:
    st.warning("Nenhum dado para os filtros selecionados.")
    st.stop()

#tipos de graficos
st.subheader("📈 Visualização")

if grafico == "Barra":
    fig = px.bar(df, x="mes", y=metrica)

elif grafico == "Linha":
    fig = px.line(df, x="mes", y=metrica)

elif grafico == "Área":
    fig = px.area(df, x="mes", y=metrica)

elif grafico == "Dispersão":
    fig = px.scatter(df, x="mes", y=metrica, color="empresa")

elif grafico == "Barra Empilhada":
    dados = df.groupby(["mes","empresa"])[metrica].sum().reset_index()
    fig = px.bar(dados, x="mes", y=metrica, color="empresa")

elif grafico == "Pizza":
    dados = df.groupby("empresa")[metrica].sum().reset_index()
    fig = px.pie(dados, names="empresa", values=metrica)

elif grafico == "Donut":
    dados = df.groupby("empresa")[metrica].sum().reset_index()
    fig = px.pie(dados, names="empresa", values=metrica, hole=0.4)

elif grafico == "Histograma":
    fig = px.histogram(df, x=metrica)

elif grafico == "Boxplot":
    fig = px.box(df, x="empresa", y=metrica)

elif grafico == "Heatmap":
    dados = df.pivot_table(
        index="empresa",
        columns="mes",
        values=metrica,
        aggfunc="sum"
    )
    fig = px.imshow(dados, text_auto=True)


fig.update_layout(
    title=f"{grafico} — {metrica.capitalize()}",
    xaxis_title="Mês",
    yaxis_title=metrica.capitalize()
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("📋 Dados Detalhados")
st.dataframe(
    df.sort_values(["empresa","mes"]),
    use_container_width=True
)
