````markdown
# Sistema de Gestão de Estoque

Sistema web completo para gestão de estoque, 
desenvolvido com FastAPI e PostgreSQL, 
totalmente containerizado com Docker 
para facilitar o deploy e garantir portabilidade.

A aplicação permite controle de usuários 
com níveis diferentes de permissão, 
gestão de inventário e relatórios detalhados 
com exportação para Excel.

---

## Índice

- [Visão Geral da Arquitetura](#visão-geral-da-arquitetura)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Guia de Deploy (Servidor de Produção)](#guia-de-deploy-servidor-de-produção)
- [Credenciais Padrão](#credenciais-padrão)

---

## Visão Geral da Arquitetura

A aplicação é orquestrada pelo Docker Compose 
e é composta por três serviços principais 
que se comunicam numa rede interna Docker:

- **db:** Container que executa o banco de dados PostgreSQL, 
utilizando a imagem oficial e persistindo dados em volume Docker.
- **app:** Container que executa a aplicação FastAPI, 
construído a partir de uma imagem customizada definida no Dockerfile, 
processando toda a lógica de negócio.
- **nginx:** Container que atua como Proxy Reverso, 
único ponto de entrada na porta 80, 
encaminhando as requisições para o serviço `app`.

Essa arquitetura garante portabilidade, 
segurança e funcionamento consistente 
em qualquer máquina com Docker.

---

## Tecnologias Utilizadas

- **Backend:** Python 3.11, FastAPI  
- **Banco de Dados:** PostgreSQL  
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5  
- **Proxy Reverso:** NGINX  
- **Containerização:** Docker, Docker Compose  
- **ORM:** SQLAlchemy  
- **Autenticação:** JWT (JSON Web Tokens) com bcrypt para senhas criptografadas  
- **Configuração:** Pydantic Settings com arquivos `.env`  
- **Servidor ASGI:** Uvicorn  
- **Exportação de Dados:** Pandas & openpyxl  

---

## Guia de Deploy (Servidor de Produção)

### Pré-requisitos no Servidor

Garanta que o servidor (Linux ou Windows) tenha Git e Docker instalados.

#### Ubuntu/Debian

```bash
sudo apt update
sudo apt install -y git docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER  # será necessário logout/login para aplicar
````

#### Windows 11 / Windows Server

* Instale [Git for Windows](https://git-scm.com/download/win)
* Instale [Docker Desktop](https://docs.docker.com/desktop/install/windows-install/) com backend WSL 2 ativado
* Certifique-se que "Start Docker Desktop when you log in" está ativado

---

### Passo 1: Clonar o Repositório

Clone o repositório e entre na pasta do projeto:

```bash
git clone https://github.com/sidneylcarneiro/estoque-afya.git
cd estoque-afya
```

---

### Passo 2: Criar Configuração do NGINX

Crie a pasta `nginx` na raiz do projeto:

```bash
mkdir nginx
```

Crie o arquivo `nginx/nginx.conf` com o conteúdo:

```nginx
events {}
http {
    server {
        listen 80;

        # Rota para a aplicação de Estoque
        location /estoque/ {
            rewrite ^/estoque/(.*)$ /$1 break;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_pass http://app:8000;
        }
    }
}
```

---

### Passo 3: Configurar Variáveis de Ambiente

Crie o arquivo `.env` na raiz do projeto e configure as variáveis de ambiente 
(lembre-se de usar valores fortes e únicos):

```env
SECRET_KEY="SUA_CHAVE_SECRETA_DE_PRODUCAO_MUITO_FORTE_AQUI"
DATABASE_URL="postgresql://admin:SENHA_FORTE_PARA_O_BANCO_DE_DADOS@db:5432/estoque_db"
ADMIN_DEFAULT_USERNAME="admin"
ADMIN_DEFAULT_PASSWORD="SENHA_FORTE_PARA_O_BANCO_DE_DADOS"
ROOT_PATH="/estoque"
```

> **Importante:** Nunca commit o arquivo `.env` com dados sensíveis no GitHub. 
Adicione `.env` ao `.gitignore` para evitar isso.

---

### Passo 4: Construir e Executar a Aplicação

Use o Docker Compose para construir e iniciar os containers:

```bash
docker-compose up --build -d
```

---

### Passo 5: Verificar o Funcionamento

Confira o status dos containers:

```bash
docker-compose ps
```

Os containers `db`, `app` e `nginx` devem estar com status `Up`.

---

### Passo 6: Acessar a Aplicação

Acesse no navegador:

* Aplicação Web: `http://<ENDERECO_IP_DO_SERVIDOR>/estoque`
* Documentação da API: `http://<ENDERECO_IP_DO_SERVIDOR>/estoque/docs`

---

## Credenciais Padrão

* Usuário: `admin`
* Senha: conforme definido em `ADMIN_DEFAULT_PASSWORD` no arquivo `.env`

---

