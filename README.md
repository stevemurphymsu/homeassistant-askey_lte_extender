# ASKEY LTE Network Extender – Home Assistant Integration

Track and visualize LTE diagnostics, alarms, GPS data, bandwidth trends, and system health from your ASKEY femtocell—all inside Home Assistant.

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

## ⚙️ Installation

### Option 1: Manual
1. Copy `custom_components/askey_lte` into `config/custom_components/`
2. Restart Home Assistant
3. Go to **Settings > Devices & Services > Add Integration**
4. Search for `ASKEY LTE`

### Option 2: HACS
1. Open HACS > Integrations > Custom Repositories
2. Add this repo and select `Integration`
3. Install & restart
4. Configure from UI

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

## 👤 Codeowners

Made by [@stevemurphymsu] – femtocell obsessive, diagnostics-obsessed, and loving LTE visibility.

PRs welcome!
