
import psycopg2 # для работы к PostgreSQL
import config


# Функция для подключения к базе данных
def get_db_connection():
    try:
        # Подключение к базе данных
        connection = psycopg2.connect(config.URL_DATABASE)
        print("Подключение успешно!")
        return connection
    except Exception as e:
        print(f"Ошибка при подключении к базе данных: {e}")
        return None