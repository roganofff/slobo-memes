"""Config module."""

from typing import Optional

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Provides settings for telegram api, rabbitmq and db connections."""

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
        """Return the bot webhook URL.

        Returns:
            str: URL of the bot webhook.
        """
        return (
            f'{self.BOT_FASTAPI_HOST}:{self.BOT_FASTAPI_PORT}/{self.BOT_WEBHOOK_PATH}'
        )

    @property
    def rabbit_url(self) -> str:
        """Return the RabbitMQ URL with authentication.

        Returns:
            str: URL of the RabbitMQ.
        """
        auth = f'{self.BOT_RABBIT_DEFAULT_USER}:{self.BOT_RABBIT_DEFAULT_PASS}'
        return f'amqp://{auth}@rabbitmq:{self.BOT_RABBIT_PORT}/'

    model_config = ConfigDict(env_file='config/.env')


settings = Settings()
