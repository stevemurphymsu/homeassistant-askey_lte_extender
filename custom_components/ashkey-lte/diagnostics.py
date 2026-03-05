"""Diagnostics support for ASKEY LTE."""
from __future__ import annotations

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_PASSWORD

from .const import DOMAIN

TO_REDACT = {CONF_PASSWORD}

async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict:
    """Return diagnostics for a config entry."""
    api = hass.data[DOMAIN][entry.entry_id]
    
    diagnostics_data = {
        "entry": {
            "title": entry.title,
            "data": async_redact_data(entry.data, TO_REDACT),
        },
        "about_status": await api.get_about_status(),
        "alarm_log": await api.get_alarm_log(),
        "reboot_log": await api.get_reboot_log(),
        "alarm_definitions": api.alarm_defs,
        "reboot_definitions": api.reboot_defs,
    }

    return diagnostics_data