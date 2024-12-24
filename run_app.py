import app
import database


if __name__ == "__main__":
    try:
        app.my_app.run(debug=True, port=5005)
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        database.close(connection=app.connection)
