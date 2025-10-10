from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Carrega e valida as configurações da aplicação a partir de variáveis de ambiente.
    """
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    ROOT_PATH: str = ""

    DATABASE_URL: str

    ADMIN_DEFAULT_USERNAME: str
    ADMIN_DEFAULT_PASSWORD: str

    model_config = SettingsConfigDict(env_file=".env", extra='ignore')

settings = Settings()

