import streamlit as st
import pandas as pd
from db import get_connection

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


st.sidebar.header("Filtros")

empresa_sel = st.sidebar.selectbox(
    "Empresa",
    ["Todas"] + sorted(df["empresa"].unique())
)

mes_sel = st.sidebar.multiselect(
    "Mês",
    ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"],
    default=df["mes"].unique().tolist()
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
        "Área"
    ]
)


if empresa_sel != "Todas":
    df = df[df["empresa"] == empresa_sel]

df = df[df["mes"].isin(mes_sel)]


dados = df.groupby("mes")[metrica].sum()


st.subheader("📈 Visualização")

if grafico == "Barra":
    st.bar_chart(dados, width="stretch")

elif grafico == "Linha":
    st.line_chart(dados, width="stretch")

elif grafico == "Área":
    st.area_chart(dados, width="stretch")


st.subheader("📋 Dados Detalhados")
st.dataframe(df, width="stretch")
