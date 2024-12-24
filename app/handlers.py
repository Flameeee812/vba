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
            return fl.render_template("successful_reg.html", initials=initials)
        return fl.render_template("lose_reg.html")

    if fl.request.method == "GET":
        return fl.render_template("reg_user.html")


def delete_user_initials():

    if fl.request.method == "POST":
        initials = fl.request.form.get("initials")

        delete = db.delete_initials(connection, initials)
        if delete:
            return fl.render_template("successful_del.html", initials=initials)
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

        update = db.update_readings(connection, initials, electricity, cold_water, hot_water, gas)
        if update:
            return fl.render_template("successful_update_readings.html", initials=initials)
        return fl.render_template("lose_update_readings.html")

    if fl.request.method == "GET":
        return fl.render_template("update_readings.html")


def get_user_readings():
    if fl.request.method == "POST":
        initials = fl.request.form.get("initials")

        readings = db.get_readings(connection, initials)
        if readings:
            return fl.render_template("successful_get_readings.html",
                                      initials=initials,
                                      electricity=readings[0],
                                      cold_water=readings[1],
                                      hot_water=readings[2],
                                      gas=readings[3])
        return fl.render_template("lose_get_readings.html")

    if fl.request.method == "GET":
        return fl.render_template("get_readings.html")


def update_user_debt():
    if fl.request.method == "POST":
        initials = fl.request.form.get("initials")
        new_payment = fl.request.form.get("new_payment")

        new_debt = db.update_debt(connection, initials, new_payment)
        if new_debt:
            return fl.render_template("successful_update_debt.html", initials=initials)
        return fl.render_template("lose_update_debt.html")

    if fl.request.method == "GET":
        return fl.render_template("update_debt.html")


def get_user_debt():
    if fl.request.method == "POST":
        initials = fl.request.form.get("initials")

        new_debt = db.get_debt(connection, initials)
        if new_debt:
            return fl.render_template("successful_get_debt.html",
                                      initials=initials,
                                      new_debt=new_debt)
        return fl.render_template("lose_get_debt.html")

    if fl.request.method == "GET":
        return fl.render_template("get_debt.html")
