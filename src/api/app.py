import os
import sys
from flask import Flask, request, jsonify
import joblib
from pymongo import MongoClient
import pandas as pd
from flask import Flask, request, jsonify
from flasgger import Swagger , swag_from
from dotenv import load_dotenv



def processa_df(df):
      
    nome_arquivo_csv = "saida.csv"

    # Salvar o DataFrame em um arquivo CSV
    df.to_csv(nome_arquivo_csv, index=False)
    

    data_real_final = df.drop(columns=["PESSOA_PIPEDRIVE_id_person","stay_time"])

    return data_real_final



mongo_password = os.environ.get('MONGO_PASSWORD')


url = f"mongodb+srv://AnaHealth:{mongo_password}@anahealth.2qbmc6n.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(url)
db_name = client["AnaHealth"]
collection = client["Api-Log"]
load_dotenv()
API_KEY_ANA = os.getenv('API_KEY_ANA')

app = Flask(__name__)
swagger = Swagger(app)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# Carrega o modelo usando um caminho absoluto
model = joblib.load('SVR_model.joblib')

def verificar_api_key():    
    api_key = request.headers.get('X-API-KEY')
    if api_key == API_KEY_ANA:
        return True
    else:
        return False
    
@app.route('/apidocs/')
def apidocs():
    return jsonify(swagger(app))

@app.route('/predict', methods=['POST'])
@swag_from('swagger/predict.yml')
def predict():
    """
    Endpoint para previsão.
    ---
    parameters:
      - name: data
        in: body
        required: true
        type: string
        description: JSON de entrada para previsão.
    responses:
      200:
        description: Resposta bem-sucedida.
        schema:
          properties:
            predicao:
              type: array
              items:
                type: number
    """

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
    
    
    
    data = processa_df(data)
    
    try : 
        
        predicao = model.predict(data)
        
        # if predicao != None:
        #     collection.insert({"features": dados ,"predict": predicao.tolist(), "date" : datetime.now().strftime('%d-%m-%Y')})
        return jsonify({'predicao': predicao.tolist()})

    except Exception:
        return jsonify({'error': 'Erro na predição do modelo'}), 400

if __name__ == '__main__':
    app.run(debug=True)