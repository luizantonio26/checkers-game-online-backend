# Usando a imagem oficial do Python
FROM python:3.12-slim

# Atualiza o gerenciador de pacotes e instala dependências do sistema
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instala o Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Adiciona o Poetry ao PATH
ENV PATH="/root/.local/bin:$PATH"

# Configurações de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Define o diretório de trabalho
WORKDIR /code

# Copia os arquivos de configuração do Poetry
COPY pyproject.toml poetry.lock ./

# Configura o Poetry para não criar ambientes virtuais
RUN poetry config virtualenvs.create false

# Instala as dependências do projeto
RUN poetry install --no-interaction --no-ansi
RUN mkdir -p /app/logs

RUN pip install hypercorn
# Copia o restante do código fonte para o contêiner
COPY . .

# Define o comando padrão
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
