from aiohttp import ClientSession
from typing import Union, Self
from types import MappingProxyType

from config.settings import settings
from src.bot import get_bot


class Image:
    __API_URL = 'https://freeimage.host/api/1/upload'
    __PARAMS = MappingProxyType(
        {
            'key': settings.IMAGE_HOST_API_KEY,
            'format': 'json',
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
    async def get_object(cls, source: str) -> Self:
        url = ''
        thumbnail_url = ''
        async with ClientSession() as session:
            this_params = cls.__PARAMS.copy()
            this_params['source'] = source
            response = await cls.upload(session, params=this_params)
            if response:
                url = response['image']['image']['url']
                thumbnail_url = response['image']['thumb']['url']
        return Image(url, thumbnail_url)


    @classmethod
    async def upload(
        cls,
        session: ClientSession,
        **kwargs,
    ) -> Union[dict, None]:
        async with session.get(cls.__API_URL, **kwargs) as response:
            if response.status == 200:
                return await response.json()
            return None

    @classmethod
    async def get_public_url(cls, source: str) -> str:
        url = ''
        async with ClientSession() as session:
            this_params = cls.__PARAMS.copy()
            this_params['source'] = source
            response = await cls.upload(session, params=this_params)
            if response:
                url = response['image']['image']['url']
        return url

    @classmethod
    async def get_telegram_url(cls, telegram_file_id: str) -> str:
        bot = get_bot()
        bot_files_url = f'https://api.telegram.org/file/bot{settings.BOT_TOKEN}'
        file_path = (await bot.get_file(telegram_file_id)).file_path
        return f'{bot_files_url}/{file_path}'
