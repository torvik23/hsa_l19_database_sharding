#!/usr/bin/env python

import os
import random
import string
import psycopg2
from psycopg2 import Error
from time import perf_counter
from functools import wraps
from memory_profiler import memory_usage


# ------------------------ Profile
def profile(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        fn_kwargs_str = ', '.join(f'{k}={v}' for k, v in kwargs.items())
        print(f'\n{fn.__name__}({fn_kwargs_str})')

        # Measure time and memory
        time_start = perf_counter()
        mem, retval = memory_usage((fn, args, kwargs), retval=True, max_usage=True)
        elapsed = perf_counter() - time_start
        print(f'Run Time: {elapsed:0.4}s')
        print('Used Memory: %iMb' % mem)

        return retval

    return inner


# ------------------------ Data
def test_shard():
    print("\nMeasure sharding performance:")
    db_host = os.environ.get('DB_HOST_SHARD', 'localhost')
    db_port = os.environ.get('DB_PORT_SHARD', '5432')
    db_name = os.environ.get('DB_NAME_SHARD', 'hsa_l19')
    db_user = os.environ.get('DB_USER_NAME_SHARD', 'hsa_user')
    db_pass = os.environ.get('DB_USER_PASSWORD_SHARD', 'aV4h5bRsgc8MB8c3')

    pg_connection = None

    try:
        pg_connection = psycopg2.connect(host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_pass)
        pg_connection.autocommit = True

        if pg_connection:
            seed_data = generate_data()
            print("=> Measure insert:")
            test_insert(pg_connection, seed_data)
            print("=> Measure select:")
            test_select(pg_connection)
            print("=> Measure delete:")
            test_delete(pg_connection)
    except Error as e:
        print("error", e)
        pass
    except Exception as e:
        print("Unknown error %s", e)
    finally:
        if pg_connection:
            pg_connection.close()


def test_noshard():
    print("\nMeasure performance without sharding:")
    db_host = os.environ.get('DB_HOST_NOSHARD', 'localhost')
    db_port = os.environ.get('DB_PORT_NOSHARD', '5435')
    db_name = os.environ.get('DB_NAME_NOSHARD', 'hsa_l19')
    db_user = os.environ.get('DB_USER_NAME_NOSHARD', 'hsa_user')
    db_pass = os.environ.get('DB_USER_PASSWORD_NOSHARD', 'aV4h5bRsgc8MB8c3')

    pg_connection = None

    try:
        pg_connection = psycopg2.connect(host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_pass)
        pg_connection.autocommit = True

        if pg_connection:
            seed_data = generate_data()
            print("=> Measure insert:")
            test_insert(pg_connection, seed_data)
            print("=> Measure select:")
            test_select(pg_connection)
            print("=> Measure delete:")
            test_delete(pg_connection)
    except Error as e:
        print("error", e)
        pass
    except Exception as e:
        print("Unknown error %s", e)
    finally:
        if pg_connection:
            pg_connection.close()


def generate_data():
    seed_num = 100000
    printable_chars = string.printable
    book_data = []
    prepared_rows = 0
    current_id = 1

    while prepared_rows < seed_num:
        book_data.append((
            current_id,
            random.randint(1, 2),
            ''.join(random.choice(printable_chars) for a in range(random.randint(5, 10))),
            ''.join(random.choice(printable_chars) for t in range(random.randint(20, 50))),
            random.randint(1990, 2020)
        ))
        current_id = current_id + 1
        prepared_rows = prepared_rows + 1

    return book_data


@profile
def test_insert(connection: psycopg2, seed_data=None):
    if seed_data is None:
        seed_data = []
    cursor = connection.cursor()
    payload = 'INSERT INTO books (id, category_id, author, title, year) VALUES (%s, %s, %s, %s, %s)'
    cursor.executemany(payload, seed_data)
    print("Number of inserted rows: %s" % cursor.rowcount)
    cursor.close()


@profile
def test_select(connection: psycopg2):
    cursor = connection.cursor()
    cursor.execute("SELECT id, category_id, author, title, year FROM books")
    print("Number of selected rows: %s" % cursor.rowcount)
    cursor.close()


@profile
def test_delete(connection: psycopg2):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM books")
    print("Number of deleted rows: %s" % cursor.rowcount)
    connection.commit()
    cursor.close()


if __name__ == '__main__':
    test_shard()
    test_noshard()
