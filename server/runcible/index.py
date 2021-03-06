import logging
from typing import Tuple
from molten import App, Route, ResponseRendererMiddleware, Settings
from molten.http import HTTP_404, Request
from molten.openapi import Metadata, OpenAPIHandler, OpenAPIUIHandler
from molten.settings import SettingsComponent
from molten.contrib.sqlalchemy import (
    SQLAlchemyMiddleware,
    SQLAlchemyEngineComponent,
    SQLAlchemySessionComponent,
)

from .api.welcome import welcome
from .api.todo import TodoManagerComponent, todo_routes
from .api.user import UserManagerComponent, user_routes
from .common import ExtJSONRenderer
from .schema import APIResponse
from .settings import SETTINGS

get_schema = OpenAPIHandler(
    metadata=Metadata(
        title="runcible",
        description="A development  API to be used in vuejs courses and tutorials.",
        version="0.0.0",
    )
)

get_docs = OpenAPIUIHandler()

components = [
    SettingsComponent(SETTINGS),
    SQLAlchemyEngineComponent(),
    SQLAlchemySessionComponent(),
    TodoManagerComponent(),
    UserManagerComponent(),
]

middleware = [ResponseRendererMiddleware(), SQLAlchemyMiddleware()]

renderers = [ExtJSONRenderer()]

routes = (
    [
        Route("/", welcome, "GET"),
        Route("/_schema", get_schema, "GET"),
        Route("/_docs", get_docs, "GET"),
        Route("/ping", lambda: {"message": "pong"}, "GET", name="ping"),
    ]
    + [todo_routes]  # noqa: W503
    + [user_routes]  # noqa: W503
)


class ExtApp(App):
    def handle_404(self, request: Request) -> Tuple[str, APIResponse]:
        """
        Returns as standardized JSONResponse on HTTP 404 Error.
        """
        return (
            HTTP_404,
            APIResponse(
                status=404,
                message=f"The resource you are looking for {request.scheme}://{request.host}{request.path} doesn't exist",
            ),
        )

    @property
    def settings(self):
        def _get_settings(_settings: Settings):
            return _settings

        settings = self.injector.get_resolver().resolve(_get_settings)()
        return settings


def create_app(_components=None, _middleware=None, _routes=None, _renderers=None):
    """
    Factory function for the creation of a `molten.App` instance
    """
    app = ExtApp(
        components=_components or components,
        middleware=_middleware or middleware,
        routes=_routes or routes,
        renderers=_renderers or renderers,
    )

    return app
