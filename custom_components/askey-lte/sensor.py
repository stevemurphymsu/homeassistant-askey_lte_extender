from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.components.number import NumberDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
import logging
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class AskeyNumber(CoordinatorEntity, SensorEntity):
    def __init__(
        self,
        coordinator,
        name,
        key,
        section,
        list_key=None,
        alarm_id=None,
        device_class=None,
        nativevalue=None,
        unit_of_measurement=None,
        state_class=None,
    ):
        super().__init__(coordinator)
        self._attr_name = name
        self._attr_unique_id = f"askey_{section}_{key}_{alarm_id if alarm_id else ''}".strip("_")
        self.key = key
        self.section = section
        self.list_key = list_key
        self.alarm_id = alarm_id
        self._attr_device_class = device_class
        self._attr_unit_of_measurement = unit_of_measurement
        self._attr_state_class = state_class
        self._value_transform = nativevalue
        _LOGGER.debug(f"Created number {self._attr_name} with unique_id {self._attr_unique_id}")

    @property
    def native_value(self):
        source = self.coordinator.data.get(self.section, {})
        if self.list_key:
            source = source.get(self.list_key, {}) if isinstance(source, dict) else {}

        value = source.get(self.key) if isinstance(source, dict) else None
        if value is None:
            return None

        try:
            if callable(self._value_transform):
                return self._value_transform(value)
        except (TypeError, ValueError):
            _LOGGER.debug("Failed to transform value for %s: %s", self.entity_id, value)

        return value

    @property
    def extra_state_attributes(self):
        return {
            #sn_interval": self.coordinator.update_interval.total_seconds() if self.coordinator.update_interval else None,
            #last_update_success": self.coordinator.last_update_success,
            #last_update_time": self.coordinator.last_update_success and self.coordinator.last_refresh,
            #section": self.section,
            #key": self.key,
        }


class AskeySensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, name, key, section, list_key=None, alarm_id=None):
        super().__init__(coordinator)
        self._attr_name = name
        self._attr_unique_id = f"askey_{section}_{key}_{alarm_id if alarm_id else ''}".strip('_')
        self.key = key
        self.section = section
        self.list_key = list_key
        self.alarm_id = alarm_id
        _LOGGER.debug(f"Created sensor {self._attr_name} with unique_id {self._attr_unique_id}")

    @property
    def native_value(self):
        source = self.coordinator.data.get(self.section, {})
        if self.list_key:
            source = source.get(self.list_key, {}) if isinstance(source, dict) else {}

        value = source.get(self.key) if isinstance(source, dict) else None
        return value

    @property
    def extra_state_attributes(self):
        return {
            #scan_interval": self.coordinator.update_interval.total_seconds() if self.coordinator.update_interval else None,
            #last_update_success": self.coordinator.last_update_success,
            #last_update_time": self.coordinator.last_update_success and self.coordinator.last_refresh,
            #section": self.section,
            #key": self.key,
        }


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback
) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]

    # list of static entity descriptions (alarms added at runtime) https://developers.home-assistant.io/docs/core/entity/number/
    entities= [
        # about_status
        AskeyNumber(name="Uptime", coordinator=coordinator, section="about_status", key="uptime", device_class=NumberDeviceClass.DURATION, unit_of_measurement="s", state_class=SensorStateClass.TOTAL_INCREASING),
        AskeySensor(name="GPS Status", coordinator=coordinator, section="about_status", key="gpsStatus"),
        AskeyNumber(name="GPS Satellites", coordinator=coordinator, section="about_status", key="gpsAmount", device_class=None, state_class=SensorStateClass.MEASUREMENT, nativevalue=int, unit_of_measurement="sat"),
        AskeyNumber(name="Active UE Count", coordinator=coordinator, section="about_status", key="activeUECount", device_class=None, state_class=SensorStateClass.MEASUREMENT, nativevalue=int, unit_of_measurement="count"),
        AskeyNumber(name="GPS Satellites Total", coordinator=coordinator, section="about_status", key="gpsAmountTot", device_class=None, state_class=SensorStateClass.TOTAL, nativevalue=int, unit_of_measurement="sat"),
        AskeyNumber(name="Active UE Count Total", coordinator=coordinator, section="about_status", key="activeUECountTot", device_class=None, state_class=SensorStateClass.TOTAL, nativevalue=int, unit_of_measurement="count"),
        # advanced_status
        AskeySensor(name="EARFCN", coordinator=coordinator, section="advanced_status", key="earfcn"),
        AskeySensor(name="CSG ID", coordinator=coordinator, section="advanced_status", key="csgID"),
        AskeyNumber(name="Percent Min", coordinator=coordinator, section="advanced_status", key="percentMin", device_class=None, state_class=SensorStateClass.MEASUREMENT, nativevalue=int, unit_of_measurement="%"),
        AskeyNumber(name="Cell Type", coordinator=coordinator, section="advanced_status", key="cellType", device_class=None, state_class=SensorStateClass.MEASUREMENT, nativevalue=int, unit_of_measurement="count"),
        AskeyNumber(name="TX dBm Max", coordinator=coordinator, section="advanced_status", key="txDbmMax", device_class=NumberDeviceClass.SIGNAL_STRENGTH, state_class=SensorStateClass.MEASUREMENT, nativevalue=float, unit_of_measurement="dBm"),
        AskeySensor(name="Operation Mode", coordinator=coordinator, section="advanced_status", key="operationMode"),
        AskeyNumber(name="Automatic TX Power Mode", coordinator=coordinator, section="advanced_status", key="automaticTxPwrMode", device_class=None, state_class=SensorStateClass.MEASUREMENT, unit_of_measurement="count"),
        AskeyNumber(name="Turn Off RF", coordinator=coordinator, section="advanced_status", key="turnOffRf", device_class=None, state_class=SensorStateClass.MEASUREMENT, unit_of_measurement="count"),
        AskeyNumber(name="Recommend TX Power", coordinator=coordinator, section="advanced_status", key="recommendTxPower", device_class=NumberDeviceClass.SIGNAL_STRENGTH, state_class=SensorStateClass.MEASUREMENT, nativevalue=float, unit_of_measurement="dBm"),
        AskeySensor(name="HNB Name", coordinator=coordinator, section="advanced_status", key="hnbName"),
        AskeySensor(name="RF Power Mode", coordinator=coordinator, section="advanced_status", key="rfPowerMode"),        AskeyNumber(name="Bandwidth", coordinator=coordinator, section="advanced_status", key="bandwidth", device_class=NumberDeviceClass.FREQUENCY, state_class=SensorStateClass.MEASUREMENT, nativevalue=int, unit_of_measurement="MHz"),
        AskeyNumber(name="TX dBm Min", coordinator=coordinator, section="advanced_status", key="txDbmMin", device_class=NumberDeviceClass.SIGNAL_STRENGTH, state_class=SensorStateClass.MEASUREMENT, nativevalue=float, unit_of_measurement="dBm"),
        AskeyNumber(name="4G Signal", coordinator=coordinator, section="advanced_status", key="FourGsignal", device_class=NumberDeviceClass.SIGNAL_STRENGTH, state_class=SensorStateClass.MEASUREMENT, nativevalue=float, unit_of_measurement="dBm"),
        AskeyNumber(name="TX Power", coordinator=coordinator, section="advanced_status", key="txPower", device_class=NumberDeviceClass.SIGNAL_STRENGTH, state_class=SensorStateClass.MEASUREMENT, nativevalue=float, unit_of_measurement="dBm"),
        AskeyNumber(name="PCI", coordinator=coordinator, section="advanced_status", key="pci", device_class=None, state_class=SensorStateClass.MEASUREMENT, nativevalue=int, unit_of_measurement="count"),
        AskeyNumber(name="ENDC X2", coordinator=coordinator, section="advanced_status", key="endcX2", device_class=None, state_class=SensorStateClass.MEASUREMENT, nativevalue=int, unit_of_measurement="count"),
        # devices_status
        AskeySensor(name="Operation Mode Last 24h", coordinator=coordinator, section="devices_status", key="operationModeLast24Hours"),
        AskeyNumber(name="Emergency Access UE Count Total", coordinator=coordinator, section="devices_status", key="emerAcUECountTot", device_class=None, state_class=SensorStateClass.MEASUREMENT, unit_of_measurement="Total"),
        AskeyNumber(name="Active UE Count Total", coordinator=coordinator, section="devices_status", key="activeUECountTot", device_class=None, state_class=SensorStateClass.TOTAL, unit_of_measurement="Total"),
        AskeyNumber(name="Active UE Count", coordinator=coordinator, section="devices_status", key="activeUECount", device_class=None, state_class=SensorStateClass.MEASUREMENT, unit_of_measurement="Total"),
        AskeySensor(name="Operation Mode Last Hour", coordinator=coordinator, section="devices_status", key="operationModeLastHour"),
        AskeyNumber(name="Emergency Access UE Count", coordinator=coordinator, section="devices_status", key="emerAcUECount", device_class=None, state_class=SensorStateClass.TOTAL, unit_of_measurement="Total"),
        AskeyNumber(name="Active UE Count Member", coordinator=coordinator, section="devices_status", key="activeUECountMem", device_class=None, state_class=SensorStateClass.TOTAL, unit_of_measurement="Total"),
        AskeyNumber(name="Emergency Access UE Count Member", coordinator=coordinator, section="devices_status", key="emerAcUECountMem", device_class=None, state_class=SensorStateClass.MEASUREMENT, unit_of_measurement="Total"),
        # gps_status
        AskeyNumber(name="Longitude", coordinator=coordinator, section="gps_status", key="longi", unit_of_measurement="°"),
        AskeyNumber(name="Latitude", coordinator=coordinator, section="gps_status", key="lati", unit_of_measurement="°")]
    
    _LOGGER.debug("Creating alarm entities")

    #alarm_defs = coordinator.data.get("alarm_defs", {})
    #for alarm_id, alarm_info in alarm_defs.items():
    #    entities.append(
    #        _make_entity(
    #            f"Alarm {alarm_info['alarmName']}",
    #            "alarmState",
    #            "alarm_log",
    #            "alarmHistoryList",
    #            alarm_id=alarm_id,
    #        )
    #    )


    async_add_entities(entities,True)
    _LOGGER.debug("async_add_entities complete")
    return True

