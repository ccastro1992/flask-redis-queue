# project/server/__init__.py


import os

from flask import Flask
from flask_bootstrap import Bootstrap4
from project.server.config import BaseConfig

def create_app(script_info=None):
    # instantiate the app
    app = Flask(
        __name__,
        template_folder="../client/templates",
        static_folder="../client/static",
    )

    # set config
    app_settings = dict(
        WTF_CSRF_ENABLED=BaseConfig.WTF_CSRF_ENABLED,
        REDIS_URL=BaseConfig.REDIS_URL,
        QUEUES=BaseConfig.QUEUES
    )
    app.config.update(app_settings)

    # set up extensions
    Bootstrap4(app)

    # register blueprints
    from project.server.main.views import main_blueprint

    app.register_blueprint(main_blueprint)

    # shell context for flask cli
    app.shell_context_processor({"app": app})

    return app
