from aiogram import exceptions

from src.bot import get_bot


async def edit_or_send_message(
    message_args: dict,
    message_id: int | None,
) -> None:
    bot = get_bot()
    if message_id:
        try:
            await bot.edit_message_text(
                message_id=message_id,
                **message_args,
            )
        except exceptions.TelegramBadRequest:
            return
        finally:
            return
    await bot.send_message(**message_args)