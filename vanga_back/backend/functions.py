import datetime
import os

import psycopg2


def establish_connection():
    """Подключение к базе данных"""
    print(f'{datetime.datetime.now()} / Установка соединения')
    connection = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        port=os.getenv('DB_PORT')
    )
    connection.autocommit = True
    return connection
