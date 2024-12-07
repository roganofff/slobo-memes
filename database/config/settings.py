from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    DB_RABBIT_PORT: int
    DB_RABBIT_DEFAULT_USER: str
    DB_RABBIT_DEFAULT_PASS: str

    IMAGE_HOST_API_KEY:str

    @property
    def db_url(self) -> str:
        protocol='postgresql+asyncpg'
        user_data = f'{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}'
        server_data = f'{self.POSTGRES_HOST}:{self.POSTGRES_PORT}'
        return f'{protocol}://{user_data}@{server_data}/{self.POSTGRES_DB}'

    @property
    def rabbit_url(self) -> str:
        auth = f'{self.DB_RABBIT_DEFAULT_USER}:{self.DB_RABBIT_DEFAULT_PASS}'
        return f'amqp://{auth}@rabbitmq:{self.DB_RABBIT_PORT}/'

    class Config:
        env_file = 'config/.env'


settings = Settings()
