# 📡 ASKEY LTE Integration – Complete API Reference

Custom Home Assistant integration for ASKEY LTE femtocells. This guide documents reverse-engineered API calls, authentication headers, payloads, and full JSON responses.

---

## 📑 Table of Contents

- [Authentication](#-authentication)
- [Core API Endpoints](#-core-api-endpoints-and-raw-responses)
  - [/webapi/simStatus](#webapisimstatus)
  - [/webapi/femtoStatus](#webapifemtostatus)
  - [/webapi/otarlist](#webapiotarlist)
  - [/webapi/refIcons](#webapireficons)
  - [/webapi/advanced](#webapiadvanced)
  - [/webapi/devices](#webapidevices)
  - [/webapi/aboutStatus](#webapiaboutstatus)
  - [/webapi/alarmLog](#webapialarmlog)
  - [/data/alarm.json](#dataalarmjson)
  - [/webapi/rebootLog](#webapirebootlog)
  - [/data/reboot.json](#datarebootjson)
  - [/webapi/serverStatus](#webapiserverstatus)
  - [/webapi/gps](#webapigps)
  - [/webapi/performance](#webapiperformance)
- [Required Headers](#-required-headers)
- [Token Handling](#-token-handling)
- [Notes for Developers](#-notes-for-developers)

---
## 🔐 Authentication
### POST `/webapi/login`

**Payload:**

```
expires=(unix timestamp+30 minutes)&password=(sha256)
```

**Response:**

```json
{
    "message": "",
    "result": 1,
    "authtoken": "YOxBe1QYRaudwxMUmFCE-9z-oPWBSkWLqKucuZUkmiwfn1muKU5CeKFfX6a8_Za5",
    "expires": "1755791190659"
}
```

---

## 🛠 Core API Endpoints and Raw Responses

### <a id="webapisimstatus"></a>`/webapi/simStatus`

```json
{
    "bhIpv6Addr": "REDACTED",
    "longi": "-73",
    "mdn": "Will display the data after login",
    "cellType": 1,
    "paTemp": "-",
    "ipMode": "2",
    "activeUECountTot": 1,
    "lati": "42",
    "gpsStatus": "Location Acquired",
    "operationMode": "Open",
    "bhStaticIpv6PrefixLen": "64",
    "FourGsignal": 1,
    "message": "",
    "hnbName": "Will display the data after login",
    "SWver": "GA5.16<br>V0.5.016.1764",
    "activeUECount": 1,
    "ipsecIp": "-",
    "bhIpv4Addr": "REDACTED",
    "serial": "REDACTED",
    "result": 1,
    "gpsSignal": 1,
    "macAddress": "REDACTED",
    "uptime": "00:28:21",
    "csgID": "Will display the data after login"
}
```

### <a id="webapifemtostatus"></a>`/webapi/femtoStatus`

```json
{
    "result": 1,
    "otarEnable": 0
}
```

### <a id="webapiotarlist"></a>`/webapi/otarlist`

```json
{
    "message": "",
    "otarList": [],
    "currentTime": "07-22-2025 16:07:48 UTC"
}
```

### <a id="webapireficons"></a>`/webapi/refIcons`

```json
{
    "activeUECount": 0,
    "message": "",
    "result": 1,
    "FourGsignal": 1,
    "operationMode": "Open",
    "cellType": 1,
    "activeUECountTot": 0,
    "gpsSignal": 1
}
```

### <a id="webapiadvanced"></a>`/webapi/advanced`

```json
{
    "earfcn": 5230,
    "csgID": "",
    "percentMin": 10,
    "cellType": 1,
    "txDbmMax": 20,
    "message": "",
    "operationMode": "Open",
    "automaticTxPwrMode": 1,
    "turnOffRf": 0,
    "recommendTxPower": 100,
    "hnbName": "",
    "rfPowerMode": 1,
    "netInfoHex": ["REDACTED"],
    "bandwidth": 50,
    "txDbmMin": 10,
    "result": 1,
    "FourGsignal": 1,
    "txPower": 100,
    "netInfo": ["REDACTED"],
    "currentTime": "07-22-2025 16:09:45 UTC",
    "pci": 483,
    "endcX2": 0
}
```

### <a id="webapidevices"></a>`/webapi/devices`

> (Partial output for brevity)

```json
{
    "operationModeLast24Hours": "1",
    "peakConnectedUsersLast24Hours": 3,
    "peakCapacityUsedLast24HoursTot": "21.43",
    "emerAcUECountTot": 0,
    "activeUECountTot": 0,
    "peakCapacityUsedLast24Hours": "21.43",
    "HourlyCapacityUsed": [
        {
            "time": "20250722T070000 UTC",
            "operationMode": "open",
            "total": "7.14",
            "member": "0.00",
            "nonMember": "7.14"
        },
        {
            "time": "20250722T080000 UTC",
            "operationMode": "open",
            "total": "14.29",
            "member": "0.00",
            "nonMember": "14.29"
        }
        // ...
    ],
    "peakConnectedUsersLast24HoursEventTime": "07-22-2025 16:00:00 UTC",
    "message": "",
    "currentTime": "07-22-2025 16:10:40 UTC",
    "peakConnectedUsersLastHourMem": 0,
    "activeUECount": 0,
    "peakCapacityUsedLastHourMem": "0.00",
    "peakCapacityUsedLastHourTot": "14.29",
    "operationModeLastHour": "1",
    "peakCapacityUsedLastHour": "14.29",
    "emerAcUECount": 0,
    "peakCapacityUsedLast24HoursMem": "0.00",
    "result": 1,
    "activeUECountMem": 0,
    "peakConnectedUsersLastHourTot": 2,
    "peakConnectedUsersLastHour": 2,
    "peakConnectedUsersLast24HoursMem": 0,
    "peakConnectedUsersLast24HoursTot": 3,
    "emerAcUECountMem": 0
}
```

### <a id="webapiaboutstatus"></a>`/webapi/aboutStatus`

```json
{
    "gpsAmount": 9,
    "message": "",
    "result": 1,
    "alarmList": [],
    "activeUECount": 0,
    "gpsAmountTot": 11,
    "startUpList": [
        {
            "no": 1,
            "datetime": "04-02-2025 01:53:11 UTC",
            "result": "complete",
            "pageNo": 1,
            "status": "Starting up ..."
        },
        {
            "no": 2,
            "datetime": "04-02-2025 01:53:18 UTC",
            "result": "complete",
            "pageNo": 3,
            "status": "HW initializing ..."
        },
        {
            "no": 3,
            "datetime": "04-02-2025 01:53:20 UTC",
            "result": "complete",
            "pageNo": 6,
            "status": "SW initializing ..."
        },
        {
            "no": 4,
            "datetime": "04-02-2025 01:53:31 UTC",
            "result": "complete",
            "pageNo": 9,
            "status": "Acquiring local IP address ...<br>&emsp;IP: REDACTED<br>&emsp;DNS1: REDACTED"
        },
        {
            "no": 5,
            "datetime": "07-22-2025 15:33:39 UTC",
            "result": "complete",
            "pageNo": 14,7
            "status": "Searching for GPS signal ...<br>&emsp;Latitude: 42<br>&emsp;Longitude: -73"
        },
        {
            "no": 6,
            "datetime": "07-22-2025 15:34:16 UTC",
            "result": "complete",
            "pageNo": 18,
            "status": "SeGW discovery and IPsec Setup ...<br>&emsp;SeGW FQDN: REDACTED<br>&emsp;SeGW IP: REDACTED<br>&emsp;Left Id: REDACTED"
        },
        {
            "no": 7,
            "datetime": "07-22-2025 15:35:20 UTC",
            "result": "complete",
            "pageNo": 20,
            "status": "Connecting to HeMS ...<br>&emsp;HeMS Url: REDACTED br>&emsp;HeNB SN: REDACTED"
        },
        {
            "no": 8,
            "datetime": "07-22-2025 15:36:57 UTC",
            "result": "complete",
            "pageNo": 26,
            "status": "Connecting to the core network ..."
        },
        {
            "no": 9,
            "datetime": "07-22-2025 15:37:03 UTC",
            "result": "complete",
            "pageNo": 30,
            "status": "Service Active"
        }
    ],
    "activeUECountTot": 14,
    "lcdDisplay": {
        "datetime": "2025-07-22 15:37:03",
        "pageEvent": "SYS_INIT_FINISH",
        "pageIndex": 13,
        "pageType": 0
    },
    "currentTime": "07-22-2025 16:11:54 UTC"
}
```

### <a id="webapialarmlog"></a>`/webapi/alarmLog`

> This response includes 60+ historical alarm entries. Example structure:

```json
{
    "alarmHistoryList": [
        {
            "alarmTime": "07-22-2025 03:08:24 UTC",
            "alarmState": "Cleared",
            "alarmDesc": "SCTP HB failed over criteria",
            "alarmId": "11112",
            "alarmName": "SCTP link failure"
        },
        {
            "alarmTime": "07-22-2025 03:04:04 UTC",
            "alarmState": "Cleared",
            "alarmDesc": "Unsuccessful IP Sec tunnel",
            "alarmId": "12017",
            "alarmName": "IPSec down"
        }
    ]
}
```

### <a id="dataalarmjson"></a>`/data/alarm.json`

> Includes mappings for all 30+ alarm IDs. Example:

```json
{
    "11112": {
        "alarmName": "SCTP link failure",
        "alarmDesc": "SCTP HB failed over criteria",
        "troubleshooting": "Check firewall or LAN settings. If unresolved, contact support."
    },
    "12017": {
        "alarmName": "IPSec down",
        "alarmDesc": "Tunnel setup failed with SeGW",
        "troubleshooting": "Verify network connectivity, firewall rules, and ISP availability."
    }
}
```

### <a id="webapirebootlog"></a>`/webapi/rebootLog`

```json
{
    "rebootHistoryList": [
        {
            "rebootTime": "07-22-2025 15:32:33 UTC",
            "rebootReason": "4"
        },
        {
            "rebootTime": "07-21-2025 21:57:21 UTC",
            "rebootReason": "1"
        }
    ]
}
```

### <a id="datarebootjson"></a>`/data/reboot.json`

```json
{
    "0": { "rebootReason": "Reboot via command line" },
    "1": { "rebootReason": "Out of power" },
    "4": { "rebootReason": "Complete restart via Web-GUI" },
    "11": { "rebootReason": "Cell fails to establish IPSec tunnel after 8 hours" }
}
```

### <a id="webapiserverstatus"></a>`/webapi/serverStatus`

```json
{
    "IKEV2_STATUS": 1,
    "IKEV2_TRY_TIME": "07-22-2025 16:16:48 UTC",
    "AGPS_TRY_TIME": "07-22-2025 16:16:48 UTC",
    "DNS_TRY_TIME": "07-22-2025 16:16:48 UTC",
    "IKEV2_PORT": "4500",
    "IPSEC_TUNNEL_STATUS": 1,
    "DNS_STATUS": 1,
    "AGPS_IP": "REDACTED",
    "AGPS_STATUS": 1,
    "message": "",
    "result": 1,
    "DNS_IP": "REDACTED",
    "IKEV2_IP": "REDACTED",
    "DNS_PORT": "53",
    "AGPS_PORT": "443",
    "currentTime": "07-22-2025 16:16:48 UTC"
}
```

### <a id="webapigps"></a>`/webapi/gps`

```json
{
    "GpsList": [
        { "SatelliteQual": "35.7", "SatelliteId": 29 },
        { "SatelliteQual": "35.6", "SatelliteId": 5 }
        // ...
    ],
    "HourlySatelliteSignals": [
        { "Min": "6", "Avg": "8.8", "Max": "11", "date": "2025-07-22 16:00:00 UTC" }
    ],
    "HourlySatelliteQualities": [
        { "Min": "9.5", "Avg": "25.1", "Max": "40.7", "date": "2025-07-22 16:00:00 UTC" }
    ],
    "gpsAmountTot": 11,
    "gpsAmount": 8,
    "gpsSignal": 1,
    "gpsStatus": "Location Acquired",
    "longi": "-73",
    "lati": "42",
    "result": 1,
    "message": "",
    "currentTime": "07-22-2025 16:20:44 UTC"
}
```

---

## 📝 Required Headers

All API requests require the following headers:

- `Content-Type: application/x-www-form-urlencoded`
- `X-Requested-With: XMLHttpRequest`
- `Authtoken: <token from /webapi/login>`

---

## 🔄 Token Handling

- The `Authtoken` returned from `/webapi/login` must be included in all subsequent requests.
- Tokens expire at the timestamp provided in the `expires` field.

---

## 💡 Notes for Developers

- This API is reverse-engineered and may change with firmware updates.
- Some endpoints may require specific permissions or device states.
- For large arrays (e.g., alarm logs), only partial data is shown for brevity.
- Use the anchor links in the Table of Contents for quick navigation.

