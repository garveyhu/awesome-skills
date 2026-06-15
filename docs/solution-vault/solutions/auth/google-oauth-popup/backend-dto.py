"""Google OAuth 请求 DTO"""

from pydantic import BaseModel, Field


class GoogleLoginDTO(BaseModel):
    access_token: str = Field(min_length=1, description="Google OAuth access token")
