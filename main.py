import streamlit as st
from db import criar_tabelas

criar_tabelas()

st.set_page_config(page_title="Gestão Empresarial", layout="wide")

st.title("Sistema de Gestão Empresarial")
st.sidebar.success("Selecione uma opção")
