import pandas as pd
from joblib import dump
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV


data = pd.read_csv("../scripts/data-engineering.csv")

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


dump(modelo_grid, 'SVR_model.joblib')
