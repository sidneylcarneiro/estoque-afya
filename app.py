from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List, Annotated
import pandas as pd
import io

# Importações locais, incluindo o novo 'config'
import crud, models, schemas
from database import SessionLocal, engine, Base
from config import settings

# --- AQUI ESTÁ A CORREÇÃO FINAL ---
# Ao criar a aplicação, passamos o root_path das nossas configurações.
app = FastAPI(
    title="Sistema de Gestão de Estoque",
    description="API para gerenciar usuários, estoque e logs de atividades.",
    version="1.0.0",
    root_path=settings.ROOT_PATH
)

# Configuração dos templates
templates = Jinja2Templates(directory="templates")

# Função para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Evento de startup para criar as tabelas e o utilizador admin
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        crud.create_admin_if_not_exists(db)
    finally:
        db.close()

# =================================
# Dependências de Autenticação
# =================================

def get_current_user(token: Annotated[str, Depends(crud.oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = crud.decode_access_token(token, credentials_exception)
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    user = crud.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user

def require_admin(current_user: Annotated[models.User, Depends(get_current_user)]):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Acesso negado: Requer privilégios de administrador.")
    return current_user

def require_regular_user(current_user: Annotated[models.User, Depends(get_current_user)]):
    if current_user.role == "admin":
        raise HTTPException(status_code=403, detail="Ação não permitida para administradores.")
    return current_user

# =================================
# Rotas de Interface (HTML)
# =================================
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root():
    return RedirectResponse(url="/login")

@app.get("/login", response_class=HTMLResponse, include_in_schema=False)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/profile", response_class=HTMLResponse, include_in_schema=False)
async def profile_page(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})

@app.get("/admin", response_class=HTMLResponse, include_in_schema=False)
async def admin_page(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

@app.get("/stock", response_class=HTMLResponse, include_in_schema=False)
async def stock_page(request: Request):
    return templates.TemplateResponse("stock.html", {"request": request})

@app.get("/logs", response_class=HTMLResponse, include_in_schema=False)
async def logs_page(request: Request):
    return templates.TemplateResponse("logs.html", {"request": request})

# =================================
# Endpoints da API de Autenticação e Utilizadores
# =================================

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nome de usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = crud.create_access_token(data={"sub": user.username, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: Annotated[models.User, Depends(get_current_user)]):
    return current_user

@app.get("/public/users", response_model=List[schemas.UserPublic])
def get_public_user_list(db: Session = Depends(get_db)):
    return crud.get_users(db)

@app.get("/userslist", response_model=List[schemas.User], dependencies=[Depends(require_admin)])
def get_user_list(db: Session = Depends(get_db)):
    return crud.get_users(db)

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), current_admin: models.User = Depends(require_admin)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Este nome de usuário já está em uso.")
    
    new_user = crud.create_user(db=db, user=user)
    crud.create_log_entry(db=db, username=current_admin.username, action=f"Criou o usuário '{new_user.username}'")
    return new_user

@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db), current_admin: models.User = Depends(require_admin)):
    user_to_delete = db.query(models.User).filter(models.User.id == user_id).first()
    if not user_to_delete:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    if user_to_delete.role == "admin":
        raise HTTPException(status_code=403, detail="Não é possível excluir a conta de administrador.")
    
    deleted_user = crud.delete_user(db=db, user_id=user_id)
    crud.create_log_entry(db=db, username=current_admin.username, action=f"Excluiu o usuário '{deleted_user.username}' (ID: {user_id})")
    return deleted_user

# =================================
# Endpoints da API de Inventário
# =================================

@app.post("/stock/", response_model=schemas.StockItem, dependencies=[Depends(require_regular_user)])
def create_stock_item(item: schemas.StockItemCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    existing_item = crud.get_stock_item_by_name(db, name=item.name)
    if existing_item:
        raise HTTPException(status_code=400, detail=f"O item '{item.name}' já existe no inventário.")

    new_item = crud.create_stock_item(db=db, item=item, user_id=current_user.id, username=current_user.username)
    crud.create_log_entry(db=db, username=current_user.username, action=f"Criou o item de inventário '{new_item.name}'")
    return new_item

@app.get("/stock/", response_model=List[schemas.StockItem], dependencies=[Depends(require_regular_user)])
def get_stock_list(search: str = "", db: Session = Depends(get_db)):
    return crud.get_stock_items(db, search=search)

@app.put("/stock/{item_id}", response_model=schemas.StockItem, dependencies=[Depends(require_regular_user)])
def update_stock_item_quantity(item_id: int, movement: schemas.StockMovement, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_item = crud.get_stock_item_by_id(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item não encontrado.")
    
    if movement.type == 'entrada':
        db_item.quantity += movement.quantity
    elif movement.type == 'saida':
        if db_item.quantity < movement.quantity:
            raise HTTPException(status_code=400, detail="A quantidade de saída não pode ser maior que o estoque atual.")
        db_item.quantity -= movement.quantity
    
    db.commit()
    db.refresh(db_item)
    action = f"Deu {movement.type} de {movement.quantity} unidades no item '{db_item.name}' (Estoque atual: {db_item.quantity})"
    crud.create_log_entry(db=db, username=current_user.username, action=action)
    return db_item

@app.delete("/stock/{item_id}", response_model=schemas.StockItem, dependencies=[Depends(require_regular_user)])
def delete_stock_item(item_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    item_to_delete = crud.get_stock_item_by_id(db, item_id)
    if not item_to_delete:
        raise HTTPException(status_code=404, detail="Item não encontrado.")
    
    if item_to_delete.quantity > 0:
        raise HTTPException(status_code=400, detail=f"Não é possível excluir o item '{item_to_delete.name}' pois seu estoque não está zerado.")
    
    item_name = item_to_delete.name
    deleted_item = crud.delete_stock_item(db=db, item_id=item_id)
    crud.create_log_entry(db=db, username=current_user.username, action=f"Excluiu o item de inventário '{item_name}'")
    return deleted_item

# =================================
# Endpoints da API de Logs
# =================================

@app.get("/logs/", response_model=List[schemas.LogEntry], dependencies=[Depends(require_admin)])
def get_logs(db: Session = Depends(get_db)):
    return crud.get_log_entries(db)

@app.get("/logs/export/excel", dependencies=[Depends(require_admin)])
def export_logs_to_excel(db: Session = Depends(get_db)):
    logs = crud.get_log_entries(db, limit=10000)
    logs_data = [
        {"ID": log.id, "Data e Hora": log.timestamp.strftime("%Y-%m-%d %H:%M:%S"), "Usuário": log.username, "Ação Realizada": log.action}
        for log in logs
    ]
    df = pd.DataFrame(logs_data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Relatorio_Atividades')
    output.seek(0)
    headers = {'Content-Disposition': 'attachment; filename="relatorio_de_atividades.xlsx"'}
    return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers=headers)

@app.get("/stock/export/excel", dependencies=[Depends(require_regular_user)])
def export_stock_to_excel(search: str = "", db: Session = Depends(get_db)):
    items = crud.get_stock_items(db, search=search)
    stock_data = [
        {"ID do Item": item.id, "Nome do Item": item.name, "Quantidade": item.quantity, "Criado Por": item.created_by_username}
        for item in items
    ]
    df = pd.DataFrame(stock_data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Inventario')
    output.seek(0)
    filename = f"relatorio_inventario_{search}.xlsx" if search else "relatorio_inventario_completo.xlsx"
    headers = {'Content-Disposition': f'attachment; filename="{filename}"'}
    return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers=headers)

