import sys
from .index import create_app
from molten import App
from wsgicors import CORS
from werkzeug.contrib.profiler import ProfilerMiddleware, MergeStream

from .error import ConfigurationError

CORS_SETTINGS = ["CORS_HEADERS", "CORS_METHODS", "CORS_ORIGIN", "CORS_MAXAGE"]


def wrap_CORS(app: App) -> CORS:
    """Initializes CORS wsgi middleware from app settings.

    """

    _cors_settings = {k: v for k, v in app.settings.items() if k.startswith("CORS")}

    for setting in CORS_SETTINGS:
        if setting not in _cors_settings or _cors_settings.get(setting) is None:
            raise ConfigurationError(f"CORS setting {setting} not configured")

    extended_app = CORS(
        app,
        headers=_cors_settings.get("CORS_HEADERS"),
        methods=_cors_settings.get("CORS_METHODS"),
        origin=_cors_settings.get("CORS_ORIGIN"),
        maxage=_cors_settings.get("CORS_MAXAGE"),
    )

    return extended_app


app = wrap_CORS(create_app())

# Uncomment to profile your code using the Werkzueg middleware.
# f = open('/Users/Drewbednar/PycharmProjects/runcible/runcible/profiler.log', 'w')
# stream = MergeStream(sys.stdout, f)
# app = ProfilerMiddleware(app, stream)
