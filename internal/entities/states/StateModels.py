from dataclasses import dataclass


@dataclass
class QuestionedData:
    city: str = ""
    full_name: str = ""
    closer_choice: str = ""
    preferred_pattern: str = ""
    attraction_mode: str = ""
    metaphor_preference: str = ""
    ai_level: str = ""
