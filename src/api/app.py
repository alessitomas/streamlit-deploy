import os
import sys
from flask import Flask, request, jsonify
import joblib
from dotenv import load_dotenv
from pymongo import MongoClient
import pandas as pd
from datetime import datetime


# Adicione o diretório raiz do projeto ao PYTHONPATH
caminho_projeto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, caminho_projeto)

from scripts.data_preprocessing import preprocessing
from scripts.data_feature_engineering import feature_engineering

load_dotenv()

url = os.getenv("URL_DB")
client = MongoClient(url)
db_name = client["AnaHealth"]
collection = client["Api-Log"]

API_KEY_ANA = os.getenv('API_KEY_ANA')

app = Flask(__name__)


# Carrega o modelo usando um caminho absoluto
model = joblib.load(os.path.join(caminho_projeto, 'notebooks/data/SVR_model.joblib'))

def verificar_api_key():    
    api_key = request.headers.get('X-API-KEY')
    if api_key == API_KEY_ANA:
        return True
    else:
        return False

@app.route('/predict', methods=['POST'])
def predict():
    if not verificar_api_key():
        return jsonify({'error': 'Acesso negado'}), 403
    
    try:
        dados = request.get_json()
        if dados is None:
            return jsonify({"erro": "Nenhum dado JSON fornecido."}), 400
    except Exception:
        return jsonify({"erro": f"Erro ao processar a requisição"}), 500

    try:
        dados = pd.DataFrame([dados])        
        print(dados.head())
    
    except Exception:
        return jsonify({"erro": "Erro no formato dos dados."}), 400
    
    dados_preprocessados = preprocessing(dados)
    if dados_preprocessados == False:
        return jsonify({'error': 'Erro no pré-processamento dos dados'}), 400
    

    dados_feature = feature_engineering(dados_preprocessados)
    if dados_feature == False:
        return jsonify({'error': 'Erro na feature engineering dos dados'}), 400
    
    
    
    try : 
        predicao = model.predict(dados_feature.values.reshape(1, -1))
       

        if predicao != None:
            collection.insert({"features": dados ,"predict": predicao.tolist(), "date" : datetime.now().strftime('%d-%m-%Y')})
            return jsonify({'predicao': predicao.tolist()})

    except Exception:
        return jsonify({'error': 'Erro na predição do modelo'}), 400

if __name__ == '__main__':
    app.run(debug=True)