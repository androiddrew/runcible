import datetime as dt
from os import path
from decimal import Decimal
from typing import Any
from molten import App, JSONRenderer, is_schema, dump_schema
from wsgicors import CORS

from .error import ConfigurationError

BASE_PATH = path.normpath(path.join(path.abspath(path.dirname(__file__)), "."))

CORS_SETTINGS = ["CORS_HEADERS", "CORS_METHODS", "CORS_ORIGIN", "CORS_MAXAGE"]


def path_to(*xs):
    """
    Construct a path from the root project directory
    """
    return path.join(BASE_PATH, *xs)


class ExtJSONRenderer(JSONRenderer):
    """JSON Render with support for ISO 8601 datetime format strings and Decimal"""

    def default(self, ob: Any) -> Any:
        """You may override this when subclassing the JSON renderer in
        order to encode non-standard object types.
        """
        if is_schema(type(ob)):
            return dump_schema(ob)
        if isinstance(ob, dt.datetime):
            return ob.isoformat()
        if isinstance(ob, Decimal):
            return float(ob)

        raise TypeError(f"cannot encode values of type {type(ob)}")  # pragma: no cover


def init_CORS(app: App) -> CORS:
    """Initializes CORS wsgi middleware from app settings.

    To be used within an application factory function.
    """

    _cors_settings = {k: v for k, v in app.settings.items() if k.startswith("CORS")}

    for setting in CORS_SETTINGS:
        if setting not in _cors_settings or _cors_settings.get(setting) is None:
            raise ConfigurationError(f"CORS setting {setting} not configured")

    extended_app = CORS(app,
                        headers=_cors_settings.get("CORS_HEADERS"),
                        methods=_cors_settings.get("CORS_METHODS"),
                        origin=_cors_settings.get("CORS_ORIGIN"),
                        maxage=_cors_settings.get("CORS_MAXAGE")
                        )

    return extended_app
