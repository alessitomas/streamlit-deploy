import pandas as pd
from joblib import dump

df = pd.read_csv("../notebooks/data/data-engineering.csv")

dump(df, 'SVR_model.joblib')
