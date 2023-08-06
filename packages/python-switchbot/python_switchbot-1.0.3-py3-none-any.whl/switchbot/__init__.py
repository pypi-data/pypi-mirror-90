"""Main classes."""
from cachetools import TTLCache
from cachetools.keys import hashkey
from distutils.util import strtobool
from functools import cached_property, partial
from json import dumps
from pycognito import Cognito
from requests import Session
from requests.auth import AuthBase
from threading import Lock

from .utils import sanitize_id, url_for


SwitchBotCognito = partial(
    Cognito, user_pool_id="us-east-1_x1fixo5LC", client_id="19n6vlutv8316utiqq66urakk3"
)


class SwitchBotAuth(AuthBase):
    """Class to handle Cognito authentication."""

    def __init__(self, switchbot):
        """Create authentication object."""
        self.switchbot = switchbot

    def __call__(self, request):
        """Add authenticalion header."""
        if "l9ren7efdj" in request.url:
            expired = self.switchbot.cognito.check_token()
            token = self.switchbot.cognito.access_token
        elif "vxhewp40e8" in request.url:
            token = self.switchbot.user_token
        else:
            raise ValueError(f"Invalid url: {request.url}")

        request.headers["Authorization"] = token

        return request


class Device:
    """Generic device base class."""

    def __init__(self, switchbot, id):
        """Create device object."""
        self.switchbot = switchbot
        self.id = sanitize_id(id)
        self.type = None
        self.children = []
        self._type = None
        self._state = None
        self._battery = None

        self.update()

    def update(self):
        """Update object state."""
        self._refresh(True)

        self.name = self._device["device_name"]

    def _refresh(self, force=False):
        self._device, device_updated = self._query_device(self.switchbot, self.id)

        self._status, status_updated = self.switchbot._api(
            "post", "refresh_device", {"items": [self.id]}
        )

        return device_updated or status_updated or force

    @classmethod
    def _query_device(cls, switchbot, id):
        data, updated = switchbot._api("get", "get_devices")

        for device in data["deviceList"]:
            if device["device_mac"] == id:
                return device, updated

        raise KeyError

    @staticmethod
    def factory(switchbot, id, group=True):
        """Return device object of correct type."""
        device, _ = Device._query_device(switchbot, sanitize_id(id))

        type = device["device_detail"]["device_type"]
        links = []

        if "deviceLinks" in device:
            links = device["deviceLinks"]

        assert type is not None

        if type == "WoLinkMini":
            return MiniHub(switchbot, id)
        elif type == "WoHand":
            return Bot(switchbot, id)
        elif type == "WoCurtain":
            if links and group:
                return CurtainGroup(switchbot, links[0])
            else:
                return Curtain(switchbot, id)
        else:
            return Device(switchbot, id)

    def debug(self):
        """Return debug data."""
        self._refresh()

        remove = [
            "ble_version",
            "cloudServiceAble",
            "commandTime",
            "hardware_version",
            "hubMac",
            "ip",
            "isEncrypted",
            "json_version",
            "lastConnectTime",
            "lastLinkToAppTime",
            "model",
            "lastDisConnectTime",
            "netConfigAble",
            "parent_device",
            "plateform",
            "platforms",
            "pubtopic",
            "remote",
            "scanTime",
            "scanTimeOld",
            "subtopic",
            "support_cmd",
            "update_time",
            "updateTime",
            "user_name",
            "userID",
            "userList",
            "version",
            "wifi_mac",
            "wifi_version",
        ]

        debug = {"device": self._device, "status": self._status}

        for key in remove:
            if key in debug["device"]:
                del debug["device"][key]
            if "device_detail" in debug["device"]:
                if key in debug["device"]["device_detail"]:
                    del debug["device"]["device_detail"][key]
            if key in debug["status"]:
                del debug["status"][key]

        return debug

    @property
    def battery(self):
        """Current battery level."""
        self._refresh()
        return self._battery

    @property
    def state(self):
        """Current state."""
        self._refresh()
        return self._state

    def _update_state(self, command, parameter="default"):
        assert self._type

        self.switchbot._api(
            "post",
            "turn_device",
            {
                "items": [
                    {
                        "deviceID": self.id,
                        "deviceType": self._type,
                        "cmdType": "command",
                        "parameter": parameter,
                        "deviceCmd": command,
                    }
                ]
            },
            force=True,
        )

        self.update()


