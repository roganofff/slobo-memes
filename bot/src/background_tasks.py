from asyncio import Task
from typing import Any

from aiogram.methods import TelegramMethod

background_tasks: set[Task[TelegramMethod[Any] | None]] = set()