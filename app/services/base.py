import logging


def register_logging(app):
    if app.config["DEBUG"]:
        app.logger.setLevel(logging.DEBUG)
    else:
        app.logger.setLevel(logging.INFO)
    logging.basicConfig(level=logging.INFO)