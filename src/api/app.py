import os
import sys
from flask import Flask, request, jsonify
import joblib
from pymongo import MongoClient
import pandas as pd
from datetime import datetime



def concatena_df(df):
    from scripts.data_feature_engineering import feature_engineering

    from scripts.data_preprocessing import mergeHeader_Columns, preprocessing
    data = pd.read_csv("../notebooks/data/Ana Health_Tabela Modelo Previsão Churn - Tabela.csv")

    data2 = mergeHeader_Columns(data)
    id_person = df["PESSOA_PIPEDRIVE_id_person"]
    data_final = pd.concat([data2,df],axis=0)

    data_pre = preprocessing(data_final)

    data_fe = feature_engineering(data_pre)
    nome_arquivo_csv = "saida.csv"

    # Salvar o DataFrame em um arquivo CSV
    data_fe.to_csv(nome_arquivo_csv, index=False)
    data_real_final = data_fe[data_fe["PESSOA_PIPEDRIVE_id_person"].isin([id_person])]

    data_real_final = data_real_final.drop(columns=["PESSOA_PIPEDRIVE_id_person","stay_time"])

    data_real_final.reset_index(inplace=True)

    return data_real_final


# Adicione o diretório raiz do projeto ao PYTHONPATH
caminho_projeto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, caminho_projeto)

url = "mongodb+srv://AnaHealth:${MONGO_PASSWORD}>@anahealth.2qbmc6n.mongodb.net/?retryWrites=true&w=majority"

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
        # json_serializado = json.dumps(dados, indent=4)  # Use indent para formatar o JSON com recuo

        # # Abre o arquivo em modo de escrita
        # with open('requisicao.json', 'w') as arquivo:
        #     arquivo.write(json_serializado)
        if dados is None:
            return jsonify({"erro": "Nenhum dado JSON fornecido."}), 400
    except Exception:
        return jsonify({"erro": f"Erro ao processar a requisição"}), 500

    try:
        data = pd.DataFrame([dados])
      
    except Exception:
        return jsonify({"erro": "Erro no formato dos dados."}), 400
    
    # dados_preprocessados = preprocessing(data)
    # if dados_preprocessados == False:
    #     return jsonify({'error': 'Erro no pré-processamento dos dados'}), 400
    # print(dados_preprocessados.shape)

    # dados_feature = feature_engineering(dados_preprocessados)

    # print(dados_feature.shape)
    # if dados_feature == False:
    #     return jsonify({'error': 'Erro na feature engineering dos dados'}), 400
    
    
    data_r = concatena_df(data)    

    
    try : 
        
        predicao = model.predict(data_r)
        
        # if predicao != None:
        #     collection.insert({"features": dados ,"predict": predicao.tolist(), "date" : datetime.now().strftime('%d-%m-%Y')})
        return jsonify({'predicao': predicao.tolist()})

    except Exception:
        return jsonify({'error': 'Erro na predição do modelo'}), 400

if __name__ == '__main__':
    app.run(debug=True)