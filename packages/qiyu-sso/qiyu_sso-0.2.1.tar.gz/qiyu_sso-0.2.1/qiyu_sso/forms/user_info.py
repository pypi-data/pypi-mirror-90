from pydantic import BaseModel, Field

__all__ = ["UserInfoArgs"]


class UserInfoArgs(BaseModel):
    """
    用户信息表单
    """

    server_uri: str = Field(
        "https://user.qiyutech.tech/api/user/info/",
        title="服务器地址",
        description="请求要访问的地址",
    )
    access_token: str = Field(..., title="访问令牌", description="使用此访问令牌可以访问指定用户的信息")
