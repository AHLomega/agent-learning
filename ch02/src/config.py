"""所有配置集中在这里，其他地方不许直接读环境变量。"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    deepseek_api_key: str
    base_url: str = "https://api.deepseek.com"
    model: str = "deepseek-flash"


settings = Settings()