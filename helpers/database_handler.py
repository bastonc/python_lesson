import sqlite3


def db_handler(query, args=()):
    # print(query)
    connect = sqlite3.connect('chinook.db')
    cursor = connect.cursor()
    cursor.execute(query, args)
    query_result = cursor.fetchall()
    return query_result
