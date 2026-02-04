# """Configuration management for the Todo backend application."""

# from pydantic_settings import BaseSettings, SettingsConfigDict
# from typing import List


# class Settings(BaseSettings):
#     """Application settings loaded from environment variables."""

#     # Database
#     database_url: str

#     # OpenAI
#     openai_api_key: str

#     # Authentication
#     better_auth_secret: str
#     jwt_algorithm: str = "HS256"
#     jwt_expiry_days: int = 7

#     # CORS
#     cors_origins: str = "http://localhost:3000"

#     # Server
#     debug: bool = False
#     log_level: str = "INFO"

#     model_config = SettingsConfigDict(
#         env_file=".env",
#         env_file_encoding="utf-8",
#         case_sensitive=False,
#     )

#     @property
#     def cors_origins_list(self) -> List[str]:
#         """Parse CORS origins from comma-separated string."""
#         return [origin.strip() for origin in self.cors_origins.split(",")]


# # Global settings instance
# settings = Settings()



"""Configuration management for the Todo backend application."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    database_url: str

    # AI Providers
    openai_api_key: Optional[str] = None   # ✅ optional now
    gemini_api_key: Optional[str] = None   # ✅ added

    # Authentication
    better_auth_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expiry_days: int = 7

    # CORS
    cors_origins: str = "http://localhost:3000"

    # Server
    debug: bool = False
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",   # 🔥 MOST IMPORTANT
    )

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]


# Global settings instance
settings = Settings()
