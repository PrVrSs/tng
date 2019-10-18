from .cor import create_cors_middleware
from .status import (
    create_error_middleware,
)


def setup_middlewares(app):
    error_middleware = create_error_middleware({
    })

    cors_middleware = create_cors_middleware()

    app.middlewares.append(error_middleware)
    app.middlewares.append(cors_middleware)
