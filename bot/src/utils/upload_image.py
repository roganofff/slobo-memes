from aiohttp import ClientSession
import asyncio
from typing import Union

from config.settings import settings

URL = 'https://freeimage.host/api/1/upload'

params = {
    'key': settings.IMAGE_HOST_API_KEY,
    'format': 'json',
}


async def get_request(
    session: ClientSession,
    **kwargs,
) -> Union[dict, None]:
    async with session.get(URL, **kwargs) as response:
        if response.status == 200:
            return await response.json()
        return None


async def upload_image(source: str) -> str:
    url = ''
    async with ClientSession() as session:
        this_params = params.copy()
        this_params['source'] = source
        response = await get_request(session, params=this_params)
        if response:
            url = response['image']['display_url']
    return url

asyncio.run(upload_image('https://api.telegram.org/file/bot8182750666:AAF32eZI_ypey1zPQf6fP0K-lkhUDxKs3A8/photos/file_0.jpg'))
