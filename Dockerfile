# Dockerfile

# Usando a imagem oficial do Python
FROM python:3.12-slim


RUN pip install poetry

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

# Configurações de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Diretório de trabalho
WORKDIR /code

# Copia os arquivos do Poetry
COPY pyproject.toml poetry.lock /code/

RUN poetry lock --no-update

# Instalar as dependências com o Poetry
RUN poetry config virtualenvs.create false \
    && poetry install

# Copia o código fonte para o contêiner
COPY . /code/

# RUN echo "from authentication.models import User; User.objects.create_superuser(email='admin@checkersgame.com', password='admin', nickname='admin', first_name='Admin', last_name='User')" | poetry run python manage.py shell
