from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    """
    Settings class. Contains all the settings from environment.
    """

    DB_URL: str

    API_HOST: str
    API_PORT: int

    LOG_LEVEL: str | int
    LOG_FORMAT: str

    IS_DEBUG: bool

    model_config = SettingsConfigDict(
        env_file=".env",
    )


settings = Settings()
