import sqlite3

try:
    sqlite_connection = sqlite3.connect('dogs.db')
    cursor = sqlite_connection.cursor()
    print("База данных запущена")


    create_dogs_table_query = '''
    CREATE TABLE IF NOT EXISTS Dogs (
        ID INTEGER PRIMARY KEY,
        Name TEXT,
        Breed TEXT
    );
    '''
    cursor.execute(create_dogs_table_query)

    sqlite_connection.commit()
    cursor.close()

except sqlite3.Error as error:
    print("Ошибка при подключении к SQLite:", error)
finally:
    if sqlite_connection:
        sqlite_connection.close()
        print("Соединение с БД закрыто")