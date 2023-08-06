from pydantic import Field, BaseModel

from ..values import USER_CENTER_DOMAIN

__all__ = ["LoginArgs"]


class LoginArgs(BaseModel):
    """
    获取登录地址的参数
    """

    server_uri: str = Field(
        f"{USER_CENTER_DOMAIN}/oauth/authorize/", title="OAuth2授权地址"
    )
    client_id: str = Field(..., title="客户ID")

    redirect_uri: str = Field(
        ..., title="跳转 URI", description="授权之后会跳转到这个 URL 并且附带 code & state 参数"
    )
    state: str = Field(..., title="状态", description="请保持唯一性,可以随机生成")
    scope: str = Field(..., title="权限范围", description="申请的权限范围, 多个使用 空格 分隔")

    response_type: str = Field("code", title="返回类型", description="固定值, 当前只支持 授权码 模式")
