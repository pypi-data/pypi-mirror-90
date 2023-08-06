import time

from fastapi import Header

from insnail_ai_tools.web.sso_decorator import fast_api_sso


@fast_api_sso
def func1(authorization: str = Header(None)):
    time.sleep(1)
    return 1


def test_fast_api_sso():
    func1()
    assert True
