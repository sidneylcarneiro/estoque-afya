
# Sistema de Gestão de Estoque

Este é um sistema web completo para **gestão de estoque**, desenvolvido com **FastAPI** e **PostgreSQL**, e totalmente containerizado com **Docker** para garantir um deploy simples e consistente.

A aplicação permite o controle de usuários com diferentes níveis de permissão, gestão de inventário e um relatório detalhado de todas as atividades com opção de exportação para Excel.

## 🏛️ Visão Geral da Arquitetura

A aplicação é orquestrada pelo **Docker Compose** e é composta por três serviços principais que se comunicam numa rede interna do Docker:

1.  **`db`**: Um container que executa o banco de dados **PostgreSQL**. Ele utiliza a imagem oficial do Postgres e persiste os dados em um volume Docker.
    
2.  **`app`**: Um container que executa a aplicação **FastAPI**. Ele é construído a partir de uma imagem customizada definida no `Dockerfile` e processa toda a lógica de negócio.
    
3.  **`nginx`**: Um container que atua como **Proxy Reverso**. Ele é o único ponto de entrada para a aplicação, recebendo as requisições na porta `80` e encaminhando-as de forma segura para o serviço `app`.
    

Esta arquitetura garante que a aplicação seja portátil, segura e funcione da mesma forma em qualquer máquina que tenha o Docker instalado.

## 🚀 Tecnologias Utilizadas

-   **Backend:** Python 3.11, FastAPI
    
-   **Banco de Dados:** PostgreSQL
    
-   **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
    
-   **Proxy Reverso:** NGINX
    
-   **Containerização:** Docker, Docker Compose
    
-   **ORM:** SQLAlchemy
    
-   **Autenticação:** JWT (JSON Web Tokens) com senhas criptografadas (bcrypt)
    
-   **Configuração:** Pydantic Settings (com arquivos `.env`)
    
-   **Servidor ASGI:** Uvicorn
    
-   **Exportação de Dados:** Pandas & openpyxl
    

## 🛠️ Guia de Deploy (Servidor de Produção)

Siga estes passos para clonar, configurar e executar a aplicação em um servidor definitivo.

### Pré-requisitos no Servidor

Garanta que o seu servidor (Linux ou Windows) tenha o **Git** e o **Docker** instalados.

#### Para Servidor Linux (Ubuntu/Debian)

```
# Atualiza os pacotes e instala o Git, Docker e Docker Compose
sudo apt update
sudo apt install -y git docker.io docker-compose
# Inicia e habilita o serviço do Docker para iniciar com o sistema
sudo systemctl start docker
sudo systemctl enable docker
# Adiciona o seu usuário ao grupo do Docker para não precisar usar 'sudo' (opcional)
# NOTA: Você precisará fazer logout e login novamente para que esta alteração tenha efeito.
sudo usermod -aG docker $USER

```

#### Para Servidor Windows (Windows 11 / Windows Server)

1.  **Instale o Git:** Baixe e instale o [**Git for Windows**](https://git-scm.com/download/win "null").
    
2.  **Instale o Docker Desktop:** Baixe e instale o [**Docker Desktop for Windows**](https://www.docker.com/products/docker-desktop/ "null"). Ele já inclui o **Docker Compose**.
    
    -   Durante a instalação, certifique-se de que a opção para usar o backend **WSL 2** está selecionada.
        
    -   Nas configurações do Docker Desktop, garanta que a opção **"Start Docker Desktop when you log in"** está ativada.
        

### Passo 1: Clonar a Branch de Deploy

Abra o seu terminal (PowerShell no Windows ou o terminal no Linux) e clone **especificamente a branch `afya`**:

```
git clone --branch afya [https://github.com/sidneylcarneiro/estoque-materiais.git](https://github.com/sidneylcarneiro/estoque-materiais.git)
cd estoque-materiais

```

### Passo 2: Criar a Configuração do NGINX

Crie a pasta e o arquivo de configuração para o nosso proxy reverso.

```
# Crie a pasta 'nginx'
mkdir nginx

```

Agora, crie o arquivo`nginx.conf` dentro desta nova pasta (com `notepad nginx/nginx.conf` no Windows ou `nano nginx/nginx.conf` no Linux) e cole o seguinte conteúdo:

```
# nginx/nginx.conf
# Esta configuração permite servir múltiplas aplicações no mesmo servidor.
events {}
http {
    server {
        listen 80;

        # Rota para a aplicação de Estoque
        # Acessível via http://HOSTNAME_DO_SERVIDOR/estoque
        location /estoque/ {
            # Reescreve o URL para remover o /estoque antes de enviar para a aplicação
            rewrite ^/estoque/(.*)$ /$1 break;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            # Encaminha para o serviço 'app' do nosso docker-compose
            proxy_pass http://app:8000;
        }

        # Rota para uma SEGUNDA APLICAÇÃO (exemplo)
        # Acessível via http://HOSTNAME_DO_SERVIDOR/outra-app
        location /outra-app/ {
            # proxy_pass http://nome_do_outro_servico:porta;
        }
    }
}

```

### Passo 3: Configurar as Variáveis de Ambiente

Crie o arquivo`.env` na raiz do projeto.

```
# No Windows (PowerShell):
New-Item .env
# No Linux:
touch .env

```

Edite o arquivo`.env` e cole o seguinte conteúdo, **ajustando os valores para produção**:

```
# .env (Configuração para o Servidor de Produção)

# IMPORTANTE: Gere uma chave nova e segura para o ambiente de produção.
# No Linux, pode usar o comando: openssl rand -hex 32
SECRET_KEY="SUA_CHAVE_SECRETA_DE_PRODUCAO_MUITO_FORTE_AQUI"

# IMPORTANTE: Altere a senha do banco de dados para uma senha forte.
# Esta senha será usada tanto pelo serviço 'db' como pela aplicação.
DATABASE_URL="postgresql://admin:SENHA_FORTE_PARA_O_BANCO_DE_DADOS@db:5432/estoque_db"

# Credenciais padrão para a criação do admin.
ADMIN_DEFAULT_USERNAME="admin"
ADMIN_DEFAULT_PASSWORD="SENHA_FORTE_PARA_O_BANCO_DE_DADOS"

```

### Passo 4: Construir e Executar a Aplicação

Com tudo configurado, use o Docker Compose para orquestrar e iniciar a aplicação.

```
# Constrói a imagem da aplicação e inicia os containers em segundo plano (-d)
docker-compose up --build -d

```

### Passo 5: Verificar o Funcionamento

Para garantir que tudo está a correr como esperado, use o seguinte comando:

```
docker-compose ps

```

Você deverá ver os três containers (`estoque-db`, `estoque-app`, `estoque-proxy`) com o estado `Up` ou `running`.

### Passo 6: Acessar a Aplicação

A sua aplicação está agora online e pronta para ser usada!

-   **Aplicação Web:**  `http://<ENDERECO_IP_DO_SEU_SERVIDOR>/estoque`
    
-   **Documentação da API:**  `http://<ENDERECO_IP_DO_SEU_SERVIDOR>/estoque/docs`
    

#### Credenciais Padrão

-   **Usuário:**  `admin`
    
-   **Senha:** A senha que você definiu em `ADMIN_DEFAULT_PASSWORD` no seu arquivo`.env`.