from types import MappingProxyType
from typing import Optional, Self

from aiohttp import ClientSession

from config.settings import settings
from src.bot import get_bot


class Image:
    __API_URL = 'https://api.imgbb.com/1/upload'
    __PARAMS = MappingProxyType(
        {
            'key': settings.IMAGE_HOST_API_KEY,
        },
    )

    def __init__(
        self,
        url: str,
        thumbnail_url: str,
    ) -> None:
        self.__url = url
        self.__thumbnail_url = thumbnail_url

    @property
    def url(self) -> str:
        return self.__url

    @property
    def thumbnail_url(self) -> str:
        return self.__thumbnail_url

    @classmethod
    async def get_object(cls, source: str) -> 'Image':
        url = ''
        thumbnail_url = ''
        async with ClientSession() as session:
            this_params = cls.__PARAMS.copy()
            this_params['image'] = source
            response = await cls.upload(session, params=this_params)
            if response:
                url = response['data']['image']['url']
                thumbnail_url = response['data']['thumb']['url']
        return Image(url, thumbnail_url)

    @classmethod
    async def upload(
        cls,
        session: ClientSession,
        **kwargs,
    ) -> Optional[dict]:
        async with session.get(cls.__API_URL, **kwargs) as response:
            if response.status == 200:
                return await response.json()
            return None

    @classmethod
    async def get_public_url(cls, source: str) -> str:
        url = ''
        if not source:
            return ''
        async with ClientSession() as session:
            this_params = cls.__PARAMS.copy()
            this_params['image'] = source
            response = await cls.upload(session, params=this_params)
            if response:
                url = response['data']['image']['url']
        return url

    @classmethod
    async def get_telegram_url(cls, telegram_file_id: str) -> str:
        bot = get_bot()
        bot_files_url = f'https://api.telegram.org/file/bot{settings.BOT_TOKEN}'
        file_path = (await bot.get_file(telegram_file_id)).file_path
        return f'{bot_files_url}/{file_path}'
