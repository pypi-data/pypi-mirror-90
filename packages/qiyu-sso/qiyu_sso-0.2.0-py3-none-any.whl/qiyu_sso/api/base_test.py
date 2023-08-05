import secrets
from urllib.parse import urlparse, parse_qs

from forms.login import LoginArgs
from .base import BaseAPI

__all__ = []


def test_get_login_url():
    """
    测试获取登录地址
    :return:
    """
    client_id = secrets.token_hex(20)
    server_uri = "https://www.google.com/oauth"
    redirect_uri = "https://www.facebook.com/demo"
    state = secrets.token_hex(24)
    scope = "read"

    args = LoginArgs(
        server_uri=server_uri,
        client_id=client_id,
        redirect_uri=redirect_uri,
        state=state,
        scope=scope,
    )

    base = BaseAPI()
    url = base.get_login_url(args)
    d = urlparse(url)

    assert d.scheme == "https"
    assert d.netloc == "www.google.com"
    assert d.path == "/oauth"
    q = parse_qs(d.query)

    assert q["response_type"] == ["code"]
    assert q["client_id"] == [client_id]
    assert q["redirect_uri"] == [redirect_uri]
    assert q["scope"] == [scope]
    assert q["state"] == [state]
