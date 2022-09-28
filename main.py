from pathlib import Path

from werkzeug.security import generate_password_hash
from flask import Flask
from flask_login import LoginManager, current_user

from view.auth import auth
from view.main import main
from view.api.flights import flights_api

from model.models import User
from app_db import db


CURRENT_DIR = Path(__file__).parent


def create_app():
    app = Flask(__name__,
                static_url_path='/static',
                static_folder=str(CURRENT_DIR / 'static'),
                template_folder=str(CURRENT_DIR / 'templates'))

    # Register BLUEPRINTS
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(flights_api, url_prefix='/api/flight')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.find_one(User, 'id', user_id)

    @app.context_processor
    def inject_user():
        if current_user.is_authenticated:
            return dict(login=current_user.username, is_admin=current_user.is_admin)
        else:
            return dict()

    return app


if __name__ == "__main__":
    admin = db.find_one(User, 'id', '0')
    if admin is None:
        admin = User(
            id='0',
            username='admin',
            password=generate_password_hash('admin', method='sha256'),
            is_admin=True
        )
        db.add(admin)


    app = create_app()
    # Testing secret key
    app.config['SECRET_KEY'] = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
    app.run(debug=True)
