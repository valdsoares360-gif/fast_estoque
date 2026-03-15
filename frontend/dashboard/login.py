import streamlit as st
import requests

API_URL = "http://localhost:8000"

def login():

    st.title("🔐 Login")

    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar"):

        response = requests.post(
            f"{API_URL}/auth/login",
            data={
                "username": username,
                "password": password
            }
        )

        if response.status_code == 200:

            token = response.json()["access_token"]

            st.session_state["token"] = token
            st.session_state["logado"] = True

            st.success("Login realizado com sucesso!")
            st.rerun()

        else:
            st.error("Usuário ou senha inválidos")