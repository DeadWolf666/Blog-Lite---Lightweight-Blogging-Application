from flask import Flask
from flask_login import LoginManager
from application.views import views
from application.auth import auth
from application.controllers import controllers
from application.models import *
from configuration.database import *
from configuration.config import DevConfig

app = None

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(DevConfig)
    db.init_app(app)

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(controllers, url_prefix="/user")

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080)
