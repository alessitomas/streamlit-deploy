from email import message
import streamlit as st
import os
from helper_functions import create_user, verify_credentials, logged_out_option

url = os.getenv('MEU_SEGREDO_URL')
db_name = os.getenv('MEU_SEGREDO_DB_NAME')
collection_name = os.getenv('MEU_SEGREDO_COLLECTION_NAME_USER')


st.title('Bem vindo ao AnaHealth Dashboard')

logged_out_option()

if 'show_signup' not in st.session_state:
    st.session_state.show_signup = False

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.show_signup:
    st.header("Cadastrar")
    with st.form("signup_form"):
        username_signup = st.text_input('Username', key="signup_username")
        password_signup = st.text_input('Senha', type='password', key="signup_password")
        submitted_signup = st.form_submit_button("Cadastro")
        if submitted_signup:
            status, message = create_user(url, db_name, collection_name, username_signup, password_signup)
            if status:
                st.success(message)
                st.session_state.logged_in = True
            else:
                st.error(message)
            
    if st.button('Já tem conta? Faça Log In'):
        st.session_state.show_signup = False
        st.rerun()
else:
    st.header("Login")
    with st.form("login_form"):
        username_login = st.text_input('Username', key="login_username")
        password_login = st.text_input('Senha', type='password', key="login_password")
        submitted_login = st.form_submit_button("Login")
        if submitted_login:
            status, status_message = verify_credentials(url, db_name, collection_name, username_login, password_login)
            if status:
                st.session_state.logged_in = True
                st.success(status_message)
                st.rerun()
            else:
                st.error(status_message)

    if st.button('Não tem conta? Cadastrar'):
        st.session_state.show_signup = True
        st.rerun()
