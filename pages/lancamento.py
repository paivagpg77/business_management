import streamlit as st
import sqlite3 as sql 

conn = sql.connect('dados.db', check_same_thread=False)
cur = conn.cursor()

empresas = cur.execute('SELECT id , nome FROM empresas').fetchall()

empresa = st.selectbox(
    'Empresa',
    empresas,
    format_func=lambda x: x[1]
)

mes = st.selectbox('Mês', [
    'Jan' , 'Fev' , 'Mar' , 'Abr' ,'Mai' , 'Jun',
    'Jul' , 'Agos' ,'Out' , 'Nov' ,'Dez'
])

receita = st.number_input('Receita' , min_value=0.0)
despesas = st.number_input('Despesas' , min_value=0.0)
impostos = st.number_input('Impostos' , min_value=0.0)


if st.button('Salvar lançamento'):
    cur.execute("""
    INSERT INTO lancamentos (empresa_id , mes , receita , despesas , impostos)
    VALUES (?,?,?,?,?)""" , (empresa[0], mes , receita, despesas , impostos))
    conn.commit()
    st.success("Dados fiscais salvos!")