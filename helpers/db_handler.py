import sqlite3


def db_handler(db, query, args=()):
    connect = sqlite3.connect(db)
    cursor = connect.cursor()
    cursor.execute(query, args)
    query_result = cursor.fetchall()
    connect.commit()
    return query_result