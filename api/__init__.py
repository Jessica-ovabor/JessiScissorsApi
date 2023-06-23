from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from .auth.views import auth_namespace
from .url_package.views import url_namespace
from .demo.views import demo_namespace
from .model.users import User
from .model.url import Url
from .utils import db
from .config.config import config_dict
from werkzeug.exceptions import NotFound,MethodNotAllowed



def create_app(config=config_dict['dev']):
    app = Flask(__name__)
    #configure the dev so we can use it
    app.config.from_object(config)
    db.init_app(app)
    jwt = JWTManager(app)
    authorizations = {
        'apikey': {
            'type': 'apiKey',
            'in': 'header',
            'name': "Authorization",
            "description": "Add a JWT token to the header with ** Bearer &lt;JWT&gt; ** token to authorize"
        }
    }

    api = Api(
        app, 
        version='1.0', 
        title='Scissors API', 
        description='A simple URL shortener REST API service',
        authorizations=authorizations,
        security='apikey'
    )
    api.add_namespace(auth_namespace, path='/auth')
    api.add_namespace(url_namespace, path='/url')
    api.add_namespace(demo_namespace, path='/demo')

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': User,
            'Url' :Url,
           
        }
    return app