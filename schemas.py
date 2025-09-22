from pydantic import BaseModel
from datetime import datetime
from typing import Literal

# ===================
# Esquemas de Token
# ===================
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    role: str | None = None

# ===================
# Esquemas de Utilizador
# ===================
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    role: str = "user"

class User(UserBase):
    id: int
    role: str

    class Config:
        from_attributes = True

# --- NOVO ESQUEMA ADICIONADO AQUI ---
class UserPublic(BaseModel):
    """Esquema para a lista pública de utilizadores, expondo apenas o necessário."""
    username: str
    role: str

    class Config:
        from_attributes = True

# ===================
# Esquemas de Inventário
# ===================
class StockItemBase(BaseModel):
    name: str

class StockItemCreate(StockItemBase):
    pass

class StockItem(StockItemBase):
    id: int
    quantity: int
    created_by_username: str

    class Config:
        from_attributes = True

class StockMovement(BaseModel):
    type: Literal['entrada', 'saida']
    quantity: int

# ===================
# Esquemas de Log
# ===================
class LogEntry(BaseModel):
    id: int
    timestamp: datetime
    username: str
    action: str

    class Config:
        from_attributes = True

