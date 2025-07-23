from typing import List, Literal
from pydantic import BaseModel, Field, RootModel


# Один участник
class Participant(BaseModel):
    id: int | str = Field(alias="id")
    city: int | str = Field(alias="город")
    full_name: int | str = Field(alias="фио")
    age: int | str = Field(alias="возраст")
    position: int | str = Field(alias="должность")            # обратите внимание на пробел в ключе
    ai_level: int | str= Field(alias="уровень в ИИ")
    team: int | str = Field(alias="команда")

    model_config = {
        "populate_by_name": True,     # позволяет создавать объект по имени поля, а не только по алиасу
        "str_strip_whitespace": True,
    }

class Participants(RootModel[List[Participant]]):
    pass



