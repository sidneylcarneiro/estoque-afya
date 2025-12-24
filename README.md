
```markdown
# Sistema de Gestão de Estoque

Sistema web completo para gestão de estoque, desenvolvido com **FastAPI** e **PostgreSQL**, totalmente containerizado com **Docker** para facilitar o deploy e garantir portabilidade.

A aplicação permite controle de usuários com níveis diferentes de permissão, gestão de inventário e geração de relatórios detalhados com exportação para Excel.

---

## 📌 Índice

- [Visão Geral da Arquitetura](#visão-geral-da-arquitetura)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Guia de Deploy](#guia-de-deploy-servidor-de-produção)
- [Credenciais Padrão](#credenciais-padrão)

---

## 🏗️ Visão Geral da Arquitetura

A aplicação é orquestrada pelo **Docker Compose** e é composta por três serviços principais que se comunicam em uma rede interna isolada:

1.  **db:** Container que executa o banco de dados **PostgreSQL**, utilizando volumes para persistência de dados.
2.  **app:** Container que executa a aplicação **FastAPI** (Python 3.11), processando toda a lógica de negócio e regras de inventário.
3.  **nginx:** Atua como **Proxy Reverso**, sendo o único ponto de entrada (porta 80), encaminhando as requisições para o backend.



---

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python 3.11, FastAPI
- **Banco de Dados:** PostgreSQL
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
- **Proxy Reverso:** NGINX
- **Infraestrutura:** Docker & Docker Compose
- **ORM:** SQLAlchemy
- **Autenticação:** JWT (JSON Web Tokens) com criptografia `bcrypt`
- **Exportação de Dados:** Pandas & openpyxl

---

## 🚀 Guia de Deploy (Servidor de Produção)

### Pré-requisitos
Certifique-se de ter o **Git** e o **Docker** instalados em seu servidor (Linux ou Windows).

#### Instalação em Ubuntu/Debian:
```bash
sudo apt update
sudo apt install -y git docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

```

---

### Passo 1: Clonar o Repositório

```bash
git clone [https://github.com/sidneylcarneiro/estoque-afya.git](https://github.com/sidneylcarneiro/estoque-afya.git)
cd estoque-afya

```

### Passo 2: Configurar o NGINX

Crie a pasta e o arquivo de configuração:

```bash
mkdir nginx
nano nginx/nginx.conf

```

Adicione o conteúdo:

```nginx
events {}
http {
    server {
        listen 80;

        location /estoque/ {
            rewrite ^/estoque/(.*)$ /$1 break;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_pass http://app:8000;
        }
    }
}

```

### Passo 3: Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY="SUA_CHAVE_SECRETA_AQUI"
DATABASE_URL="postgresql://admin:SENHA_FORTE@db:5432/estoque_db"
ADMIN_DEFAULT_USERNAME="admin"
ADMIN_DEFAULT_PASSWORD="SENHA_DO_ADMIN"
ROOT_PATH="/estoque"

```

### Passo 4: Executar a Aplicação

Inicie os serviços em modo *detached* (segundo plano):

```bash
docker-compose up --build -d

```

---

## 🔑 Credenciais Padrão

* **URL da Aplicação:** `http://<IP_DO_SERVIDOR>/estoque`
* **Documentação Swagger:** `http://<IP_DO_SERVIDOR>/estoque/docs`
* **Usuário:** `admin`
* **Senha:** Definida no seu arquivo `.env`

```
```
