from pydantic import Field, BaseModel

__all__ = ["TokenArgs"]


class TokenArgs(BaseModel):
    """
    获取 Token 的参数
    """

    server_uri: str = Field(..., title="获取 OAuth2 Token 的地址")
    redirect_uri: str = Field(
        ..., title="跳转 URI", description="授权之后会跳转到这个 URL 并且附带 code & state 参数"
    )
    client_id: str = Field(..., title="客户ID")
    client_secret: str = Field(..., title="客户机密")
    code: str = Field(..., title="授权码")

    grant_type: str = Field(
        "authorization_code", title="授权类型", description="固定值[当前仅仅支持授权码]"
    )