class Bot(Device):
    """Bot device class."""

    def update(self):
        """Update object state."""
        super().update()

        self.type = "Bot"
        self._type = "WoHand"

        if self._status["deviceMode"] == "0":
            self.mode = "press"
        elif self._status["deviceMode"] == "1":
            self.mode = "toggle"
        else:
            raise NotImplementedError

    def _refresh(self, force=False):
        if not super()._refresh(force):
            return

        self._state = self._status["status"]["power"] == "on"

    @property
    def state(self):
        """Current bot state."""
        self._refresh()

        return self._state if self.mode == "toggle" else False

    @state.setter
    def state(self, value):
        """Set bot state."""
        if self.mode == "toggle":
            self._update_state("turnOn" if value else "turnOff")
        elif self.mode == "press" and value:
            self.press()

    def turn(self, value):
        """Set bot state."""
        self.state = strtobool(value)

    def press(self):
        """Press bot button."""
        assert self.mode == "press"

        self._update_state("press")

    def toggle(self):
        """Toggle bot state."""
        self.state = not self.state


class CurtainGroup(Device):
    """CurtainGroup class, containing other curtains as children."""

    def update(self):
        """Update object state."""
        super().update()

        self.type = "CurtainGroup"
        self.master = True
        self.grouped = True

        for child in self._device["deviceLinks"]:
            self.children.append(self.factory(self.switchbot, child, False))

    @property
    def state(self):
        """Current curtain state."""
        return self.children[0].state

    @state.setter
    def state(self, value):
        """Set curtain state."""
        self.children[0].state = value

    @property
    def position(self):
        """Current curtain position."""
        return self.children[0].position

    @position.setter
    def position(self, value):
        """Set curtain position."""
        self.children[0].position = value

    @property
    def moving(self):
        """ A curtain is currently moving."""
        for child in self.children:
            if child.moving:
                return True

        return False

    @property
    def direction(self):
        direction = self.children[0].direction

        for child in self.children:
            if child.direction != direction:
                return "Multiple"

        return direction

    @property
    def battery(self):
        """Current minimum battery level."""
        values = []

        for child in self.children:
            values.append(child.battery)

        return min(values)

    @property
    def calibrated(self):
        """All curtains are calibrated."""
        for child in self.children:
            if not child.calibrated:
                return False

        return True

    @property
    def fitting(self):
        """Type of fitting."""
        return self.children[0].fitting

    def open(self):
        """Open curtains."""
        self.children[0].open()

    def close(self):
        """Close curtains."""
        self.children[0].close()

    def move(self, value):
        """Move curtains."""
        self.children[0].move(value)

    def toggle(self):
        """Toggle curtains."""
        self.children[0].toggle()


class Curtain(Device):
    """Curtain device class."""

    def update(self):
        """Update object state."""
        super().update()

        self.type = "Curtain"
        self._type = "WoCurtain"
        self._mode = self._status["deviceMode"]
        self.calibrated = self._device["isCalibrate"]
        self.direction = self._device["openDirection"].title()
        self.master = self._device["isMaster"]
        self.grouped = self._device["isGroup"]
        self._moving = False

        if "device_mode" in self._device:
            self.fitting = self._device["device_mode"]
        else:
            self.fitting = "Unknown"

    def _refresh(self, force=False):
        if not super()._refresh(force):
            return

        self._moving = self._status["status"]["isMove"]

        if self._device["isMaster"]:
            self._position = self._status["status"]["position"]
        else:
            self._position = None

        if "battery" in self._status["status"]:
            self._battery = self._status["status"]["battery"]
        else:
            self._battery = None

    @property
    def position(self):
        """Current curtain position."""
        self._refresh()
        return self._position

    @position.setter
    def position(self, value):
        """Set curtain position."""
        assert self.master

        self._update_state("setPosition", ",".join(["0", self._mode, str(value)]))

    @property
    def state(self):
        """Current curtain state."""
        return True if self._position == 0 else False

    @state.setter
    def state(self, value):
        """Set curtain state."""
        assert self.master

        if value:
            self.close()
        else:
            self.open()

    @property
    def moving(self):
        """Curtain is currently moving."""
        self._refresh()
        return self._moving

    def open(self):
        """Open curtain."""
        assert self.master

        self.move(0)

    def close(self):
        """Close curtain."""
        assert self.master

        self.move(100)

    def move(self, value):
        """Move curtain."""
        assert self.master

        if value == "open":
            return self.open()
        elif value == "close":
            return self.close()
        elif value == "closed":
            return self.close()

        assert int(value) >= 0
        assert int(value) <= 100

        self.position = int(value)

    def toggle(self):
        """Toggle curtain."""
        self.state = not self.state


