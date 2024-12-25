import flask as fl
import database as db


def home_handler():
    """Хендлер для домашней страницы"""

    return fl.render_template("home.html")


def registration():
    """Хендлер для страницы регистрации"""

    if fl.request.method == "POST":
        passport = fl.request.form.get("passport")

        reg = db.add_passport(db.connection, passport)
        if reg:
            return fl.render_template("successful_reg.html", passport=passport)
        return fl.render_template("lose_reg.html")

    if fl.request.method == "GET":
        return fl.render_template("reg_user.html")


def delete_user_passport():
    """Хендлер для страницы удаления пользователя"""

    if fl.request.method == "POST":
        passport = fl.request.form.get("passport")

        delete = db.delete_passport(db.connection, passport)
        if delete:
            return fl.render_template("successful_del.html", passport=passport)
        return fl.render_template("lose_del.html")

    if fl.request.method == "GET":
        return fl.render_template("del_user.html")


def update_user_readings():
    """Хендлер для страницы обновления показаний счётчиков"""

    if fl.request.method == "POST":
        passport = fl.request.form.get("passport")
        electricity = fl.request.form.get("electricity")
        cold_water = fl.request.form.get("cold_water")
        hot_water = fl.request.form.get("hot_water")
        gas = fl.request.form.get("gas")

        update = db.update_readings(db.connection, passport, electricity, cold_water, hot_water, gas)
        if update:
            return fl.render_template("successful_update_readings.html", passport=passport)
        return fl.render_template("lose_update_readings.html")

    if fl.request.method == "GET":
        return fl.render_template("update_readings.html")


def get_user_readings():
    """Хендлер для страницы получения информации о показаниях счётчиков"""

    if fl.request.method == "POST":
        passport = fl.request.form.get("passport")

        readings = db.get_readings(db.connection, passport)
        if readings:
            return fl.render_template("successful_get_readings.html",
                                      passport=passport,
                                      electricity=readings[0],
                                      cold_water=readings[1],
                                      hot_water=readings[2],
                                      gas=readings[3])
        return fl.render_template("lose_get_readings.html")

    if fl.request.method == "GET":
        return fl.render_template("get_readings.html")


def update_user_debt():
    """Хендлер для страницы оплаты задолжности"""

    if fl.request.method == "POST":
        passport = fl.request.form.get("passport")
        new_payment = fl.request.form.get("new_payment")

        new_debt = db.update_debt(db.connection, passport, new_payment)
        if new_debt:
            return fl.render_template("successful_update_debt.html", passport=passport)
        return fl.render_template("lose_update_debt.html")

    if fl.request.method == "GET":
        return fl.render_template("update_debt.html")


def get_user_debt():
    """Хендлер для страницы получния информации о задолжности"""

    if fl.request.method == "POST":
        passport = fl.request.form.get("passport")

        new_debt = db.get_debt(db.connection, passport)
        if new_debt:
            return fl.render_template("successful_get_debt.html",
                                      passport=passport,
                                      new_debt=new_debt)
        return fl.render_template("lose_get_debt.html")

    if fl.request.method == "GET":
        return fl.render_template("get_debt.html")
