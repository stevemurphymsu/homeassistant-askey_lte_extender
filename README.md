# ASKEY LTE Network Extender – Home Assistant Integration

System health, usage, alarms, and bandwidth trends from your ASKEY LTE femtocell inside Home Assistant.  This integration is confirmed to work with ASKEY LTE extenders issued by Verzion. 

---

## 🔧 Features

- Real-time LTE signal and transmission metrics
- GPS location, satellite count, and signal quality
- Alarm log decoding + severity mapping
- Reboot reason tracker and event monitoring
- Device usage stats: active UEs, hourly load, peak bandwidth
- Performance monitoring (uplink/downlink)
- Dashboard panels (ApexCharts, Mini Graph Card)
- Config Flow UI for IP + password input
- Auto-refresh token authentication
- Services to manually refresh token or metadata
- Long-term statistics: hourly capacity + historical bandwidth

---

<!-- ha-marketplace:exclude-start -->

## ⚙️ Installation

[![Open your Home Assistant instance and open a repository in the Marketplace.](https://my.home-assistant.io/badges/marketplace_repository.svg)](https://my.home-assistant.io/redirect/marketplace_repository/?owner=stevemurphymsu&repository=homeassistant-askey_lte_extender&category=integration)


[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=askey-l
)

Or install manually:
1. Copy `custom_components/askey_lte` into `config/custom_components/`
2. Restart Home Assistant
3. Go to **Settings > Devices & Services > Add Integration**
4. Search for `ASKEY LTE`

<!-- ha-marketplace:exclude-end -->

---

## 🧩 Configuration

Enter:
- IP address of your ASKEY extender
- Admin password

All tokens are cached securely and refreshed automatically.

---

## 📊 Dashboards

Prebuilt panels available in `/dashboards/`:
- `askey_overview.yaml`
- `lte_performance.yaml`
- `gps_diagnostics.yaml`
- `alarms_and_reboots.yaml`
- `usage_trends.yaml`
- `system_status.yaml`

Import via UI or include in `lovelace.yaml`.

---

## 🔁 Automations & Helpers

Add input number entities for each hour (00–23) and import:
- `/helpers/input_numbers.yaml`
- `/automations/update_hourly_capacity.yaml`

This tracks hourly usage and feeds long-term statistics.

---

## 🔔 Events Fired

- `askey_alarm_event`
- `askey_reboot_event`

Use these in automations, logbook, or persistent notifications.

---

## 📚 Documentation

Full documentation available in the GitHub repo including setup, token flow, troubleshooting, and extensibility tips.

- [Full API Reference →](docs/api.md)

---

## Release Notes

- v1.0.0 - Initial Release

---

## 👤 Codeowners

Made by [@stevemurphymsu].

PRs welcome!
