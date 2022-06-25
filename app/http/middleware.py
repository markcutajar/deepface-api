from app.extensions import auth


def register_token_validation(app):
    @app.before_request
    @auth.login_required
    def before_request():
        pass


@auth.verify_token
def verify_token(token):

    return True

