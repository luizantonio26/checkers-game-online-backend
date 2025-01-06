# Usando a imagem oficial do Python
FROM python:3.12-slim

# Atualiza o gerenciador de pacotes e instala dependências do sistema
# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

ENV UV_SYSTEM_PYTHON=1
# Configurações de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Define o diretório de trabalho
WORKDIR /code

# Copia os arquivos de configuração do Poetry
COPY pyproject.toml uv.lock ./

# Configura o Poetry para não criar ambientes virtuais
#RUN poetry config virtualenvs.create false

# Instala as dependências do projeto
#RUN poetry install --no-interaction --no-ansi

RUN mkdir -p /app/logs

#RUN pip install hypercorn
# Copia o restante do código fonte para o contêiner
COPY . .
RUN uv sync --frozen --no-cache

# Define o comando padrão
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
