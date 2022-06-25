import os

from flask import Flask

from app.extensions import api
from app.http.resources.verify import Verify
from app.http.exceptions.base import register_exception_handling
from app.services.base import register_logging


def create_app():
    """Application factory. This is used to run the app from the root.
    """
    app = Flask(__name__.split('.')[0])
    app.config.from_object(os.environ['APP_SETTINGS'])
    register_endpoints()
    register_auth(app)
    register_extensions(app)
    register_services(app)
    register_scripts(app)
    return app


def register_extensions(app):
    api.init_app(app)


def register_scripts(app):
    """Function to add cli commands to the app.
    Example: app.cli.add_command(custom_command_cli)
    """
    pass


def register_services(app):
    """Function to add cli commands to the app.
    Example: app.warehouse = Warehouse(app)
    """
    register_logging(app)
    register_exception_handling(app)


def register_endpoints():
    api.add_resource(Verify, '/actions/verify')


def register_auth(app):
    pass
