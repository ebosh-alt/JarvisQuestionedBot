import asyncio
import sys
import textwrap

from loguru import logger

from config import Config
from internal.app.app import dp, bot
from internal.entities.database.base import create_async_database
from internal.handlers import routers
from pkg import middleware
from pkg.logger import set_logger


@logger.catch()
async def run() -> None:
    set_logger()
    await create_async_database()
    # if len(sys.argv) > 1:
    #     if sys.argv[1] == "test_data":
    #         await append_all()
    for router in routers:
        dp.include_router(router)
    dp.update.middleware(middleware.Logging())


    await dp.start_polling(bot)

