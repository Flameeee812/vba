from .handlers import *


vba = fl.Blueprint('vba', __name__)


@vba.route("/", methods=["GET"])
def home():
    return home_handler()


@vba.route("/reg_user", methods=["POST", "GET"])
def reg_user():
    return registration()


@vba.route("/delete_user", methods=["POST", "GET"])
def delete_user():
    return delete_user_initials()


@vba.route("/update_readings", methods=["POST", "GET"])
def update_readings():
    return update_user_readings()

