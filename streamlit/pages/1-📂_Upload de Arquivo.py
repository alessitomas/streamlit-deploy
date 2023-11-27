import streamlit as st
import pandas as pd

st.title('Upload de um arquivo CSV')


uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv", help='Dataset em formato de arquivo CSV, será usado para as vizualizações.')

if uploaded_file is not None:
    # Read the uploaded CSV file
    df = pd.read_csv(uploaded_file)
    
    # Display the dataframe
    st.write(df)

