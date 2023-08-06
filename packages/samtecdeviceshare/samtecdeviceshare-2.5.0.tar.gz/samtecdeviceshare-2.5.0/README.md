# Samtec Device Share

A Python 3 SDC conforming REST API to run on IoT devices that enables user discovery, viewing, and management.

## Installation

```bash
pip install samtecdeviceshare
```

## Running

First ensure all environment variables are set correctly.
Note: To test locally for development ensure EMULATION and PYTHON_ENV are set.

```bash
python -m samtecdeviceshare.server
```

## Environment Variables

### Application / SDC / SDS

| Name              | Description                   | Default                                     |
| ----------------- | ----------------------------- | ------------------------------------------- |
| REST_ADDRESS      | Rest API Address              | 0.0.0.0                                     |
| REST_PORT         | Rest port                     | 47546                                       |
| APP_VERSION       | SemVer of app                 | 0.0.0                                       |
| APP_LOG_PATH      | Path to store log files       | default tempdir()                           |
| APP_WEB_PORT      | Embedded web app port         | 80                                          |
| APP_IMG_PATH      | app icon path                 | {CURDIR}../static/img.png                   |
| SDC_WIFI_TYPE     | enum: HOTSPOT CLIENT DISABLED | HOTSPOT                                     |
| SDC_WIFI_SSID     | WiFi SSID                     | SDC-${**BALENA_PREFIX**_DEVICE_UUID}        |
| SDC_WIFI_PASS     | WiFi passphrase               | samtec1!                                    |
| SDC_WIFI_IFACE    | WiFi hardware interface       | wlan0                                       |
| ETH_DISABLE       | Disable ethernet              | null                                        |
| ETH_TARGET_NAME   | Eth hardware interface        | null                                        |
| ETH_DHCP_TIMEOUT  | Timeout to get DHCP address   | 15                                          |
| ETH_LOCAL_TIMEOUT | Timeout to get autoip address | 30                                          |
| PYTHON_ENV        | enum: development production  | production                                  |
| EMULATION         | Use emulated devices/io       | null                                        |
| LOG_VERBOSE       | boolean verbose logs          | false                                       |
| SDS_ROOT_PATH     | API root path                 | ''                                          |

### Balena

Refer to Balena [documentation](https://www.balena.io/docs/learn/develop/runtime/) for list and description of variables.

- BALENA_SUPERVISOR_API_KEY
- BALENA_APP_ID
- BALENA_DEVICE_TYPE
- BALENA
- BALENA_SUPERVISOR_ADDRESS
- BALENA_SUPERVISOR_HOST
- BALENA_DEVICE_UUID
- BALENA_API_KEY
- BALENA_APP_RELEASE
- BALENA_SUPERVISOR_VERSION
- BALENA_APP_NAME
- BALENA_DEVICE_NAME_AT_INIT
- BALENA_HOST_OS_VERSION
- BALENA_SUPERVISOR_PORT

## Development

### Installing

```bash
git clone git@bitbucket.org:samteccmd/samtecdeviceshare.git samtecdeviceshare
cd samtecdeviceshare
poetry install --dev
poetry shell
```

### Testing

First, run dummy Balena supervisor:

```bash
bash ./tests/dummy-supervisor.sh
```

Next, fire up REST server using uvicorn:

```bash
EMULATION=1 PYTHON_ENV="development" uvicorn samtecdeviceshare.server:app --reload
```

**Interactive API docs** will be available: <http://127.0.0.1:8000/docs>

### Unit Tests

```bash
pylint --rcfile .pylintrc samtecdeviceshare
pytest
```
