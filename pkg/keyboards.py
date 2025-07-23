from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


class Builder:
    @staticmethod
    def create_keyboard(name_buttons: list | dict, *sizes: int) -> types.InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()
        if type(name_buttons) is list:
            for name_button in name_buttons:
                keyboard.button(text=name_button, callback_data=name_button)
        elif type(name_buttons) is dict:
            for name_button in name_buttons:
                if (
                        "http" in name_buttons[name_button]
                        or "@" in name_buttons[name_button]
                ):
                    keyboard.button(text=name_button, url=name_buttons[name_button])
                else:
                    keyboard.button(
                        text=name_button, callback_data=name_buttons[name_button]
                    )

        if len(sizes) == 0:
            sizes = (1,)
        keyboard.adjust(*sizes)
        return keyboard.as_markup(resize_keyboard=True, one_time_keyboard=True)

    @staticmethod
    def create_reply_keyboard(
            name_buttons: list,
            one_time_keyboard: bool = False,
            request_contact: bool = False,
            *sizes,
    ) -> types.ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardBuilder()
        for name_button in name_buttons:
            if name_button is not tuple:
                keyboard.button(text=name_button, request_contact=request_contact)
            else:
                keyboard.button(text=name_button, request_contact=request_contact)
        if len(sizes) == 0:
            sizes = (1,)
        keyboard.adjust(*sizes)
        return keyboard.as_markup(
            resize_keyboard=True, one_time_keyboard=one_time_keyboard
        )


class Keyboards:
    @property
    def start(self):
        buttons = {
            "Поехали ✅": "start_questioned"
        }

        return Builder.create_keyboard(buttons)

    @property
    def cities(self):
        buttons = {
            "Москва": "Москва",
            "Екатеринбург": "Екатеринбург",

        }
        return Builder.create_keyboard(buttons)

    @property
    def ai_levels(self):
        buttons = {
            "1 — нет опыта": "1",
            "2 — начальный": "2",
            "3 — уверенный пользователь": "3",
            "4 — продвинутый пользователь": "4",
        }
        return Builder.create_keyboard(buttons)

    @property
    def confirm_mailing(self):
        buttons = {
            "Отправить": "mailing_confirm",
        }
        return Builder.create_keyboard(buttons)
keyboards: Keyboards = Keyboards()
