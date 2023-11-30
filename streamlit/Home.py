import streamlit as st
import sys
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente de um arquivo .env
load_dotenv()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '', 'utils')))

from helper_functions import create_user, logged_out_option,  verify_credentials, add_log

url = os.getenv('URL_DB')
db_name = "AnaHealth"
collection_name_user = "User"
collection_name_log = "Log"
collection_name_dataset = "Dataset"

st.title('Bem vindo ao AnaHealth Dashboard')

logged_out_option()


if 'show_signup' not in st.session_state:
    st.session_state.show_signup = False

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = None

if 'Admin' not in st.session_state:
    st.session_state.Admin = False

if st.session_state.show_signup and st.session_state.Admin:
    st.header("Cadastrar")
    with st.form("signup_form"):
        username_signup = st.text_input('Username', key="signup_username")
        password_signup = st.text_input('Senha', type='password', key="signup_password")
        role_singup = st.selectbox('Role', ['User', 'Admin'])
        submitted_signup = st.form_submit_button("Cadastro")
        if submitted_signup:
            status, message = create_user(url, db_name, collection_name_user, username_signup, password_signup, role_singup)
            if status:
                add_log(url, db_name, collection_name_log, st.session_state.logged_in, f"Cadastro de {username_signup}")
                st.success(message)
            else:
                st.error(message)
            
    if st.button('Faça Log In com outra conta'):
        st.session_state.show_signup = False
        st.rerun()

else:
    st.header("Login")
    with st.form("login_form"):
        username_login = st.text_input('Username', key="login_username")
        password_login = st.text_input('Senha', type='password', key="login_password")
        submitted_login = st.form_submit_button("Login")
        if submitted_login:
            status, status_message, role = verify_credentials(url, db_name, collection_name_user, username_login, password_login)
            if status:
                st.success(status_message)
                st.session_state.logged_in = username_login
                if role == 'Admin':
                    st.session_state.Admin = True
                else:
                    st.session_state.Admin = False
                add_log(url, db_name, collection_name_log, username_login, "Login")
                
                st.rerun()
            else:
                st.error(status_message)


    if st.session_state.Admin and st.button('Cadastrar nova conta'):
        st.session_state.show_signup = True
        st.rerun()