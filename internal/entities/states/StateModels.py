from dataclasses import dataclass


@dataclass
class QuestionedData:
    city: str = ""
    full_name: str = ""
    age: str = ""
    position: str = ""
    ai_level: str = ""
