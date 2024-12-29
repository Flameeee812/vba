import sqlite3 as sql
import logger
from .config import DATABASE


def get_connection():
    """Функция для получения базы данных"""

    connection = sql.connect(DATABASE, check_same_thread=False)
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Taxpayers (
        id INTEGER PRIMARY KEY,
        passport TEXT NOT NULL UNIQUE,
        electricity INTEGER,
        cold_water INTEGER,
        hot_water INTEGER,
        gas INTEGER,
        debt REAL DEFAULT 0.0,
        last_payment REAL DEFAULT 0.0,
        last_month_debt REAL DEFAULT 0.0
        )
        ''')
    connection.commit()

    logger.app_logger.info("База данных запущена")
    return connection


def reset_to_zero_debt(connection):
    """Функция, добавляющая задолжность за предыдущий месяц к новой

    Параметры:
    1. connection - подключение к базе данных
    """
    try:
        cursor = connection.cursor()

        cursor.execute("UPDATE Taxpayers SET last_month_debt = debt, debt = 0")
        connection.commit()
        logger.app_logger.info("Столбец debt обнулился")

    except Exception as e:
        logger.app_logger.exception(f"Ошибка при обновлении долга: {e}")


def reset_to_zero_readings(connection):
    """Функция, добавляющая задолжность за предыдущий месяц к новой

    Параметры:
    1. connection - подключение к базе данных
    """
    try:
        cursor = connection.cursor()

        cursor.execute("UPDATE Taxpayers SET electricity = 0, cold_water = 0, hot_water = 0, gas = 0")
        connection.commit()
        logger.app_logger.info("Столбцы с показаниями счётчиков обнулились")

    except Exception as e:
        logger.app_logger.exception(f"Ошибка при обновлении долга: {e}")


def add_passport(connection, passport: str):
    """Функция для добавления пользователя в базу данных

    Параметры:
    1. connection - подключение к базе данных
    2. passport - паспортные данные пользователя
    """

    cursor = connection.cursor()

    # Ошибка, если паспортные данные заданы некорректно
    if (len("".join(passport.split())) != 10) or (len(passport.split()) != 2):
        logger.app_logger.error(f"Неверное заполнение паспортных данных: {passport}")
        return 0

    # Ошибка, если паспортные данные пользователя представлеы не в числовом виде
    if all(char.isdigit() for char in passport.split()) is False:
        logger.app_logger.error(f"Введён неверный тип данных: {passport}")
        return 0

    try:
        cursor.execute("""INSERT INTO Taxpayers (passport) VALUES (?)""", (passport,))
        connection.commit()
        logger.app_logger.info(f"Пользователь {passport} успешно добавлен")
        return 1

    except sql.IntegrityError as e:
        logger.app_logger.error(f"Ошибка целостности данных: {e}")
        return 0
    except Exception as e:
        logger.app_logger.exception(f"Ошибка при добавлении пользователя: {e}")
        return 0


def delete_passport(connection, passport: str):
    """Функция для удаления пользователя из базы данных

        Параметры:
        1. connection - подключение к базе данных
        2. passport - паспортные данные пользователя
        """

    cursor = connection.cursor()

    if all(char.isdigit() for char in passport.split()) is False:
        logger.app_logger.error(f"Введён неверный тип данных: {passport}")
        return 0

    try:
        cursor.execute("SELECT COUNT(*) FROM Taxpayers WHERE passport = ?", (passport,))
        count = cursor.fetchone()[0]
        if count != 0:
            cursor.execute("DELETE FROM Taxpayers WHERE passport = ?", (passport,))
            connection.commit()
            logger.app_logger.info(f"Пользователь {passport} удалён из базы.")
            return 1

        logger.app_logger.warning(f"Попытка удалить несуществующего пользователя: {passport}")
        return 0

    except Exception as e:
        logger.app_logger.exception(f"Ошибка при удалении пользователя: {e}")
        return 0


def update_readings(connection, passport: str, electricity: str, cold_water: str, hot_water: str, gas: str):
    """Функция для обновления показаний счётчиков пользователя

        Параметры:
        1. connection - подключение к базе данных
        2. electricity - показания счётчика электричества
        3. cold_water - показания счётчика холодной воды
        4. hot_water - показания счётчика горячей воды
        5. gas - показания счётчика газа
        6. passport - паспортные данные пользователя
        """

    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM Taxpayers WHERE passport = ?", (passport,))
    if cursor.fetchone()[0] == 0:
        logger.app_logger.warning(f"Пользователь {passport} не найден в базе данных.")
        return 0

    if all(char.isdigit() for char in passport.split()) is False:
        logger.app_logger.error(f"Введён неверный тип данных: {passport}")
        return 0

    try:
        if not gas:  # Если в форму не добавили значение показания газа
            gas = 0

        cursor.execute("SELECT last_month_debt FROM Taxpayers WHERE passport = ?",
                       (passport,))
        last_month_debt = cursor.fetchone()[0]

        electricity, cold_water, hot_water, gas = map(int, [electricity, cold_water, hot_water, gas])

        # Подсчёт долга по актуальному Казансому тарифу с учётом долга за предыдущий месяц
        actual_debt = (
                round(electricity * 5.09 + cold_water * 29.41 + hot_water * 226.7 + gas * 7.47, 2) + last_month_debt)

        cursor.execute("""
            UPDATE Taxpayers 
            SET electricity = ?, cold_water = ?, hot_water = ?, gas = ?, debt = ?, last_month_debt = ?
            WHERE passport = ?
        """, (electricity, cold_water, hot_water, gas, actual_debt, 0, passport))

        connection.commit()
        logger.app_logger.info(f"Показания для пользователя {passport} успешно обновлены.")
        return 1

    except Exception as e:
        logger.app_logger.exception(f"Ошибка при добавлении показаний в базу данных: {e}")
        return 0


def get_readings(connection, passport: str):
    """Функция для получения информации о показаниях счётчиков пользователя

        Параметры:
        1. connection - подключение к базе данных
        2. passport - паспортные данные пользователя
        """

    cursor = connection.cursor()

    if all(char.isdigit() for char in passport.split()) is False:
        logger.app_logger.error(f"Введён неверный тип данных: {passport}")
        return 0

    try:
        cursor.execute("""SELECT electricity, cold_water, hot_water, gas FROM Taxpayers WHERE passport == ?""",
                       (passport,))
        readings = cursor.fetchone()

        if all([isinstance(reading, int) for reading in readings]):
            logger.app_logger.info(f"Получены данные о показаниях для пользователя: {passport}")
            return readings

        logger.app_logger.warning(f"Данные для пользователя {passport} отсутствуют в базе.")

    except Exception as e:
        logger.app_logger.exception(f"Ошибка при попытке отобразить данные о показаниях: {e}")
        return 0


def update_debt(connection, passport: str, new_payment):
    """Функция для оплаты задолжности пользователя

        Параметры:
        1. connection - подключение к базе данных
        2. passport - паспортные данные пользователя
        3. new_payment - сумма оплаты задолжности
        """

    cursor = connection.cursor()

    if all(char.isdigit() for char in passport.split()) is False:
        logger.app_logger.error(f"Введён неверный тип данных: {passport}")
        return 0

    try:
        cursor.execute("""SELECT debt FROM Taxpayers WHERE passport == ?""",
                       (passport, ))
        debt = cursor.fetchone()
        if debt:
            debt = debt[0]
            try:
                new_debt = debt - float(new_payment)

                cursor.execute("""UPDATE Taxpayers SET last_payment = ?, debt = ? WHERE passport = ?""",
                               (new_payment, new_debt, passport))
                connection.commit()
                logger.app_logger.info(f"Оплата для {passport} прошла успешно")
                return 1
            except ValueError as VE:
                logger.app_logger.exception(f"Введён неверный тип данных: {VE}")
                return 0
    except Exception as e:
        logger.app_logger.exception(f"Ошибка при попытке оплатить задолжность для {passport}: {e}")
        return 0


def get_debt(connection, passport):
    """Функция для получения информации о задолжности пользователя

        Параметры:
        1. connection - подключение к базе данных
        2. passport - паспортные данные пользователя
        """

    cursor = connection.cursor()

    if all(char.isdigit() for char in passport.split()) is False:
        logger.app_logger.error(f"Введён неверный тип данных: {passport}")
        return 0

    try:
        cursor.execute("SELECT COUNT(*) FROM Taxpayers WHERE passport = ?", (passport,))
        count = cursor.fetchone()[0]
        if count != 0:
            cursor.execute("""SELECT debt, last_month_debt FROM Taxpayers WHERE passport == ?""",
                           (passport, ))
            debt = cursor.fetchone()
            if debt[0]:
                logger.app_logger.info(f"Получены данные об остатке долга для: {passport}")
                return debt[0]
            elif debt[1]:
                logger.app_logger.info(f"Получены данные об остатке долга для: {passport}")
                return debt[1]
            logger.app_logger.info(f"Информация о задолжности {passport} отсутствует")
            return 0

        logger.app_logger.info(f"""Не удалось получить информацию об 
остатке долга, так как пользователь {passport} не зарегистрирован""")
        return 0

    except Exception as e:
        logger.app_logger.exception(f"Ошибка при попытке отобразить данные о задолжности: {e}")
        return 0


def close_conn(connection):
    """Функция для закрытия базы данных

    Параметры:
    1. connection - подключение к базе данных
    """

    connection.close()
    logger.app_logger.info("База данных закрыта")
