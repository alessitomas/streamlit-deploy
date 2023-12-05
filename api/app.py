from flask import Flask, request, jsonify
import joblib
from ..src.scripts.data_preprocessing import preprocessing
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy


from ..src.scripts.data_feature_engineering import feature_engineering

load_dotenv()

API_KEY_ANA = os.getenv('API_KEY_ANA')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///log_Ana_Health.db'
db = SQLAlchemy(app)

model = joblib.load('./src/scripts/SVR_model.joblib')

def verificar_api_key():    
    api_key = request.headers.get('X-API-KEY')
    if api_key == API_KEY_ANA:
        return True
    else:
        return False

@app.route('/predict', methods=['POST'])
def predict():
    from model import Log
    if not verificar_api_key():
        return jsonify({'error': 'Acesso negado'}), 403
    
    dados = request.json
    dados_preprocessados= preprocessing(dados)
    dados_feature = feature_engineering(dados_preprocessados)
    novo_log = Log(data=str(dados))
    db.session.add(novo_log)
    db.session.commit()
    predicao = model.predict(dados_feature)
    return jsonify({'predicao': predicao.tolist()})

if __name__ == '__main__':
    app.run(debug=True)
