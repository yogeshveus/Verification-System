from flask import Flask
from config import SECRET_KEY, DATABASE
from database.db import init_db
from routes.auth_routes import auth
from routes.manufacturer_routes import manufacturer
from routes.consumer_routes import consumer


def create_app(test_config=None):
    app = Flask(__name__)
    app.secret_key = SECRET_KEY
    app.config['DATABASE'] = DATABASE

    if test_config:
        app.config.update(test_config)

    app.register_blueprint(auth)
    app.register_blueprint(manufacturer)
    app.register_blueprint(consumer)

    init_db(app.config['DATABASE'])
    return app

app = create_app()

#if __name__ == "__main__":
    #app.run(debug=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)




