from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from loguru import logger

from config import Config
from internal.app.app import bot
from internal.entities.database import users, User
from internal.entities.models import Participants
from internal.filters.Filters import IsAdmin
from pkg.get_message import get_mes
from pkg.google_client import GoggleClient
from pkg.keyboards import keyboards

router = Router()

config = Config.load()


def analyze(participants: Participants) -> dict[str, dict[str, list[dict[str, str]]]]:
    result = {}
    for vl in participants.root:
        if not result.get(vl.city):
            result[vl.city] = {}

        if not result[vl.city].get(vl.team):
            result[vl.city][vl.team] = []
        result[vl.city][vl.team].append({"id": vl.id, "full_name": vl.full_name})
    for city, teams in result.items():
        result[city] = {k: v for k, v in sorted(teams.items())}
    return result


@router.message(Command("send"), IsAdmin())
async def send_message(message: Message):
    user_id = message.from_user.id
    participants = await GoggleClient.get_all_table_users()
    data = analyze(participants)
    mail_text = ""
    dates = {"Москва": "МОСКВА 09.08",
             "Екатеринбург": "ЕКАТЕРИНБУРГ 10.08"}
    for city in data:
        text = get_mes("mailing", data=data[city], date=dates[city])
        mail_text += text + "\n" + 40 * "-" + "\n"
    await bot.send_message(chat_id=user_id,
                           text=mail_text + "\n\nОтправить пользователям текст?",
                           reply_markup=keyboards.confirm_mailing)


@router.callback_query(F.data == "mailing_confirm")
async def confirm_mailing(message: CallbackQuery):
    participants = await GoggleClient.get_all_table_users()
    data = analyze(participants)
    texts = {}
    dates = {"Москва": "МОСКВА 09.08",
             "Екатеринбург": "ЕКАТЕРИНБУРГ 10.08"}
    for city in data:
        if city == "":
            continue
        if city not in texts:
            texts[city] = get_mes("mailing", data=data[city], date=dates.get(city, ""))
        for team in data[city]:
            for user in data[city][team]:
                try:
                    await bot.send_message(chat_id=user["id"],
                                           text=texts[city])
                    logger.info(f"{user["id"]} | {city}")
                except:
                    pass


mailing_rt = router
