Sistema de Gestão de Estoque
Este é um sistema web completo para gestão de estoque, desenvolvido com FastAPI e PostgreSQL, e totalmente containerizado com Docker para garantir um deploy simples e consistente.

A aplicação permite o controle de usuários com diferentes níveis de permissão, gestão de inventário e um relatório detalhado de todas as atividades com opção de exportação para Excel.

🏛️ Visão Geral da Arquitetura
A aplicação é orquestrada pelo Docker Compose e é composta por dois serviços principais que se comunicam numa rede interna do Docker:

app: Um container que executa a aplicação FastAPI. Ele é construído a partir de uma imagem customizada definida no Dockerfile e serve a API e a interface web na porta 8000.

db: Um container que executa o banco de dados PostgreSQL. Ele utiliza a imagem oficial do Postgres e persiste os dados em um volume Docker para garantir que não haja perda de dados.

Esta arquitetura garante que a aplicação seja portátil e funcione da mesma forma em qualquer máquina que tenha o Docker instalado.

🚀 Tecnologias Utilizadas
Backend: Python 3.11, FastAPI

Banco de Dados: PostgreSQL

Frontend: HTML5, CSS3, JavaScript, Bootstrap 5

Containerização: Docker, Docker Compose

ORM: SQLAlchemy

Autenticação: JWT (JSON Web Tokens) com senhas criptografadas (bcrypt)

Configuração: Pydantic Settings (com arquivos .env)

Servidor ASGI: Uvicorn

Exportação de Dados: Pandas & openpyxl

🛠️ Guia de Deploy (Servidor de Produção)
Siga estes passos para clonar, configurar e executar a aplicação em um servidor definitivo.

Pré-requisitos no Servidor
Garanta que o seu servidor (Linux ou Windows) tenha o Git e o Docker instalados.

Para Servidor Linux (Ubuntu/Debian)
# Atualiza os pacotes e instala o Git, Docker e Docker Compose
sudo apt update
sudo apt install -y git docker.io docker-compose
# Inicia e habilita o serviço do Docker para iniciar com o sistema
sudo systemctl start docker
sudo systemctl enable docker
# Adiciona o seu usuário ao grupo do Docker para não precisar usar 'sudo' (opcional)
# NOTA: Você precisará fazer logout e login novamente para que esta alteração tenha efeito.
sudo usermod -aG docker $USER

Para Servidor Windows (Windows 11 / Windows Server)
Instale o Git: Baixe e instale o Git for Windows.

Instale o Docker Desktop: Baixe e instale o Docker Desktop for Windows. Ele já inclui o Docker Compose.

Durante a instalação, certifique-se de que a opção para usar o backend WSL 2 está selecionada.

Nas configurações do Docker Desktop, garanta que a opção "Start Docker Desktop when you log in" está ativada para que a aplicação reinicie com o servidor.

Passo 1: Clonar a Branch de Deploy
Abra o seu terminal (PowerShell no Windows ou o terminal no Linux) e clone especificamente a branch afya:

git clone --branch afya [https://github.com/sidneylcarneiro/estoque-materiais.git](https://github.com/sidneylcarneiro/estoque-materiais.git)
cd estoque-materiais

Passo 2: Configurar as Variáveis de Ambiente
Crie o arquivo .env que guardará as configurações sensíveis da aplicação.

# No Windows (PowerShell), você pode criar o arquivo com:
New-Item .env

# No Linux, você pode usar:
touch .env

Agora, edite o arquivo .env (com notepad .env no Windows ou nano .env no Linux) e cole o seguinte conteúdo, ajustando os valores para produção:

# .env (Configuração para o Servidor de Produção)

# IMPORTANTE: Gere uma chave nova e segura para o ambiente de produção.
# No Linux, pode usar o comando: openssl rand -hex 32
SECRET_KEY="SUA_CHAVE_SECRETA_DE_PRODUCAO_MUITO_FORTE_AQUI"

# URL de conexão do banco de dados para o ambiente Docker. NÃO ALTERE O HOST 'db'.
# IMPORTANTE: Altere a senha aqui para uma senha forte.
DATABASE_URL="postgresql://admin:SENHA_FORTE_PARA_O_BANCO_DE_DADOS@db:5432/estoque_db"

# Credenciais padrão para a criação automática do usuário administrador.
# A senha do banco de dados e a do admin devem ser as mesmas definidas acima.
ADMIN_DEFAULT_USERNAME="admin"
ADMIN_DEFAULT_PASSWORD="SENHA_FORTE_PARA_O_BANCO_DE_DADOS"

Passo 3: Construir e Executar a Aplicação
Com tudo configurado, use o Docker Compose para orquestrar e iniciar a aplicação.

# Constrói a imagem da aplicação e inicia os containers em segundo plano (-d)
docker-compose up --build -d

Passo 4: Verificar o Funcionamento
Para garantir que tudo está a correr como esperado, use o seguinte comando:

docker-compose ps
