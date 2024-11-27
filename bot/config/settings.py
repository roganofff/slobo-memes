from pydantic_settings import BaseSettings

from typing import Optional

class Settings(BaseSettings):
    BOT_TOKEN: str
    BOT_WEBHOOK_PATH: str

    WEBHOOK_URL: Optional[str]

    IMAGE_HOST_API_KEY: str

    @property
    def bot_webhook_url(self) -> str:
        return f'{self.WEBHOOK_URL}/{self.BOT_WEBHOOK_PATH}'

    class Config:
        env_file = 'config/.env'


settings = Settings()
