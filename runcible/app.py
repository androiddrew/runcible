from .index import create_app
from .common import init_CORS

app = create_app(initializers=[init_CORS])