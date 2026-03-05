from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN
from .api import AskeyLTEApi
import aiohttp
import logging

_LOGGER = logging.getLogger(__name__)

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
                vol.Required("password"): str
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
                return self.async_create_entry(
                    title="ASKEY LTE",
                    data={
                        "ip_address": user_input["ip_address"],
                        "password": user_input["password"]
                    }
                )
            errors["base"] = "auth_failed"

        # Get current config entry
        current_entry = self.hass.config_entries.async_get_entry(self.context["entry_id"])

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
            }),
            errors=errors
        )