class MiniHub(Device):
    """Mini Hub device class."""

    def update(self):
        """Update object state."""
        super().update()

        self.type = "MiniHub"


class SwitchBot:
    """Main SwitchBot class."""

    def __init__(self, email_or_tokens=None, **kwargs):
        """Create SwitchBot object."""
        email, tokens = kwargs.get("email"), kwargs.get("tokens")
        if isinstance(email_or_tokens, str):
            email = email_or_tokens
        elif isinstance(email_or_tokens, dict):
            tokens = email_or_tokens

        email_passed, tokens_passed = email is not None, tokens is not None
        if email_passed and tokens_passed:
            raise ValueError("Either email or tokens should be passed")

        if email_passed:
            self.cognito = SwitchBotCognito(username=email)
        elif tokens_passed:
            self.cognito = SwitchBotCognito(**tokens)
        else:
            raise ValueError("Neither email nor tokens are passed")

        self._ttl = kwargs.get("ttl", 5 * 60)
        self.cache = TTLCache(100, self._ttl)
        self.lock = Lock()
        self.session = self._prepare_session()

    def _api(self, method, type, json=None, force=False):
        updated = False
        data = None

        key = hashkey(method, type, dumps(json))

        if not force:
            with self.lock:
                data = self.cache.get(key)

        if force or not data:
            if method == "get":
                response = self.session.get(url_for(type))
            elif method == "post":
                response = self.session.post(url_for(type), json=json)
            else:
                raise NotImplementedError

            data = response.data

            with self.lock:
                self.cache[key] = data

            updated = True

        return data, updated

    def authenticate(self, password):
        """Authenticate with SwitchBot."""
        self.cognito.authenticate(password)

    def device(self, id):
        """Return individual device by ID."""
        return Device.factory(self, id)

    @property
    def devices(self):
        """Return all devices."""
        devices = []

        for id in self.ids:
            devices.append(self.device(id))

        return devices

    @property
    def ids(self):
        """Return all device IDs."""
        data, _ = self._api("get", "query_user")

        return data["sortInfo"]["array"]

    @cached_property
    def user_token(self):
        """Return user token."""
        data, _ = self._api("get", "query_user")

        return data["openApiToken"]["token"]

    @property
    def authenticated(self):
        """Currently authenticated."""
        return bool(self.cognito.access_token)

    @property
    def cognito_tokens(self):
        """Return Cognito tokens."""
        return {
            "id_token": self.cognito.id_token,
            "refresh_token": self.cognito.refresh_token,
            "access_token": self.cognito.access_token,
        }

    @property
    def ttl(self):
        """Return cache TTL."""
        return self._ttl

    @ttl.setter
    def ttl(self, value):
        """Set cache TTL."""
        self._ttl = value
        self.cache.ttl = value

    def _prepare_session(self):
        def handle_response(response, *args, **kwargs):
            data = {key.lower(): value for key, value in response.json().items()}

            assert data["statuscode"] == 100

            data = data["body"]
            data = data["items"] if "items" in data else data

            response.data = (
                data[0] if isinstance(data, list) and (len(data) == 1) else data
            )

            return response

        session = Session()
        session.auth = SwitchBotAuth(self)
        session.headers.update({"Content-Type": "application/json"})
        session.hooks["response"].append(handle_response)
        return session
