from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN, DEFAULT_SCAN_INTERVAL
from .api import AskeyLTEApi
import aiohttp
import logging

_LOGGER = logging.getLogger(__name__)

MIN_SCAN_INTERVAL = 30

class AskeyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def _test_credentials(self, ip_address, password):
        """Test if we can authenticate with the host."""
        try:
            session = aiohttp.ClientSession()
            api = AskeyLTEApi(ip_address, password, session)
            await api.authenticate()
            await session.close()
            return True
        except Exception as ex:
            _LOGGER.error("Failed to authenticate: %s", ex)
            return False

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            valid = await self._test_credentials(
                user_input["ip_address"],
                user_input["password"]
            )
            if valid:
                return self.async_create_entry(
                    title="ASKEY LTE",
                    data={
                        "ip_address": user_input["ip_address"],
                        "password": user_input["password"]
                    }
                )
            errors["base"] = "auth_failed"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("ip_address"): str,
                vol.Required("password"): str,
                vol.Required("scan_interval", default=DEFAULT_SCAN_INTERVAL): vol.All(
                    vol.Coerce(int), vol.Range(min=MIN_SCAN_INTERVAL)
                ),
            }),
            errors=errors
        )

    async def async_step_reconfigure(self, user_input=None):
        """Handle reconfiguration of the device."""
        errors = {}
        if user_input is not None:
            valid = await self._test_credentials(
                user_input["ip_address"],
                user_input["password"]
            )
            if valid:
                return self.async_update_reload_and_abort(
                    self._get_reconfigure_entry(),
                    data={
                        "ip_address": user_input["ip_address"],
                        "password": user_input["password"],
                        "scan_interval": user_input.get("scan_interval", DEFAULT_SCAN_INTERVAL),
                    }
                )
            errors["base"] = "auth_failed"

        # Get current config entry
        current_entry = self._get_reconfigure_entry()

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=vol.Schema({
                vol.Required(
                    "ip_address",
                    default=current_entry.data.get("ip_address", "")
                ): str,
                vol.Required(
                    "password",
                    default=current_entry.data.get("password", "")
                ): str,
                vol.Required(
                    "scan_interval",
                    default=current_entry.data.get("scan_interval", DEFAULT_SCAN_INTERVAL),
                ): vol.All(vol.Coerce(int), vol.Range(min=MIN_SCAN_INTERVAL)),
            }),
            errors=errors
        )
