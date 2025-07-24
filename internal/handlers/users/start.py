from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from config import Config
from internal.app.app import bot
from internal.entities.database import users, User
from pkg.get_message import get_mes
from pkg.keyboards import keyboards

router = Router()

config = Config.load()


@router.callback_query(F.data == "back_start_menu")
@router.message(Command("start"))
async def start(message: Message | CallbackQuery):
    id = message.from_user.id
    user = await users.get(message.from_user.id)
    if not user:
        user = User(
            id=message.from_user.id,
            username=message.from_user.username,
        )
        await users.new(user)
        await bot.send_message(chat_id=id,
                               text=get_mes(f"start"),
                               reply_markup=keyboards.start)
    else:
        await bot.send_message(chat_id=id,
                               text=get_mes(f"reset"),
                               )


start_rt = router
