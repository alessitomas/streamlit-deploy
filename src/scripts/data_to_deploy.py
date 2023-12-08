import pandas as pd
from joblib import dump
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV
import os



def modelo(data):

    try:
        for indice, linha in data['status_won'].items():
            if linha == 1:
                data.drop(indice, inplace=True)

        data.reset_index(drop=True, inplace=True)

        X = data.drop(columns=['stay_time'], axis=1)
        y = data['stay_time']

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.25,
            random_state=42,
        )

        pipe_svr = Pipeline([
            ("svr", SVR()),
        ])

        parametros_grid_svr = {
            'svr__kernel': ['linear', 'rbf'],
            'svr__C': [0.1, 1, 10],
            'svr__epsilon': [0.1, 0.2, 0.5],
        }

        modelo_grid = GridSearchCV(pipe_svr, parametros_grid_svr, cv=5, scoring='neg_mean_squared_error', verbose=1, n_jobs=-1)
        modelo_grid.fit(X_train, y_train)

        

        # Verifique se o modelo foi treinado com sucesso
        if hasattr(modelo_grid, 'best_estimator_'):
            print("Modelo treinado com sucesso.")

        # Caminho do arquivo
        caminho_arquivo = os.path.abspath('../notebooks/data/SVR_model.joblib')
        print(f"Salvando modelo em: {caminho_arquivo}")

        # Salvar o modelo
        dump(modelo_grid, caminho_arquivo)

        print("Modelo salvo com sucesso.")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")


ffff = pd.read_csv("../notebooks/data/data-engineering.csv")
print(ffff.shape)
# Chame a função modelo
modelo(ffff)
