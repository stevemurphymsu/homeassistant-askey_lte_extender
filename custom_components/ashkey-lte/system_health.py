"""System health for ASKEY LTE."""
from homeassistant.components import system_health
from homeassistant.core import HomeAssistant, callback
from .const import DOMAIN

@callback
def async_register(hass: HomeAssistant, register: system_health.SystemHealthRegistration) -> None:
    """Register system health callbacks."""
    register.async_register_info(system_health_info)

async def system_health_info(hass: HomeAssistant) -> dict[str, any]:
    """Get system health info."""
    client = None
    for entry_id, data in hass.data[DOMAIN].items():
        client = data
        break

    data = {
        "api_reachable": "ok" if client and await client.get_about_status() else "error"
    }

    return data