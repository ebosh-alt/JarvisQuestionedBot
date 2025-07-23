from typing import Literal, List, Annotated

from pydantic import Field, field_validator
from pydantic_settings import SettingsConfigDict, BaseSettings, NoDecode

from config.settings.base import ConfigBase


class TelegramConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="tg_")
    bot_token: str
    bot_link: str
    admins: Annotated[List[int], NoDecode]

    @field_validator('admins', mode='before')
    def decode_numbers(cls, v: str) -> List[int]:
        return [int(id) for id in v.split(" ")]

class DatabaseConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="db_")

    type: Literal["SQLITE", "POSTGRES"]

    sqlite_host: str = ""

    postgres_dbms: str = "postgresql"
    postgres_driver: str = "asyncpg"
    postgres_user: str = "postgres"
    postgres_password: str = "password"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_name: str = "database"

    @property
    def link_connect(self) -> str:
        if self.type == "SQLITE":
            return self.sqlite_host
        return f"{self.postgres_dbms}+{self.postgres_driver}://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_name}"



class ProjectConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="project_")
    name: str
    chat_id: int



class Config(BaseSettings):
    telegram: TelegramConfig = Field(default_factory=TelegramConfig)
    db: DatabaseConfig = Field(default_factory=DatabaseConfig)
    project: ProjectConfig = Field(default_factory=ProjectConfig)

    @classmethod
    def load(cls) -> "Config":
        return cls()