DOMAIN = "askey-lte"
BASE_URL_TEMPLATE = "https://{ip}/webapi"
METADATA_PATHS = {
    "alarms": "data/alarm.json",
    "reboots": "data/reboot.json"
}
DEFAULT_SCAN_INTERVAL = 30  # seconds
EVENT_ALARM = "askey_alarm_event"
EVENT_REBOOT = "askey_reboot_event"
