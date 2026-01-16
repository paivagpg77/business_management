import streamlit as st 

st.set_page_config(
    page_title='Gerenciamento Fiscal',
    page_icon='📊',
    layout='wide'
)

st.title('Sistema de Gerenciamento Fiscal')
st.markdown('Gerencie os dados fiscais da sua empresa aqui , e visualize os indicadores da sua empresa.')
st.divider()

st.info(
    'Use o menu à esquerda para: \n'
    '-Cadastrar sua Empresa\n'
    '-Lançar dados fiscais\n'
    '-Visualizar Gráficos'
)