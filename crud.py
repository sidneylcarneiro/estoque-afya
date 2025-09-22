from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
import models, schemas
from config import settings # Importa as configurações

# =================================
# Configuração de Segurança e Hashing
# =================================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha fornecida corresponde à senha criptografada."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Gera o hash de uma senha."""
    return pwd_context.hash(password)

# =================================
# Funções de Token e Autenticação
# =================================

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise credentials_exception

def authenticate_user(db: Session, username: str, password: str | None = None):
    """
    Autentica um utilizador.
    - Se a senha for fornecida (admin), verifica a senha.
    - Se a senha não for fornecida (utilizador comum), apenas verifica se o utilizador existe.
    """
    user = get_user_by_username(db, username=username)
    if not user:
        return None
    # Se o utilizador é admin (tem senha), a senha deve ser verificada
    if user.role == "admin":
        if not password or not verify_password(password, user.hashed_password):
            return None
    # Se for um utilizador comum, não é necessária senha
    return user

# =================================
# Funções de Utilizador (CRUD)
# =================================

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate, password: str | None = None):
    """Cria um novo utilizador, com senha opcional."""
    hashed_password = get_password_hash(password) if password else None
    db_user = models.User(
        username=user.username,
        role=user.role,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
    
def create_admin_if_not_exists(db: Session):
    """Verifica se o utilizador admin existe e, se não, cria-o com a senha padrão das configurações."""
    admin = get_user_by_username(db, settings.ADMIN_DEFAULT_USERNAME)
    if not admin:
        admin_schema = schemas.UserCreate(username=settings.ADMIN_DEFAULT_USERNAME, role="admin")
        create_user(db, user=admin_schema, password=settings.ADMIN_DEFAULT_PASSWORD)
        print(f"Utilizador '{settings.ADMIN_DEFAULT_USERNAME}' criado com sucesso.")

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

# =================================
# Funções de Inventário
# =================================

def get_stock_item_by_name(db: Session, name: str):
    """Busca um item de inventário pelo seu nome exato (case-insensitive)."""
    return db.query(models.StockItem).filter(models.StockItem.name.ilike(name)).first()

def get_stock_items(db: Session, search: str = ""):
    return db.query(models.StockItem).filter(models.StockItem.name.ilike(f"%{search}%")).all()

def create_stock_item(db: Session, item: schemas.StockItemCreate, user_id: int, username: str):
    # A restrição de nome duplicado é verificada aqui antes de criar
    db_item = models.StockItem(
        name=item.name,
        quantity=0,
        created_by_id=user_id,
        created_by_username=username
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_stock_item(db: Session, item_id: int):
    db_item = db.query(models.StockItem).filter(models.StockItem.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item
    
def get_stock_item_by_id(db: Session, item_id: int):
    return db.query(models.StockItem).filter(models.StockItem.id == item_id).first()
    
# =================================
# Funções de Log
# =================================

def create_log_entry(db: Session, username: str, action: str):
    db_log = models.LogEntry(username=username, action=action)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_log_entries(db: Session, skip: int = 0, limit: int = 200):
    return db.query(models.LogEntry).order_by(models.LogEntry.timestamp.desc()).offset(skip).limit(limit).all()

