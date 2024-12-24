import flask as fl
import database as db

connection = db.get_connection()


def home_handler():
    return fl.render_template("home.html")


def registration():

    if fl.request.method == "POST":
        initials = fl.request.form.get("initials")

        reg = db.add_initials(connection, initials)
        if reg:
            return fl.render_template("successful_reg.html")
        return fl.render_template("lose_reg.html")

    if fl.request.method == "GET":
        return fl.render_template("reg.html")


def delete_user_initials():

    if fl.request.method == "POST":
        initials = fl.request.form.get("initials")

        delete = db.delete_initials(connection, initials)
        if delete:
            return fl.render_template("successful_del.html")
        return fl.render_template("lose_del.html")

    if fl.request.method == "GET":
        return fl.render_template("del_user.html")


def update_user_readings():

    if fl.request.method == "POST":
        initials = fl.request.form.get("initials")
        electricity = fl.request.form.get("electricity")
        cold_water = fl.request.form.get("cold_water")
        hot_water = fl.request.form.get("hot_water")
        gas = fl.request.form.get("gas")
        if gas is None:
            gas = 0

        update = db.update_readings(connection, initials, electricity, cold_water, hot_water, gas)
        if update:
            return fl.render_template("successful_update_readings.html")
        return fl.render_template("lose_update_readings.html")

    if fl.request.method == "GET":
        return fl.render_template("update_readings.html")


def get_user_readings():
    pass


def update_user_debt():
    pass


def get_user_debt():
    pass
