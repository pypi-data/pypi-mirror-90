from httpx import AsyncClient

import fsu.internal.error_code as E
from fsu.error import UniversalLogicError


async def get_wxwork_user(corp_id, corp_secret, code, redis):
    redis_key    = f"fsu.wxwork.access_token:<{corp_id}>"
    access_token = await redis.get(redis_key)

    async with AsyncClient() as client:
        # get access_token if not exists
        if access_token is None:
            params = {
                "corpid"     : corp_id,
                "corpsecret" : corp_secret,
            }

            resp = await client.get("https://qyapi.weixin.qq.com/cgi-bin/gettoken", params=params)
            data = resp.json()

            if "errcode" in data and data["errcode"] != 0:
                raise UniversalLogicError(E.LOGIN_FAILED, data["errmsg"])

            access_token = data["access_token"]
            expires_in   = data["expires_in"]

            tr = redis.multi_exec()
            tr.set(redis_key, access_token)
            tr.expire(redis_key, expires_in - 200)
            ok1, ok2 = await tr.execute()
            assert ok1
            assert ok2

        # get user id
        params = {
            "access_token" : access_token,
            "code"         : code,
        }

        resp = await client.get("https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo", params=params)
        data = resp.json()

        if "errcode" in data:
            errcode = data["errcode"]

            # invalid token
            if errcode == 42001:
                await redis.delete(redis_key)
                return await get_wxwork_user(corp_id, corp_secret, code, redis)

            if errcode != 0:
                raise UniversalLogicError(E.LOGIN_FAILED, data["errmsg"])

        if "UserId" not in data:
            raise UniversalLogicError(E.LOGIN_FAILED, "not a member")

        # get user detail
        user_id = data["UserId"]

        params = {
            "access_token" : access_token,
            "userid"       : user_id,
        }

        resp = await client.get("https://qyapi.weixin.qq.com/cgi-bin/user/get", params=params)
        data = resp.json()

        if "errcode" in data:
            errcode = data["errcode"]

            # invalid token
            if errcode == 42001:
                await redis.delete(redis_key)
                return await get_wxwork_user(corp_id, corp_secret, code, redis)

            if errcode != 0:
                raise UniversalLogicError(E.LOGIN_FAILED, data["errmsg"])

        return data


async def get_wechat_user(app_id, app_secret, code):
    async with AsyncClient() as client:
        # get access_token
        params = {
            "appid"      : app_id,
            "secret"     : app_secret,
            "code"       : code,
            "grant_type" : "authorization_code",
        }

        resp = await client.get("https://api.weixin.qq.com/sns/oauth2/access_token", params=params)
        data = resp.json()

        if "errcode" in data and data["errcode"] != 0:
            raise UniversalLogicError(E.LOGIN_FAILED, data["errmsg"])

        access_token = data["access_token"]
        open_id      = data["openid"]

        # get user detail
        params = {
            "access_token" : access_token,
            "openid"       : open_id,
        }

        resp = await client.get("https://api.weixin.qq.com/sns/userinfo", params=params)
        data = resp.json()

        if "errcode" in data and data["errcode"] != 0:
            raise UniversalLogicError(E.LOGIN_FAILED, data["errmsg"])

        return data
