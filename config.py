from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Carrega e valida as configurações da aplicação a partir de variáveis de ambiente.
    """
    # Configurações da Aplicação
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Configurações do Banco de Dados
    DATABASE_URL: str

    # Credenciais Padrão do Admin
    ADMIN_DEFAULT_USERNAME: str
    ADMIN_DEFAULT_PASSWORD: str

    # Configuração para ler a partir de um arquivo .env
    model_config = SettingsConfigDict(env_file=".env", extra='ignore')

# Cria uma instância única das configurações que será usada em toda a aplicação
settings = Settings()
