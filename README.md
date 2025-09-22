
````markdown
# Sistema de Gestão de Estoque

Este é um sistema web completo para **gestão de estoque**, desenvolvido com **FastAPI** e **PostgreSQL**.  
A aplicação permite o controle de usuários com diferentes níveis de permissão, gestão de inventário e um relatório detalhado de todas as atividades.

---

## 🚀 Tecnologias Utilizadas

- **Backend:** Python, FastAPI  
- **Banco de Dados:** PostgreSQL  
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5  
- **ORM:** SQLAlchemy  
- **Autenticação:** JWT (JSON Web Tokens)  
- **Configuração:** Pydantic Settings (com arquivos `.env`)  
- **Servidor ASGI:** Uvicorn  
- **Exportação de Dados:** Pandas  

---

## ✅ Pré-requisitos

Antes de começar, garanta que você tem as seguintes ferramentas instaladas na sua máquina:

- Python (versão **3.9** ou superior)  
- Git  
- Docker (**recomendado** para o banco de dados) ou uma instalação local do PostgreSQL  

---

## 🛠️ Guia de Instalação e Execução

### 1. Clonar o Repositório

```bash
git clone https://github.com/sidneylcarneiro/estoque-materiais.git
cd estoque-materiais
````

---

### 2. Configurar o Ambiente Virtual

É uma boa prática usar um ambiente virtual para isolar as dependências do projeto.

```bash
# Criar o ambiente virtual
python -m venv .venv
```

Ativar o ambiente virtual:

* **Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
```

* **macOS/Linux:**

```bash
source .venv/bin/activate
```

---

### 3. Instalar as Dependências

Com o ambiente virtual ativo, instale todas as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

---

### 4. Configurar o Banco de Dados (Usando Docker)

A forma mais simples de rodar o PostgreSQL é usando Docker:

```bash
docker run --name estoque-db -e POSTGRES_PASSWORD=sua_senha_super_segura -p 5432:5432 -d postgres
```

> ⚠️ **Importante:** Substitua `sua_senha_super_segura` por uma senha de sua preferência.

Este comando irá baixar a imagem do PostgreSQL (se necessário) e iniciar um servidor na porta `5432`.

---

### 5. Configurar as Variáveis de Ambiente

A aplicação usa um arquivo `.env` para gerenciar configurações sensíveis.

**a. Criar o arquivo `.env`:**
Na raiz do projeto, crie o arquivo `.env`.

**b. Exemplo de configuração:**

```env
# Arquivo .env

# Chave secreta para a codificação dos tokens JWT.
# Em produção, gere uma chave segura com o comando: openssl rand -hex 32
SECRET_KEY="uma-chave-secreta-muito-forte-e-aleatoria-0123456789"

# URL de conexão do banco de dados.
# Formato: postgresql://USUARIO:SENHA@HOST:PORTA/NOME_DO_BANCO
DATABASE_URL="postgresql://postgres:sua_senha_super_segura@localhost:5432/postgres"

# Credenciais padrão para a criação automática do usuário administrador
ADMIN_DEFAULT_USERNAME="admin"
ADMIN_DEFAULT_PASSWORD="admin"
```

> ⚠️ Se você optou por uma instalação local do PostgreSQL, ajuste a `DATABASE_URL` com as credenciais criadas manualmente.

---

### 6. Executar a Aplicação

Com tudo configurado, inicie o servidor FastAPI:

```bash
uvicorn app:app --reload
```

> O parâmetro `--reload` reinicia o servidor automaticamente sempre que houver alterações nos arquivos.

---

### 7. Acessar a Aplicação

* Aplicação Web: [http://127.0.0.1:8000](http://127.0.0.1:8000)
* Documentação Interativa (Swagger UI): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 👤 Usuário Padrão

Na primeira execução, o sistema cria automaticamente:

* **Usuário:** `admin`
* **Senha:** `admin`

Você já pode fazer login e começar a usar o sistema!