import time
from aiohttp import ClientSession
#from .const import BASE_URL_TEMPLATE, METADATA_PATHS
import json
import logging

_LOGGER = logging.getLogger(__name__)

class AskeyLTEApi:
    def __init__(self, ip, password, session: ClientSession):
        self.ip = ip
        self.password = password
        self.session = session
        self.token = None
        self.xsrf = None
        self.token_expiry = 0
        self.alarm_defs = {}
        self.reboot_defs = {}

    @property
    def headers(self):
        return {
            "Content-Type": "application/json",
            "Authtoken": self.token or "",
            "X-Requested-With": "XMLHttpRequest"
        }

    @property
    def cookies(self):
        return {
            "X-XSRF-TOKEN": self.xsrf,
            "Authtoken": self.token
        }
    
    def base_url(self, path=""):
        if path.startswith("data/"):
            return f"https://{self.ip}/{path}"  # direct root path
        return f"https://{self.ip}/webapi/{path}"

    async def authenticate(self):
        expires_ts = str(int((time.time() + 1800) * 1000))
        try:
            async with self.session.post(f"https://{self.ip}/webapi/login?password={self.password}&expires={expires_ts}", headers=self.headers, ssl=False) as response:            
                data = await response.json()
                self.token = data.get("Authtoken")
                self.token_expiry = data.get("expires")
                self.xsrf = response.cookies.get("X-XSRF-TOKEN")
                await self.cache_metadata()
                self.alarm_log = await self.get_alarm_log()
                self.reboot_log = await self.get_reboot_log()
        except Exception as e:
            _LOGGER.error("ASKEY: Exception during authentication %s", e)
        return {}
        
    async def fetch_data(self, endpoint):
        try:
            async with self.session.get(self.base_url(endpoint), headers=self.headers, cookies=self.cookies, ssl=False) as response:
                text = await response.text()
                return json.loads(text) if response.status == 200 else {}
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

async def test_api():
    async with ClientSession() as session:
        ip=""
        password=""
        api = AskeyLTEApi(ip, password, session)
        await api.authenticate()
        print(f"Alarm Codes: {api.alarm_defs}\n")
        print(f"Reboot Codes: {api.reboot_defs}\n")
        about = await api.get_about_status()
        print(f"About status: {about}\n\n")
        reboot_log = await api.get_reboot_log()
        print(f"Reboot Log: {reboot_log}\n\n")
        alarm_log = await api.get_alarm_log()
        print(f"Alarm Log: {alarm_log}\n\n")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_api())