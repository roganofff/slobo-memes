from pydantic_settings import BaseSettings

from typing import Optional

class Settings(BaseSettings):
    BOT_TOKEN: str
    BOT_WEBHOOK_PATH: str

    BOT_FASTAPI_HOST: Optional[str]
    BOT_FASTAPI_PORT: int

    BOT_RABBIT_PORT: int
    BOT_RABBIT_DEFAULT_USER: str
    BOT_RABBIT_DEFAULT_PASS: str

    IMAGE_HOST_API_KEY: str

    @property
    def bot_webhook_url(self) -> str:
        return f'{self.BOT_FASTAPI_HOST}:{self.BOT_FASTAPI_PORT}/{self.BOT_WEBHOOK_PATH}'

    @property
    def rabbit_url(self) -> str:
        auth = f'{self.BOT_RABBIT_DEFAULT_USER}:{self.BOT_RABBIT_DEFAULT_PASS}'
        return f'amqp://{auth}@rabbitmq:{self.BOT_RABBIT_PORT}/'

    class Config:
        env_file = 'config/.env'


settings = Settings()
