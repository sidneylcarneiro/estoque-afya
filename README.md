
````markdown
# 📦 Sistema de Gestão de Estoque

Este é um sistema web completo para **gestão de estoque**, desenvolvido com **FastAPI** e **PostgreSQL**, e totalmente containerizado com **Docker** para garantir um deploy simples e consistente.

A aplicação permite:

- Controle de usuários com diferentes níveis de permissão  
- Gestão de inventário  
- Relatório detalhado de todas as atividades com **opção de exportação para Excel**

---

## 🏛️ Visão Geral da Arquitetura

A aplicação é orquestrada pelo **Docker Compose** e é composta por dois serviços principais que se comunicam numa **rede interna Docker**:

- **`app`**: Um container que executa a aplicação **FastAPI**, construído a partir de uma imagem customizada definida no `Dockerfile`. Serve a **API** e a **interface web** na porta `8000`.
- **`db`**: Um container que executa o **PostgreSQL**, utilizando a imagem oficial. Os dados são persistidos em um volume Docker, evitando perdas de dados.

> Esta arquitetura garante portabilidade e consistência em qualquer máquina com Docker instalado.

---

## 🚀 Tecnologias Utilizadas

- **Backend**: Python 3.11, FastAPI  
- **Banco de Dados**: PostgreSQL  
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5  
- **Containerização**: Docker, Docker Compose  
- **ORM**: SQLAlchemy  
- **Autenticação**: JWT (JSON Web Tokens) com senhas criptografadas via `bcrypt`  
- **Configuração**: Pydantic Settings com arquivos `.env`  
- **Servidor ASGI**: Uvicorn  
- **Exportação de Dados**: Pandas & openpyxl  

---

## 🛠️ Guia de Deploy (Servidor de Produção)

Siga os passos abaixo para clonar, configurar e executar a aplicação em um servidor de produção.

---

### ✅ Pré-requisitos no Servidor

Garanta que o servidor (Linux ou Windows) tenha o **Git** e o **Docker** instalados.

#### Para Servidor Linux (Ubuntu/Debian)

```bash
# Atualiza os pacotes e instala o Git, Docker e Docker Compose
sudo apt update
sudo apt install -y git docker.io docker-compose

# Inicia e habilita o Docker
sudo systemctl start docker
sudo systemctl enable docker

# (Opcional) Permite rodar docker sem sudo
sudo usermod -aG docker $USER
````

> ℹ️ É necessário **logout/login** após adicionar o usuário ao grupo `docker`.

---

#### Para Servidor Windows (Windows 11 / Windows Server)

1. Instale o Git: [Git for Windows](https://git-scm.com/download/win)
2. Instale o Docker Desktop: [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)

Durante a instalação do Docker:

* Ative a opção para usar o **WSL 2 Backend**
* Nas configurações, ative **"Start Docker Desktop when you log in"**

---

## 📦 Deploy da Aplicação

### 🔁 Passo 1: Clonar a Branch de Deploy

```bash
git clone --branch afya https://github.com/sidneylcarneiro/estoque-materiais.git
cd estoque-materiais
```

---

### 🔐 Passo 2: Configurar as Variáveis de Ambiente

Crie o arquivo `.env` com as configurações sensíveis da aplicação.

#### No Windows (PowerShell)

```powershell
New-Item .env
notepad .env
```

#### No Linux

```bash
touch .env
nano .env
```

Cole o seguinte conteúdo no `.env`, ajustando os valores:

```env
# .env (Configuração para o Servidor de Produção)

# IMPORTANTE: Gere uma chave segura com o comando:
# openssl rand -hex 32
SECRET_KEY="SUA_CHAVE_SECRETA_DE_PRODUCAO_MUITO_FORTE_AQUI"

# NÃO ALTERE O HOST 'db'
DATABASE_URL="postgresql://admin:SENHA_FORTE_PARA_O_BANCO_DE_DADOS@db:5432/estoque_db"

# Credenciais padrão para o usuário administrador
ADMIN_DEFAULT_USERNAME="admin"
ADMIN_DEFAULT_PASSWORD="SENHA_FORTE_PARA_O_BANCO_DE_DADOS"
```

---

### 🏗️ Passo 3: Construir e Executar a Aplicação

Execute o seguinte comando para construir e iniciar os containers:

```bash
docker-compose up --build -d
```

---

### 🔍 Passo 4: Verificar o Funcionamento

Verifique se os containers estão rodando corretamente:

```bash
docker-compose ps
```

---

## ✅ Acesso à Aplicação

Após subir os containers, acesse:

```
http://localhost:8000
```

> Em um servidor remoto, substitua `localhost` pelo IP ou domínio do servidor.

---

## 📤 Exportação de Dados

A aplicação permite exportar relatórios em Excel diretamente via interface, utilizando **Pandas** e **openpyxl**.

---

## 🧑‍💻 Autor

**Sidney L. Carneiro**
[GitHub - sidneylcarneiro](https://github.com/sidneylcarneiro)

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

```
