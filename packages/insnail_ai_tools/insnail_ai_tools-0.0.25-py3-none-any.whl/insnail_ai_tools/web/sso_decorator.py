# from __future__ import absolute_import
import inspect
from functools import wraps

import redis
import requests
from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from insnail_ai_tools.web.django.response import BaseResponse as DjangoBaseResponse
from insnail_ai_tools.web.fastapi.scheme import BaseResponse

GET_USER_INFO_URL = "http://127.0.0.1:8000/cas/getWeComCustomerInfo"
Config = {"host": "localhost", "port": 6379, "decode_responses": True}
REDIS_TOKEN_KEY = "login_token"
pool = redis.ConnectionPool(
    host=Config["host"],
    port=Config["port"],
    decode_responses=Config["decode_responses"],
)
rd = redis.Redis(connection_pool=pool)


def fast_api_sso(func):
    """
        fast_api 单点登录拦截装饰器
    Args:
        func:

    Returns:

    """

    @wraps(func)
    def fast_api(*args, **kwargs):
        """
            fast_api的装饰器
        Returns:

        """
        authorization = kwargs.get("authorization")
        if authorization and rd.sismember(REDIS_TOKEN_KEY, authorization):
            pass
        else:
            content = BaseResponse()
            content.code = status.HTTP_401_UNAUTHORIZED
            content.msg = "未登录"
            # 返回失败
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=jsonable_encoder(content),
            )
            # pass
        return func(*args, **kwargs)

    @wraps(func)
    async def fast_api_async(*args, **kwargs):
        """
            fast_api的装饰器, 异步
        Returns:

        """
        authorization = kwargs.get("authorization")
        if authorization and rd.sismember(REDIS_TOKEN_KEY, authorization):
            pass
        else:
            content = BaseResponse()
            content.code = status.HTTP_401_UNAUTHORIZED
            content.msg = "未登录"
            # 返回失败
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=jsonable_encoder(content),
            )
            # pass
        res = await func(*args, **kwargs)
        return res

    if inspect.iscoroutinefunction(func):
        return fast_api_async()
    else:
        return fast_api


def django_sso(func):
    """
        django 单点登录装饰器
    Args:
        func:

    Returns:

    """
    from django.http import JsonResponse

    @wraps(func)
    def django(request):
        """
            django的装饰器
        Args:
            request:

        Returns:

        """
        token = request.META.get("HTTP_AUTHORIZATION")
        if token and rd.sismember(REDIS_TOKEN_KEY, token):
            pass
        else:
            # 返回失败
            content = DjangoBaseResponse.get_failure("未登录")
            content["code"] = (status.HTTP_401_UNAUTHORIZED,)
            return JsonResponse(content)
        return func(request)

    return django


def register_middleware(app_):
    """
        注册app中间件
    Args:
        app_:

    Returns:

    """
    app_.middleware("http")(_add_process_time_header)


async def _add_process_time_header(request: Request, call_next):
    """
        拦截登录的中间件
    Args:
        request:
        call_next:

    Returns:

    """
    token = request.headers.get("authorization")
    # print(token)
    if token and rd.sismember(REDIS_TOKEN_KEY, token):
        pass
    else:
        content = BaseResponse()
        content.code = (status.HTTP_401_UNAUTHORIZED,)
        content.msg = "未登录"
        # 返回失败
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED, content=jsonable_encoder(content)
        )
    response = await call_next(request)
    return response


def get_user_info_by_token(token: str):
    """
        通过token获取成员信息
    Args:
        token:

    Returns:
        example：
            {
                "code": 0, # 状态码
                "msg": msg, # 描述语
                "data": {
                    'external_contact_list': [], # 客户列表
                    'external_group_list': [], # 客户群列表
                    'external_behavior_data': [], # 客户联系客户统计数据
                    'external_group_statistic_data': [], # 群聊数据统计数据
                }
            }
    """
    # print('get_user_info_by_token_file', sys.path)
    data = {"token": token}
    res = requests.get(url=GET_USER_INFO_URL, params=data)
    return res.json()
