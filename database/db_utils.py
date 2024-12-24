import re
import datetime
import logger


def add_initials(connection, initials: str):
    """Функция для добавления пользователя в базу данных

    Параметры:
    1. connection - подключение к базе данных
    2. initials - инициалы пользователя
    """

    cursor = connection.cursor()

    # Ошибка, если количество слов в инициалах заданы некорректно
    if len(initials.split()) < 2 or len(initials.split()) > 3:
        logger.app_logger.error(f"Ненврное заполнение инициалов: {initials}")
        return 0

    # Ошибка, если инициалы пользователя представлеы не в буквенном виде
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
    """Функция для удаления пользователя из базы данных

        Параметры:
        1. connection - подключение к базе данных
        2. initials - инициалы пользователя
        """

    cursor = connection.cursor()

    if not re.match(r"^[A-Za-zА-Яа-яЁё\s]+$", initials):
        logger.app_logger.error(f"Введён неверный тип данных: {initials}")
        return 0

    try:
        cursor.execute("SELECT COUNT(*) FROM Taxpayers WHERE initials = ?", (initials,))
        count = cursor.fetchone()[0]
        if count != 0:
            cursor.execute("DELETE FROM Taxpayers WHERE initials = ?", (initials,))
            connection.commit()
            logger.app_logger.info(f"Пользователь {initials} удалён из базы.")
            return 1

        logger.app_logger.warning(f"Попытка удалить несуществующего пользователя: {initials}")
        return 0

    except Exception as e:
        logger.app_logger.exception(f"Ошибка при удалении пользователя: {e}")
        return 0


def update_readings(connection, initials: str, electricity: str, cold_water: str, hot_water: str, gas: str):
    """Функция для обновления показаний счётчиков пользователя

        Параметры:
        1. connection - подключение к базе данных
        2. electricity - показания счётчика электричества
        3. cold_water - показания счётчика холодной воды
        4. hot_water - показания счётчика горячей воды
        5. gas - показания счётчика газа
        6. initials - инициалы пользователя
        """

    cursor = connection.cursor()
    day = datetime.datetime.now().day  # день подачи показаний
    month = datetime.datetime.now().month  # месяц подачи показаний
    year = datetime.datetime.now().year  # год подачи показаний

    cursor.execute("SELECT COUNT(*) FROM Taxpayers WHERE initials = ?", (initials,))
    if cursor.fetchone()[0] == 0:
        logger.app_logger.warning(f"Пользователь {initials} не найден в базе данных.")
        return 0

    if not re.match(r"^[A-Za-zА-Яа-яЁё\s]+$", initials):
        logger.app_logger.error(f"Введён неверный тип данных: {initials}")
        return 0

    try:
        if not gas:  # Если в форму не добавили значение показания газа
            gas = 0

        electricity, cold_water, hot_water, gas = map(int, [electricity, cold_water, hot_water, gas])
        # Подсчёт долга по актуальному Казансому тарифу
        debt = round(electricity * 5.09 + cold_water * 29.41 + hot_water * 226.7 + gas * 7.47, 2)
        cursor.execute("SELECT debt, month, year FROM Taxpayers WHERE initials = ?",
                       (initials,))
        result = cursor.fetchone()
        current_debt, last_calculated_month, last_calculated_year = result

        # Обновление оплаты после 15 числа нового/нынешнего месяца
        if (day >= 15) or (month > last_calculated_month) or (year > last_calculated_year):
            debt += current_debt

        cursor.execute("""
            UPDATE Taxpayers 
            SET electricity = ?, cold_water = ?, hot_water = ?, gas = ?, debt = ?, month = ?, year = ?
            WHERE initials = ?
        """, (electricity, cold_water, hot_water, gas, debt, month, year, initials))

        connection.commit()
        logger.app_logger.info(f"Показания для пользователя {initials} успешно обновлены.")
        return 1

    except Exception as e:
        logger.app_logger.exception(f"Ошибка при добавлении показаний в базу данных: {e}")
        return 0


def get_readings(connection, initials: str):
    """Функция для получения информации о показаниях счётчиков пользователя

        Параметры:
        1. connection - подключение к базе данных
        2. initials - инициалы пользователя
        """

    cursor = connection.cursor()

    if not re.match(r"^[A-Za-zА-Яа-яЁё\s]+$", initials):
        logger.app_logger.error(f"Введён неверный тип данных: {initials}")
        return 0

    try:
        cursor.execute("""SELECT electricity, cold_water, hot_water, gas FROM Taxpayers WHERE initials == ?""",
                       (initials,))
        readings = cursor.fetchone()

        if readings:
            logger.app_logger.info(f"Получены данные о показаниях для пользователя: {initials}")
            return readings

        logger.app_logger.warning(f"Данные для пользователя {initials} отсутствуют в базе.")

    except Exception as e:
        logger.app_logger.exception(f"Ошибка при попытке отобразить данные: {e}")
        return 0


def update_debt(connection, initials: str, new_payment):
    """Функция для оплаты задолжности пользователя

        Параметры:
        1. connection - подключение к базе данных
        2. initials - инициалы пользователя
        3. new_payment - сумма оплаты задолжности
        """
    
    cursor = connection.cursor()

    if not re.match(r"^[A-Za-zА-Яа-яЁё\s]+$", initials):
        logger.app_logger.error(f"Введён неверный тип данных: {initials}")
        return 0

    cursor.execute("""SELECT debt FROM Taxpayers WHERE initials == ?""",
                   (initials, ))
    debt = cursor.fetchone()
    if debt:
        debt = debt[0]
        try:
            new_debt = debt - float(new_payment)

            cursor.execute("""UPDATE Taxpayers SET last_payment = ?, debt = ? WHERE initials = ?""",
                           (new_payment, new_debt, initials))
            connection.commit()
            logger.app_logger.info(f"Значение debt для {initials} обновлены")
            return 1
        except ValueError as VE:
            logger.app_logger.exception(f"Введён неверный тип данных: {VE}")
            return 0


def get_debt(connection, initials):
    """Функция для получения информации о задолжности пользователя

        Параметры:
        1. connection - подключение к базе данных
        2. initials - инициалы пользователя
        """
    
    cursor = connection.cursor()

    if not re.match(r"^[A-Za-zА-Яа-яЁё\s]+$", initials):
        logger.app_logger.error(f"Введён неверный тип данных: {initials}")
        return 0

    cursor.execute("""Select debt FROM Taxpayers WHERE initials == ?""",
                   (initials, ))
    debt = cursor.fetchone()
    logger.app_logger.info(f"Получены данные об остатке долга для: {initials}")
    return debt[0] if debt else None
