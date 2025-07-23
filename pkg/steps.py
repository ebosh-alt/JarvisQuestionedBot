from typing import Literal, Optional, List, Any
from aiogram.types import InlineKeyboardMarkup
from pydantic import BaseModel

from pkg.keyboards import keyboards


class StepField(BaseModel):
    name: str
    prompt: str
    field_type: Optional[Literal["string", "integer", "float", "date_range", "list"]] = "string"
    keyboard: InlineKeyboardMarkup | Any = None


class StepsSchema(BaseModel):
    steps: List[StepField]


steps_schema = StepsSchema(steps=[
    StepField(
        name="city",
        prompt="📍 В каком городе ты будешь участвовать в мероприятии?",
        keyboard=keyboards.cities,
    ),
    StepField(
        name="full_name",
        prompt="📝 Как тебя зовут? (Имя и фамилия полностью)",
    ),
    StepField(
        name="age",
        prompt="📆 Сколько тебе лет?",
    ),
    StepField(
        name="position",
        prompt="💼 Какая у тебя должность?",
    ),
    StepField(
        name="ai_level",
        prompt=(
            "🤖 Оцени уровень владения нейросетями:\n"
            "1 — нет опыта\n"
            "2 — начальный\n"
            "3 — уверенный пользователь\n"
            "4 — продвинутый пользователь\n"
        ),
        keyboard=keyboards.ai_levels,  # опционально
    )
])
