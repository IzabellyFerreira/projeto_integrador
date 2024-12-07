# Escolha a imagem base
FROM python:3.11-slim

# Defina o diretório de trabalho
WORKDIR /base

# Copie o arquivo de requisitos para o container
COPY requirements.txt .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código da aplicação para o container
COPY . .

# Exponha a porta em que o servidor irá rodar
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver"]
