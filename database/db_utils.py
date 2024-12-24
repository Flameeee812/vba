import logger
import re


def add_initials(connection, initials: str):
    cursor = connection.cursor()

    if len(initials.split()) < 2 or len(initials.split()) > 3:
        logger.app_logger.error(f"Ненврное заполнение инициалов: {initials}")
        return 0

    elif not re.match(r"^[A-Za-zА-Яа-яЁё\s]+$", initials):
        logger.app_logger.error(f"Введён неверный тип данных: {initials}")
        return 0

    try:
        cursor.execute("""INSERT INTO Taxpayers (initials) VALUES (?)""", (initials,))
        connection.commit()
        logger.app_logger.info(f"Пользователь {initials} успешно добавлен")
        return 1

    except Exception as e:
        logger.app_logger.exception(f"Ошибка при добавлении пользователя: {e}")
        return 0


def delete_initials(connection, initials: str):
    cursor = connection.cursor()

    if not re.match(r"^[A-Za-zА-Яа-яЁё\s]+$", initials):
        logger.app_logger.error(f"Введён неверный тип данных: {initials}")
        return 0

    try:
        cursor.execute("SELECT COUNT(*) FROM Taxpayers WHERE initials = ?", (initials,))
        count = cursor.fetchone()[0]
        if count > 0:
            cursor.execute("DELETE FROM Taxpayers WHERE initials = ?", (initials,))
            connection.commit()
            logger.app_logger.info(f"Пользователь {initials} удалён из базы.")
            return 1
        else:
            logger.app_logger.warning(f"Попытка удалить несуществующего пользователя: {initials}")
            return 0

    except Exception as e:
        logger.app_logger.exception(f"Ошибка при удалении пользователя: {e}")
        return 0


def update_readings(connection, initials: str, electricity: str, cold_water: str, hot_water: str, gas: str):
    cursor = connection.cursor()

    if not re.match(r"^[A-Za-zА-Яа-яЁё\s]+$", initials):
        logger.app_logger.error(f"Введён неверный тип данных: {initials}")
        return 0

    cursor.execute("SELECT COUNT(*) FROM Taxpayers WHERE initials = ?", (initials,))
    if cursor.fetchone()[0] == 0:
        logger.app_logger.warning(f"Пользователь {initials} не найден в базе данных.")
        return 0

    try:
        electricity, cold_water, hot_water, gas = map(int, [electricity, cold_water, hot_water, gas])
        debt = round(electricity * 5.09 + cold_water * 29.41 + hot_water * 226.7 + gas * 7.47, 2)
        cursor.execute(
            """
            UPDATE Taxpayers 
            SET electricity = ?, cold_water = ?, hot_water = ?, gas = ?, debt = ?
            WHERE initials = ?
            """,
            (electricity, cold_water, hot_water, gas, debt, initials)
        )
        connection.commit()
        logger.app_logger.info(f"Показания для пользователя {initials} успешно обновлены.")
        return 1

    except Exception as e:
        logger.app_logger.exception(f"Ошибка при добавлении показаний в базу данных: {e}")
        return 0


def get_readings(connection, initials: str):
    cursor = connection.cursor()

    if not re.match(r"^[A-Za-zА-Яа-яЁё\s]+$", initials):
        logger.app_logger.error(f"Введён неверный тип данных: {initials}")
        return 0

    try:
        cursor.execute("""SELECT electricity, cold_water, hot_water, gas FROM Taxpayers WHERE initials == ?""",
                       (initials,))
        readings = cursor.fetchone()

        if readings:
            logger.app_logger.info(f"Получены данные для пользователя: {initials}")
            return readings

        logger.app_logger.warning(f"Данные для пользователя {initials} отсутствуют в базе.")

    except Exception as e:
        logger.app_logger.exception(f"Ошибка при попытке отобразить данные: {e}")
        return 0


def update_debt(connection, initials: str, new_payment):
    cursor = connection.cursor()

    if not re.match(r"^[A-Za-zА-Яа-яЁё\s]+$", initials):
        logger.app_logger.error(f"Введён неверный тип данных: {initials}")
        return 0
    else:
        cursor.execute("""SELECT debt FROM Taxpayers WHERE initials == ?""",
                       (initials, ))
        debt = cursor.fetchone()
        if debt:
            debt = debt[0]
            try:
                new_debt = debt - float(new_payment)

                cursor.execute("""UPDATE Taxpayers SET payment = ?, debt = ? WHERE initials = ?""",
                               (new_payment, new_debt, initials))
                connection.commit()
                return 1
            except ValueError as VE:
                logger.app_logger.exception(f"Введён неверный тип данных: {VE}")
                return 0


def get_debt(connection, initials):
    cursor = connection.cursor()

    if not re.match(r"^[A-Za-zА-Яа-яЁё\s]+$", initials):
        logger.app_logger.error(f"Введён неверный тип данных: {initials}")
        return 0
    else:
        cursor.execute("""Select debt FROM Taxpayers WHERE initials == ?""",
                       (initials, ))
        debt = cursor.fetchone()
        return debt[0] if debt else None
