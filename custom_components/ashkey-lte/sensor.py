from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import EntityCategory
import logging

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback
) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]

    entities = [
        AskeySensor(coordinator, "Last Alarm", "alarmName", "alarm_log", "alarmHistoryList"),
        AskeySensor(coordinator, "Last Reboot Reason", "rebootReason", "reboot_log", "rebootHistoryList"),
        # About Status sensors
        AskeySensor(coordinator, "Uptime", "uptime", "about_status"),
        AskeySensor(coordinator, "GPS Status", "gpsStatus", "about_status"),
        AskeySensor(coordinator, "GPS Satellites", "gpsAmount", "about_status"),
        AskeySensor(coordinator, "Active UE Count", "activeUECount", "about_status"),
        AskeySensor(coordinator, "GPS Satellites Total", "gpsAmountTot", "about_status"),
        AskeySensor(coordinator, "Active UE Count Total", "activeUECountTot", "about_status"),
        # Advanced sensors
        AskeySensor(coordinator, "EARFCN", "earfcn", "advanced_status"),
        AskeySensor(coordinator, "CSG ID", "csgID", "advanced_status"),
        AskeySensor(coordinator, "Percent Min", "percentMin", "advanced_status"),
        AskeySensor(coordinator, "Cell Type", "cellType", "advanced_status"),
        AskeySensor(coordinator, "TX dBm Max", "txDbmMax", "advanced_status"),
        AskeySensor(coordinator, "Operation Mode", "operationMode", "advanced_status"),
        AskeySensor(coordinator, "Automatic TX Power Mode", "automaticTxPwrMode", "advanced_status"),
        AskeySensor(coordinator, "Turn Off RF", "turnOffRf", "advanced_status"),
        AskeySensor(coordinator, "Recommend TX Power", "recommendTxPower", "advanced_status"),
        AskeySensor(coordinator, "HNB Name", "hnbName", "advanced_status"),
        AskeySensor(coordinator, "RF Power Mode", "rfPowerMode", "advanced_status"),
        AskeySensor(coordinator, "Bandwidth", "bandwidth", "advanced_status"),
        AskeySensor(coordinator, "TX dBm Min", "txDbmMin", "advanced_status"),
        AskeySensor(coordinator, "4G Signal", "FourGsignal", "advanced_status"),
        AskeySensor(coordinator, "TX Power", "txPower", "advanced_status"),
        AskeySensor(coordinator, "PCI", "pci", "advanced_status"),
        AskeySensor(coordinator, "ENDC X2", "endcX2", "advanced_status"),
        # Devices sensors (excluding HourlyCapacityUsed)
        AskeySensor(coordinator, "Operation Mode Last 24h", "operationModeLast24Hours", "devices_status"),
        AskeySensor(coordinator, "Peak Connected Users Last 24h", "peakConnectedUsersLast24Hours", "devices_status"),
        AskeySensor(coordinator, "Peak Capacity Used Last 24h Total", "peakCapacityUsedLast24HoursTot", "devices_status"),
        AskeySensor(coordinator, "Emergency Access UE Count Total", "emerAcUECountTot", "devices_status"),
        AskeySensor(coordinator, "Active UE Count Total", "activeUECountTot", "devices_status"),
        AskeySensor(coordinator, "Peak Capacity Used Last 24h", "peakCapacityUsedLast24Hours", "devices_status"),
        AskeySensor(coordinator, "Peak Connected Users Last 24h Event Time", "peakConnectedUsersLast24HoursEventTime", "devices_status"),
        AskeySensor(coordinator, "Peak Connected Users Last Hour Member", "peakConnectedUsersLastHourMem", "devices_status"),
        AskeySensor(coordinator, "Active UE Count", "activeUECount", "devices_status"),
        AskeySensor(coordinator, "Peak Capacity Used Last Hour Member", "peakCapacityUsedLastHourMem", "devices_status"),
        AskeySensor(coordinator, "Peak Capacity Used Last Hour Total", "peakCapacityUsedLastHourTot", "devices_status"),
        AskeySensor(coordinator, "Operation Mode Last Hour", "operationModeLastHour", "devices_status"),
        AskeySensor(coordinator, "Peak Capacity Used Last Hour", "peakCapacityUsedLastHour", "devices_status"),
        AskeySensor(coordinator, "Emergency Access UE Count", "emerAcUECount", "devices_status"),
        AskeySensor(coordinator, "Peak Capacity Used Last 24h Member", "peakCapacityUsedLast24HoursMem", "devices_status"),
        AskeySensor(coordinator, "Active UE Count Member", "activeUECountMem", "devices_status"),
        AskeySensor(coordinator, "Peak Connected Users Last Hour Total", "peakConnectedUsersLastHourTot", "devices_status"),
        AskeySensor(coordinator, "Peak Connected Users Last Hour", "peakConnectedUsersLastHour", "devices_status"),
        AskeySensor(coordinator, "Peak Connected Users Last 24h Member", "peakConnectedUsersLast24HoursMem", "devices_status"),
        AskeySensor(coordinator, "Peak Connected Users Last 24h Total", "peakConnectedUsersLast24HoursTot", "devices_status"),
        AskeySensor(coordinator, "Emergency Access UE Count Member", "emerAcUECountMem", "devices_status"),
        # GPS sensors
        AskeySensor(coordinator, "GPS Satellites Total", "gpsAmountTot", "gps_status"),
        AskeySensor(coordinator, "GPS Satellites", "gpsAmount", "gps_status"),
        AskeySensor(coordinator, "GPS Signal", "gpsSignal", "gps_status"),
        AskeySensor(coordinator, "GPS Status", "gpsStatus", "gps_status"),
        AskeySensor(coordinator, "Longitude", "longi", "gps_status"),
        AskeySensor(coordinator, "Latitude", "lati", "gps_status")
    ]

    alarm_defs = coordinator.data.get("alarm_defs", {})
    for alarm_id, alarm_info in alarm_defs.items():
        entities.append(AskeySensor(coordinator, f"Alarm {alarm_info['alarmName']}", "alarmState", "alarm_log", "alarmHistoryList", alarm_id=alarm_id))

    async_add_entities(entities)

class AskeySensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, name, key, section, list_key=None, alarm_id=None):
        super().__init__(coordinator)
        self._attr_name = f"ASKEY LTE {name}"
        self._attr_unique_id = f"askey_{section}_{key}_{alarm_id if alarm_id else ''}".strip('_')
        self.key = key
        self.section = section
        self.list_key = list_key
        self.alarm_id = alarm_id
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def extra_state_attributes(self):
        if self.alarm_id:
            data = self.coordinator.data.get(self.section, {})
            items = data.get(self.list_key, [])
            for item in reversed(items):
                if item.get("alarmId") == self.alarm_id:
                    return {
                        "alarm_time": item.get("alarmTime"),
                        "alarm_desc": item.get("alarmDesc"),
                        "alarm_id": item.get("alarmId"),
                        "alarm_name": item.get("alarmName")
                    }
            return {}
        return {}

    @property
    def native_value(self):
        data = self.coordinator.data.get(self.section, {})
        if self.alarm_id:
            items = data.get(self.list_key, [])
            for item in reversed(items):  # latest first
                if item.get("alarmId") == self.alarm_id:
                    return item.get(self.key)
            return None
        elif self.list_key:
            items = data.get(self.list_key, [])
            if items:
                value = items[-1].get(self.key)
                if self.section == "reboot_log" and self.key == "rebootReason":
                    reboot_defs = self.coordinator.data.get("reboot_defs", {})
                    return reboot_defs.get(str(value), {}).get("rebootReason", str(value))
                return value
        else:
            return data.get(self.key)
