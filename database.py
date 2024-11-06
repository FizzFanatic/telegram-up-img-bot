
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


# Функция для добавления пользователя в базу данных или обновления баланса
def add_user_to_db(telegram_id):
    try:
        # Подключение к базе данных
        conn = get_db_connection()
        cursor = conn.cursor()

        # Проверка, существует ли пользователь в базе
        cursor.execute('SELECT * FROM users WHERE telegram_id = %s', (telegram_id,))
        user = cursor.fetchone()

        if user is None:
            # Если пользователя нет в базе, добавляем нового с 5 кредитами
            cursor.execute('INSERT INTO users (telegram_id, account_credit_balance) VALUES (%s, %s)', (telegram_id, 5))
            conn.commit()
            return True  # Новый пользователь добавлен
        else:
            # Если пользователь уже существует, ничего не делаем
            return False
    except Exception as e:
        print(f"Ошибка при работе с базой данных: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


# Функция для получения баланса пользователя
def get_user_balance(telegram_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT account_credit_balance FROM users WHERE telegram_id = %s', (telegram_id,))
        result = cursor.fetchone()
        if result:
            return result[0]  # Возвращаем баланс
        else:
            return None  # Пользователь не найден
    except Exception as e:
        print(f"Ошибка при запросе к базе данных: {e}")
        return None
    finally:
        cursor.close()
        conn.close()
