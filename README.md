
## sprint4-support-vector-team
`Nosso modelo preditivo é capaz de, através de uma robusta tabela de dados fornecida pela empresa Ana Health, estimar o número de horas que o usuário ficará na plataforma desde a data em que ele entrou, com a finalidade de auxiliar a empresa na redução do churn.`


## Stack utilizada

**Dashboard:** Streamlit

**Banco de Dados:** MongoDB

**Back-end:** Pandas, Matplotlib , missingno, pymongo, bcrypt, plotly, scikit learn, python-dotenv, Flask


## Instalação das Dependencias

Crie um ambiente virtual

```bash
  python3 -m venv env
  source env/bin/activate
```

Instale as Dependencias 

```bash
  pip install -r requirements.txt
```
    
## O conjunto de Dados utilizado foi fornecido pela empresa Ana Health

 - [Tabela de Dados](https://docs.google.com/spreadsheets/d/1ku3RbAe_BQFqSxfEgbJARmUMaKEidGqvWo-xh-E7XE0/edit#gid=841451143)

## Pré-processamento  e Feature Engineering dos Dados

O pré-processamento foi realizado nos notebooks contidos
na pasta 'pré-processamento' dentro da pasta 'notebooks', com o objetivo específico de lidar
com valores nulos. Neste sentido, adotamos estratégias como descartar colunas com
muitos valores nulos, consideradas irrelevantes para o modelo, ou preencher esses valores
nulos com o número 0. Também fizemos feature engineering dos dados, onde criamos novas colunas, 
descartamos outras, entre outros procedimentos. Os notebooks relativos à essas atividades estão na 
pasta "feature engineering". As tabelas criadas pelos processos de pré-processamento e feature engineering se 
encontram na pasta "data".

## O modelo

O notebook de treinamento do modelo está contido na pasta `notebooks/modelo_tempo_permanencia.ipynb` , nele foram treinados os algoritmos de `Regressor Linear`, `Random Forest` e `Support Vector Regressor`, juntamente com ajuste de hiperparâmetros com `GridSearch` da biblioteca `scikit-learn`, os resultados obtidos foram

- **Random Forest Regressor**: 
- RMSE: 96.99
- R2: 0.25312721913815717
 - EVS: 0.32890013577762933 
- Erro percentual médio: 15.93% 

- **Support Vector Regressor**: 
- RMSE: 85.63
- R2: 0.4178046750004776 
- EVS: 0.43484915131508506
- Erro percentual médio: 14.06% 

- **Linear Regression**:
- RMSE: 167.07
- R2: -1.2161651340448807
- EVS: -1.1666649285715551 
- Erro percentual médio: 27.43% 

`Utilizamos métricas como RMSE, R2, EVS e o erro percentual médio para avaliação.
RMSE significa “erro quadrático médio”, R2 é o coeficiente de determinação e EVS significa
“explained variance score”.`

Tivemos o melhor desempenho com o algoritmo Support Vector Regressor, com os hiperparâmetros: 
'poly_features__degree': 1, 
'svr__C': 1, 
'svr__epsilon': 0.1, 
'svr__kernel': 'linear'

## Documentação da API

#### Retorna o tempo estimado, em dias, de permanência do usuario na plataforma.

```http
  POST /api/data
```

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `api_key` | `string` | **Obrigatório**. A chave da sua API |



## Autores

- [@st4pzz](https://github.com/st4pzz)
- [@juliapaiva1](https://github.com/juliapaiva1)
- [@alessitomas](https://github.com/alessitomas)
- [@WeeeverAlex](https://github.com/WeeeverAlex)


