import argparse
import json
import logging
import time
from http.cookies import SimpleCookie

import aiohttp
import py_mini_racer

_LOGGER = logging.getLogger(__name__)


class AskeyLTEApi:
    def __init__(self, ip, password, session: aiohttp.ClientSession):
        self.ip = ip
        self.password = password
        self.session = session
        self.alarm_defs = {}
        self.reboot_defs = {}

    @property
    def headers(self):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Requested-With": "XMLHttpRequest",
        }
        return headers

    def base_url(self, path=""):
        if path.startswith("data/") or path.startswith("js/"):
            return f"https://{self.ip}/{path}"  # direct root path
        return f"https://{self.ip}/webapi/{path}?_={str(int((time.time()) * 1000))}"

    async def authenticate(self):
        expires_ts = str(int((time.time() + 1800) * 1000))
        js_code = await self.fetch_data("js/common.js?v=v3.6.0408", return_json=False)
        if not isinstance(js_code, str):
            raise RuntimeError("Unable to retrieve ASKEY login script")
        sha256_start = js_code.find("function sha256")
        if sha256_start < 0:
            raise RuntimeError("ASKEY login script does not contain sha256")
        sha256result = py_mini_racer.MiniRacer().eval(
            js_code[sha256_start:] + f" sha256({json.dumps(self.password)})"
        )
        async with self.session.post(
            f"https://{self.ip}/webapi/login",
            params={"expires": expires_ts, "password": sha256result},
            headers=self.headers,
            ssl=False,
        ) as response:
            response.raise_for_status()
            data = await response.json()
            if data.get("result") != 1:
                raise Exception(f"ASKEY Device Error: {data.get('message')}")
            self.session.cookie_jar.update_cookies(
                response.cookies, response_url=response.url
            )
            await self.cache_metadata()
        return {}

    async def fetch_data(self, endpoint, return_json=True):
        try:
            url = self.base_url(endpoint)
            headers = self.headers.copy()
            xsrf_cookie = self.session.cookie_jar.filter_cookies(url).get(
                "X-XSRF-TOKEN"
            )
            if xsrf_cookie:
                headers["X-XSRF-TOKEN"] = xsrf_cookie.value
            async with self.session.get(
                url,
                headers=headers,
                ssl=False,
            ) as response:
                text = await response.text()
                if response.status != 200:
                    _LOGGER.warning(
                        "ASKEY request for %s returned HTTP %s",
                        endpoint,
                        response.status,
                    )
                    return {}
                if return_json:
                    return json.loads(text)
                else:
                    return text
        except Exception as e:
            _LOGGER.error("ASKEY: Exception while fetching %s: %s", endpoint, e)
            return {}

    async def cache_metadata(self):
        self.alarm_defs = await self.fetch_data("data/alarm.json")
        self.reboot_defs = await self.fetch_data("data/reboot.json")

    async def get_alarm_log(self) -> dict:
        return await self.fetch_data("alarmLog")

    async def get_reboot_log(self) -> dict:
        return await self.fetch_data("rebootLog")

    async def get_about_status(self) -> dict:
        return await self.fetch_data("aboutStatus")

    async def get_advanced_status(self) -> dict:
        return await self.fetch_data("advanced")

    async def get_devices_status(self) -> dict:
        return await self.fetch_data("devices")

    async def get_gps_status(self) -> dict:
        return await self.fetch_data("gps")


async def on_request_start(session, trace_config_ctx, params):
    cookies = session.cookie_jar.filter_cookies(params.url)
    _LOGGER.debug(
        "Starting request: %s %s; session cookies: %s",
        params.method,
        params.url.path,
        _cookie_values(cookies),
    )


async def on_request_headers_sent(session, trace_config_ctx, params):
    cookies = SimpleCookie()
    for header in params.headers.getall("Cookie", []):
        cookies.load(header)
    _LOGGER.debug(
        "Sent request: %s %s; cookies: %s",
        params.method,
        params.url.path,
        _cookie_values(cookies),
    )


async def on_request_end(session, trace_config_ctx, params):
    _LOGGER.debug(
        "Ending request: %s %s -> status %s; received cookies: %s",
        params.method,
        params.url.path,
        params.response.status,
        _cookie_values(params.response.cookies),
    )


def _cookie_values(cookies):
    return {name: cookie.value for name, cookie in cookies.items()}


def create_trace_config():
    trace_config = aiohttp.TraceConfig()
    trace_config.on_request_start.append(on_request_start)
    trace_config.on_request_headers_sent.append(on_request_headers_sent)
    trace_config.on_request_end.append(on_request_end)
    return trace_config


async def test_api(ip, password):
    logging.basicConfig(level=logging.DEBUG)
    async with aiohttp.ClientSession(
        cookie_jar=aiohttp.CookieJar(unsafe=True),
        # trace_configs=[create_trace_config()],
    ) as session:
        api = AskeyLTEApi(ip, password, session)
        await api.authenticate()

        # print(f"Alarm Codes: {api.alarm_defs}\n")
        # print(f"Reboot Codes: {api.reboot_defs}\n")
        devices = await api.get_devices_status()
        print(f"About status: {devices}\n\n")
        print(f"Reboot Log: {api.reboot_log}\n\n")
        print(f"Alarm Log: {api.alarm_log}\n\n")


if __name__ == "__main__":
    import asyncio

    parser = argparse.ArgumentParser(description="Test Askey LTE API")
    parser.add_argument("ip", type=str, help="IP address of the Askey LTE device")
    parser.add_argument("password", type=str, help="Password for the Askey LTE device")
    args = parser.parse_args()
    asyncio.run(test_api(args.ip, args.password))
