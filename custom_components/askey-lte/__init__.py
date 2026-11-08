from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

import aiohttp
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .api import AskeyLTEApi, create_trace_config
from .const import DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class AskeyDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the ASKEY LTE device."""

    def __init__(
        self, hass: HomeAssistant, config_entry: ConfigEntry, api: AskeyLTEApi
    ) -> None:
        """Initialize."""
        scan_interval = config_entry.data.get("scan_interval", DEFAULT_SCAN_INTERVAL)
        super().__init__(
            hass,
            _LOGGER,
            name="ASKEY LTE Data Coordinator",
            config_entry=config_entry,
            update_interval=timedelta(seconds=scan_interval),
        )
        self.api = api

    async def _async_setup(self):
        """Set up the coordinator

        This is the place to set up your coordinator,
        or to load data, that only needs to be loaded once.

        This method will be called automatically during
        coordinator.async_config_entry_first_refresh.
        """
        try:
            await self.api.authenticate()
        except Exception as err:
            raise ConfigEntryAuthFailed from err

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        try:
            # Fetch updated data
            alarm_log = await self.api.get_alarm_log()
            reboot_log = await self.api.get_reboot_log()
            about_status = await self.api.get_about_status()
            advanced_status = await self.api.get_advanced_status()
            devices_status = await self.api.get_devices_status()
            gps_status = await self.api.get_gps_status()

            return {
                "alarm_log": alarm_log,
                "reboot_log": reboot_log,
                "about_status": about_status,
                "advanced_status": advanced_status,
                "devices_status": devices_status,
                "gps_status": gps_status,
                "alarm_defs": self.api.alarm_defs,
                "reboot_defs": self.api.reboot_defs,
            }
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up ASKEY LTE from a config entry."""
    ip = entry.data.get("ip_address")
    password = entry.data.get("password")

    logging.getLogger(__name__).debug(f"Creating session for API with IP: {ip}")
    session = async_create_clientsession(
        hass,
        verify_ssl=False,
        cookie_jar=aiohttp.CookieJar(unsafe=True),
        trace_configs=[create_trace_config()],
    )

    logging.getLogger(__name__).debug("Loading API")
    api = AskeyLTEApi(ip, password, session)
    logging.getLogger(__name__).debug("Loading AskeyDataUpdateCoordinator")
    coordinator = AskeyDataUpdateCoordinator(hass, entry, api)

    logging.getLogger(__name__).debug("Performing initial data refresh")
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "api": api,
        "coordinator": coordinator,
    }

    logging.getLogger(__name__).debug("Configuring sensors asynchronously")
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    logging.getLogger(__name__).debug("async_setup_entry done")
    return True

    # async_add_entities(
    #    AskeyLTEApi(coordinator) for idx, ent in enumerate(coordinator.data)
    # )


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
