import json
import os

import tornado.web

from tornado_swagger._builders import generate_doc_from_endpoints
from tornado_swagger._handlers import SwaggerHomeHandler

STATIC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "swagger_ui"))


def export_swagger(
    routes,
    api_base_url="/",
    description="Swagger API definition",
    api_version="1.0.0",
    title="Swagger API",
    contact="",
    schemes=None,
    security_definitions=None,
):
    return generate_doc_from_endpoints(
        routes,
        api_base_url=api_base_url,
        description=description,
        api_version=api_version,
        title=title,
        contact=contact,
        schemes=schemes,
        security_definitions=security_definitions,
    )


def setup_swagger(
    routes,
    swagger_url="/api/doc",
    api_base_url="/",
    description="Swagger API definition",
    api_version="1.0.0",
    title="Swagger API",
    contact="",
    schemes=None,
    security_definitions=None,
):
    swagger_schema = generate_doc_from_endpoints(
        routes,
        api_base_url=api_base_url,
        description=description,
        api_version=api_version,
        title=title,
        contact=contact,
        schemes=schemes,
        security_definitions=security_definitions,
    )

    _swagger_url = "/{}".format(swagger_url) if not swagger_url.startswith("/") else swagger_url
    _base_swagger_url = _swagger_url.rstrip("/")

    routes += [
        tornado.web.url(_swagger_url, SwaggerHomeHandler),
        tornado.web.url("{}/".format(_base_swagger_url), SwaggerHomeHandler),
    ]

    with open(os.path.join(STATIC_PATH, "ui.jinja2"), "r") as f:
        SwaggerHomeHandler.SWAGGER_HOME_TEMPLATE = f.read().replace("{{ SWAGGER_SCHEMA }}", json.dumps(swagger_schema))