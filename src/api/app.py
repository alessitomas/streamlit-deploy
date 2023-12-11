from distutils.command.clean import clean
import os
import sys
import joblib
from pymongo import MongoClient
import pandas as pd
from flask import Flask, request, jsonify
from scripts.data_preprocessing import preprocessing, mergeHeader_Columns
from scripts.data_feature_engineering import feature_engineering

mongo_password = os.environ.get('MONGO_PASSWORD')
ana_api_key = os.environ.get('ANA_API_KEY')

url = f"mongodb+srv://API-SPRINT:{mongo_password}@anahealth.2qbmc6n.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(url)
db_name = client["AnaHealth"]
collection = db_name["Api-Log"]

app = Flask(__name__)

# Carrega o modelo usando um caminho absoluto
model = joblib.load('SVR_model.joblib')

@app.route('/predict', methods=['POST'])
def predict():
    dados_crus = pd.read_csv('dados_recentes.csv')
    dados_crus = mergeHeader_Columns(dados_crus)
    
    if request.headers.get('ana-api-key') != ana_api_key:
        return jsonify({'error': 'Chave de API inválida'}), 401
    try:
        dados = request.get_json()
        if dados is None:
            return jsonify({"erro": "Nenhum dado JSON fornecido."}), 400
    except Exception:
        return jsonify({"erro": f"Erro ao processar a requisição"}), 500
    
    try:
        data = pd.DataFrame([dados])
      
    except Exception:
        return jsonify({"erro": "Erro no formato dos dados."}), 400
    
    dados_crus_merge = pd.concat([dados_crus, data], ignore_index=True)
    cleaned_df = feature_engineering(preprocessing(dados_crus_merge))
    insert_data = {
        "dados": dados, 
        "predicao": model.predict(cleaned_df.tail(1).drop(columns=['stay_time'], axis=1)).tolist(), 
        "real": cleaned_df.tail(1)['stay_time'].tolist()
    }
    try:
        collection.insert_one(insert_data)
    except Exception:
        return jsonify({"erro": "Erro ao inserir os dados no banco de dados."}), 500
    return jsonify({'predicao': model.predict(cleaned_df.tail(1).drop(columns=['stay_time'], axis=1)).tolist(), "real": cleaned_df.tail(1)['stay_time'].tolist()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)