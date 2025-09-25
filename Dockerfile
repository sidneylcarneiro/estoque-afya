# Dockerfile

# Passo 1: Imagem Base
# Começamos com uma imagem oficial do Python. A versão "slim" é menor e otimizada.
FROM python:3.11-slim

# Passo 2: Definir o Diretório de Trabalho
# Define o diretório padrão dentro do container. Todos os comandos seguintes
# serão executados a partir daqui.
WORKDIR /app

# Passo 3: Copiar os Arquivos de Dependências
# Copia apenas o requirements.txt primeiro para otimizar o cache de build.
COPY requirements.txt .

# Passo 4: Instalar as Dependências
# Executa o pip para instalar tudo o que está listado no requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt

# Passo 5: Copiar o Restante do Código
# Agora, copia todos os outros arquivos do projeto (.py, templates, etc.) para o container.
COPY . .

# Passo 6: Expor a Porta
# Informa ao Docker que a aplicação dentro deste container irá escutar na porta 8000.
EXPOSE 8000

# Passo 7: Comando de Execução (Otimizado para Produção)
# Removemos a flag '--reload' para um ambiente mais estável.
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

