
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    openai_api_key: str | None = Field(default=None, env="OPENAI_API_KEY")
    anthropic_api_key: str | None = Field(default=None, env="ANTHROPIC_API_KEY")
    tavily_api_key: str | None = Field(default=None, env="TAVILY_API_KEY")
    google_application_credentials: str | None = Field(default=None, env="GOOGLE_APPLICATION_CREDENTIALS")
    google_project_id: str | None = Field(default=None, env="GOOGLE_PROJECT_ID")
    google_location: str | None = Field(default="us-central1", env="GOOGLE_LOCATION")

    openai_smart_model: str = "gpt-4o-mini"
    anthropic_smart_model: str = "claude-3-5-sonnet-latest"
    temperature: float = 0.3

    class Config:
        env_file = ".env"
