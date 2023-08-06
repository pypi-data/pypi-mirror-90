# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['samtecdeviceshare']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.3,<4.0.0',
 'fastapi>=0.63.0,<0.64.0',
 'lockfile>=0.12.2,<0.13.0',
 'pydantic>=1.7.3,<2.0.0',
 'pyhumps>=1.6.1,<2.0.0',
 'uvicorn>=0.13.3,<0.14.0']

extras_require = \
{':sys_platform == "linux"': ['python-networkmanager', 'dbus-python']}

setup_kwargs = {
    'name': 'samtecdeviceshare',
    'version': '2.5.0',
    'description': 'Handles a variety of common routines for SDC-based applications',
    'long_description': '# Samtec Device Share\n\nA Python 3 SDC conforming REST API to run on IoT devices that enables user discovery, viewing, and management.\n\n## Installation\n\n```bash\npip install samtecdeviceshare\n```\n\n## Running\n\nFirst ensure all environment variables are set correctly.\nNote: To test locally for development ensure EMULATION and PYTHON_ENV are set.\n\n```bash\npython -m samtecdeviceshare.server\n```\n\n## Environment Variables\n\n### Application / SDC / SDS\n\n| Name              | Description                   | Default                                     |\n| ----------------- | ----------------------------- | ------------------------------------------- |\n| REST_ADDRESS      | Rest API Address              | 0.0.0.0                                     |\n| REST_PORT         | Rest port                     | 47546                                       |\n| APP_VERSION       | SemVer of app                 | 0.0.0                                       |\n| APP_LOG_PATH      | Path to store log files       | default tempdir()                           |\n| APP_WEB_PORT      | Embedded web app port         | 80                                          |\n| APP_IMG_PATH      | app icon path                 | {CURDIR}../static/img.png                   |\n| SDC_WIFI_TYPE     | enum: HOTSPOT CLIENT DISABLED | HOTSPOT                                     |\n| SDC_WIFI_SSID     | WiFi SSID                     | SDC-${**BALENA_PREFIX**_DEVICE_UUID}        |\n| SDC_WIFI_PASS     | WiFi passphrase               | samtec1!                                    |\n| SDC_WIFI_IFACE    | WiFi hardware interface       | wlan0                                       |\n| ETH_DISABLE       | Disable ethernet              | null                                        |\n| ETH_TARGET_NAME   | Eth hardware interface        | null                                        |\n| ETH_DHCP_TIMEOUT  | Timeout to get DHCP address   | 15                                          |\n| ETH_LOCAL_TIMEOUT | Timeout to get autoip address | 30                                          |\n| PYTHON_ENV        | enum: development production  | production                                  |\n| EMULATION         | Use emulated devices/io       | null                                        |\n| LOG_VERBOSE       | boolean verbose logs          | false                                       |\n| SDS_ROOT_PATH     | API root path                 | \'\'                                          |\n\n### Balena\n\nRefer to Balena [documentation](https://www.balena.io/docs/learn/develop/runtime/) for list and description of variables.\n\n- BALENA_SUPERVISOR_API_KEY\n- BALENA_APP_ID\n- BALENA_DEVICE_TYPE\n- BALENA\n- BALENA_SUPERVISOR_ADDRESS\n- BALENA_SUPERVISOR_HOST\n- BALENA_DEVICE_UUID\n- BALENA_API_KEY\n- BALENA_APP_RELEASE\n- BALENA_SUPERVISOR_VERSION\n- BALENA_APP_NAME\n- BALENA_DEVICE_NAME_AT_INIT\n- BALENA_HOST_OS_VERSION\n- BALENA_SUPERVISOR_PORT\n\n## Development\n\n### Installing\n\n```bash\ngit clone git@bitbucket.org:samteccmd/samtecdeviceshare.git samtecdeviceshare\ncd samtecdeviceshare\npoetry install --dev\npoetry shell\n```\n\n### Testing\n\nFirst, run dummy Balena supervisor:\n\n```bash\nbash ./tests/dummy-supervisor.sh\n```\n\nNext, fire up REST server using uvicorn:\n\n```bash\nEMULATION=1 PYTHON_ENV="development" uvicorn samtecdeviceshare.server:app --reload\n```\n\n**Interactive API docs** will be available: <http://127.0.0.1:8000/docs>\n\n### Unit Tests\n\n```bash\npylint --rcfile .pylintrc samtecdeviceshare\npytest\n```\n',
    'author': 'Adam Page',
    'author_email': 'adam.page@samtec.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
