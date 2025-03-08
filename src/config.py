# import os
# from pydantic import BaseSettings, Field

# class Settings(BaseSettings):
#     GITHUB_TOKEN: str = Field(..., env="GITHUB_TOKEN")
#     GITHUB_WEBHOOK_SECRET: str = Field(None, env="GITHUB_WEBHOOK_SECRET")
    
#     OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
#     OPENAI_MODEL: str = Field("gpt-4", env="OPENAI_MODEL")
    
#     LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")
#     MAX_TOKENS_PER_REQUEST: int = Field(4096, env="MAX_TOKENS_PER_REQUEST")
#     REVIEW_COMMENT_PREFIX: str = Field("AI Review: ", env="REVIEW_COMMENT_PREFIX")
    
#     class Config:
#         env_file = ".env"
#         env_file_encoding = "utf-8"

# settings = Settings()
