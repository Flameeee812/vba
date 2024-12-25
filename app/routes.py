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
    return delete_user_passport()


@vba.route("/update_readings", methods=["POST", "GET"])
def update_readings():
    return update_user_readings()


@vba.route("/get_readings", methods=["POST", "GET"])
def get_readings():
    return get_user_readings()


@vba.route("/update_debt", methods=["POST", "GET"])
def update_debt():
    return update_user_debt()


@vba.route("/get_debt", methods=["POST", "GET"])
def get_debt():
    return get_user_debt()
