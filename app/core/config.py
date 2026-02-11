from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    bot_token: str = Field(..., alias="BOT_TOKEN")
    topgg_token: str | None = Field(None, alias="TOPGG_TOKEN")
    db_url: str = Field(..., alias="DB_URL")

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )


config = Config() # pyright: ignore[reportCallIssue]
