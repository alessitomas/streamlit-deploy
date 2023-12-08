# Usar uma imagem base do Python
FROM python:3.8-slim

# Definir o diretório de trabalho no container
WORKDIR /app

# Copiar os arquivos do projeto para o diretório /app no container
COPY . /app

# Instalar as dependências do projeto
RUN pip install -r requirements.txt

# Expõe a porta que o Flask vai rodar
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["python", "app.py"]
