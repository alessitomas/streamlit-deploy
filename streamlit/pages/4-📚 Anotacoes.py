import streamlit as st
import pandas as pd
import sys
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente de um arquivo .env
load_dotenv()
# Append the utils directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))

from helper_functions import get_data_from_mongo, check_authentication, logged_out_option


check_authentication()
logged_out_option()

url = os.getenv('URL_DB')
db_name = "AnaHealth"
collection_name_dataset = "Dataset"

df = get_data_from_mongo(url, db_name, collection_name_dataset)

st.title("Anotações")

# Crie uma área de texto para as anotações
notes = st.text_area("Escreva suas anotações aqui...")

# Crie uma coluna para os botões
col1, col2, col3 = st.columns(3)

# Crie um botão para salvar as anotações
with col2:
    if st.button('Salvar Anotações'):
        # Aqui você pode adicionar o código para salvar as anotações
        # Por exemplo, você pode salvar as anotações em um arquivo:
        with open('notes.txt', 'a') as f:  # Abra o arquivo em modo de anexação
            f.write(notes + '\n')  # Adicione uma nova linha ao final das anotações
        st.success('Anotações salvas com sucesso!')


# Crie um botão para carregar as anotações
with col1:
    if st.button('Carregar Anotações'):
        with open('notes.txt', 'r') as f:
            notes = f.read().split('\n')
        st.success('Anotações carregadas com sucesso!')
        for i, note in enumerate(notes):  # Obtenha o índice e a anotação
            if note.strip():  # Se a anotação não for vazia
                st.text_area('', value=note, key=f'note_{i}')  # Use o índice como chave

# Crie um botão para limpar as anotações
with col3:
    if st.button('Limpar Última Anotação'):
        # Carregar todas as anotações
        with open('notes.txt', 'r') as f:
            notes = f.read().split('\n')

        # Remover a penultima anotação e apagar as anotacoes vazias
        if notes:
            notes = notes[:-2]
            notes = [note for note in notes if note.strip()]

        # Salvar as anotações restantes
        with open('notes.txt', 'w') as f:
            for note in notes:
                f.write(note + '\n')

        st.success('Última anotação limpa com sucesso!')