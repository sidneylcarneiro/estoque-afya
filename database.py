from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Importa as configurações do nosso novo arquivo config.py
from config import settings

# A URL do banco de dados agora é lida a partir das configurações,
# que por sua vez lêem do arquivo .env.
# Nenhuma informação sensível fica mais no código.
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

