import flask as fl
from . import scheduler
from .routes import vba


my_app = fl.Flask(__name__, template_folder="../templates")
my_app.register_blueprint(vba, url_prefix="/vba")
