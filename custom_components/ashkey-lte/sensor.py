from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.entity import EntityCategory
from homeassistant.exceptions import ConfigEntryNotReady
from datetime import timedelta
import logging
import asyncio

from .const import DOMAIN, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback
) -> None:
    api = hass.data[DOMAIN]["api"]

    async def async_update_data():
        try:
            alarm_data = await api.get_alarm_log()
            reboot_data = await api.get_reboot_log()
            about_data = await api.get_about_status()

            latest_alarm = alarm_data["alarmHistoryList"][-1]
            latest_reboot = reboot_data["rebootHistoryList"][-1]

            # Store for other use if needed
            hass.data[DOMAIN]["last_alarm"] = latest_alarm
            hass.data[DOMAIN]["last_reboot"] = latest_reboot

            return {
                "alarm": latest_alarm,
                "reboot": latest_reboot,
                "about": about_data
            }

        except Exception as err:
            _LOGGER.exception("Unexpected error fetching askey-lte data")
            raise UpdateFailed(f"Error communicating with ASKEY API: {err}") from err

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="askey-lte sensor",
        update_method=async_update_data,
        update_interval = timedelta(seconds=DEFAULT_SCAN_INTERVAL),
    )

    await coordinator.async_config_entry_first_refresh()

    entities = [
        AskeySensor(coordinator, "Last Alarm", "alarmName", "alarm"),
        AskeySensor(coordinator, "Last Reboot", "rebootReason", "reboot"),
        AskeySensor(coordinator, "Uptime", "uptime", "about"),
        AskeySensor(coordinator, "GPS Status", "gpsStatus", "about")
    ]

    async_add_entities(entities)

class AskeySensor(SensorEntity):
    def __init__(self, coordinator, name, key, section):
        self.coordinator = coordinator
        self._attr_name = f"ASKEY LTE {name}"
        self._attr_unique_id = f"askey_{section}_{key}"
        self.key = key
        self.section = section
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def native_value(self):
        data = self.coordinator.data.get(self.section, {})
        return data.get(self.key)
