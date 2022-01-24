#!/usr/bin/env python

import os
import random
import string
import psycopg2
from psycopg2 import Error

db_host = os.environ.get('DB_HOST', 'localhost')
db_port = os.environ.get('DB_PORT', '5435')
db_name = os.environ.get('DB_NAME', 'hsa_l19')
db_user = os.environ.get('DB_USER_NAME', 'hsa_user')
db_pass = os.environ.get('DB_USER_PASSWORD', 'aV4h5bRsgc8MB8c3')

SEED_NUM = 1000000
printable_chars = string.printable
pgConnection = None

try:
    pgConnection = psycopg2.connect(host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_pass)
    pgConnection.autocommit = True
    if pgConnection:
        cursor = pgConnection.cursor()
        n = 1

        print("Generate %s rows for no-shard container..." % SEED_NUM)
        book_data = []
        while True:
            if n > SEED_NUM:
                break

            book_data.append((
                n,
                random.randint(1, 2),
                ''.join(random.choice(printable_chars) for a in range(random.randint(5, 10))),
                ''.join(random.choice(printable_chars) for t in range(random.randint(20, 50))),
                random.randint(1990, 2020)
            ))
            n += 1

        book_payload = 'INSERT INTO books (id, category_id, author, title, year) VALUES (%s, %s, %s, %s, %s)'
        cursor.executemany(book_payload, book_data)
        print("Done!")
except Error as e:
    print("error", e)
    pass
except Exception as e:
    print("Unknown error %s", e)
finally:
    # closing database connection.
    if pgConnection:
        cursor.close()
        pgConnection.close()
