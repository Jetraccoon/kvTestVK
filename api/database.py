import tarantool

from config import DATABASE_HOST, DATABASE_PORT, DATABASE_USER, DATABASE_PASSWORD


def get_tarantool_connection():
    connection = tarantool.connect(host=DATABASE_HOST,
                                   port=DATABASE_PORT,
                                   user=DATABASE_USER,
                                   password=DATABASE_PASSWORD)
    return connection


def get_user_from_db(username: str):
    connection = get_tarantool_connection()
    users_space = connection.space('users')
    user = users_space.select(username, index='username')
    return user
