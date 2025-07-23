import json

from loguru import logger
from aiogram.types import Message, CallbackQuery, FSInputFile
from typing import Any, Awaitable, Callable, Dict
from aiogram.types import TelegramObject

from internal.app.app import bot
from internal.entities.database import users
from pkg.get_message import get_mes
from pkg.keyboards import keyboards as kb

class Logging:
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> None:
        id = None
        try:
            if type(event.message) is Message:
                # logger.info(json.dumps(event.model_dump().get("message"), indent=4, ensure_ascii=False))
                id = event.message.from_user.id
                logger.info(
                    f'{["@" + event.message.from_user.username, event.message.from_user.id]}'
                    f' - message - {event.message.text}')
            else:
                id = event.callback_query.from_user.id
                logger.info(
                    f'{["@" + event.callback_query.from_user.username, event.callback_query.from_user.id]}'
                    f' - callback_query - {event.callback_query.data}')
        except:
            if type(event.message) is Message:
                id = event.message.from_user.id
                logger.info(
                    f'{[event.message.from_user.id]}'
                    f' - message - {event.message.text}')
            else:
                try:
                    id = event.callback_query.from_user.id
                    logger.info(
                        f'{[event.callback_query.from_user.id]}'
                        f' - callback_query - {event.callback_query.data}')
                except:
                    logger.info(f"{[event]}")
        result = await handler(event, data)
        return result
