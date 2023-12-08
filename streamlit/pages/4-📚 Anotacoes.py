import streamlit as st
import pandas as pd
import sys
import os
from dotenv import load_dotenv
import datetime

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
        # Obtenha a data e a hora atual
        now = datetime.datetime.now()
        timestamp = now.strftime("%B %d of %Y at %H:%M:%S")

        # Aqui você pode adicionar o código para salvar as anotações
        # Por exemplo, você pode salvar as anotações em um arquivo:
        with open('notes.txt', 'a') as f:  # Abra o arquivo em modo de anexação
            f.write(f'{timestamp}:   {notes}\n')  # Adicione uma nova linha ao final das anotações
        st.success('Anotações salvas com sucesso!')



# Crie um botão para carregar as anotações
with col1:
    if st.button('Carregar Anotações'):
        with open('notes.txt', 'r') as f:
            notes = f.read().split('\n')

        for i, note in enumerate(notes):  # Obtenha o índice e a anotação
            if note.strip():  # Se a anotação não for vazia
                if ': ' in note:
                    timestamp, note_text = note.split(': ', 1)  # Separe a data e a hora da anotação
                    col1, col2 = st.columns(2)  # Crie duas colunas
                    with col1.container():
                        st.markdown(f'**{timestamp}**')  # Exiba a data e a hora na primeira coluna
                    with col2.container():
                        st.markdown(note_text)  # Exiba a anotação na segunda coluna
                else:
                    st.markdown(note)  # Exiba a anotação sem data e hora
            
        st.success('Anotações carregadas com sucesso!')

# Crie um botão para limpar as anotações
with col3:
    if st.button('Limpar Última Anotação'):
        # Carregar todas as anotações
        with open('notes.txt', 'r') as f:
            notes = f.read().split('\n')

        # Armazenar a última anotação não vazia
        last_note = None
        for note in reversed(notes):
            if note.strip():
                last_note = note
                break

        # Remover a penultima anotação e apagar as anotacoes vazias
        if notes:
            notes = notes[:-2]
            notes = [note for note in notes if note.strip()]

        # Salvar as anotações restantes
        with open('notes.txt', 'w') as f:
            for note in notes:
                f.write(note + '\n')
        
        # Exibir o horário da última anotação removida
        if last_note and ': ' in last_note:
            timestamp, note_text = last_note.split(': ', 1)  # Separe a data e a hora da anotação
            st.markdown(f'Última anotação: **{timestamp}**')  # Exiba a data e a hora

        st.success('Última anotação limpa com sucesso!')

        