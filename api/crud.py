from database import get_tarantool_connection


def write_data(data: dict):
    conn = get_tarantool_connection()
    for key, value in data.items():
        conn.replace('kv_store', (str(key), str(value)))


def read_data(keys: list):
    conn = get_tarantool_connection()
    result = {}
    for key in keys:
        res = conn.select('kv_store', key)
        if res:
            result[key] = res[0][1]
    return result
