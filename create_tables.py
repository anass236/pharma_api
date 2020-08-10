import psycopg2

connection = psycopg2.connect(user="postgres",
                              password="root",
                              host="127.0.0.1",
                              port="5432",
                              database="pharmacie")
cursor = connection.cursor()

create_table = '''CREATE TABLE IF NOT EXISTS users 
                  (id INTEGER PRIMARY KEY, username text, password text)'''
cursor.execute(create_table)

create_table = '''CREATE TABLE IF NOT EXISTS items 
                  (name text, price float)'''

cursor.execute(create_table)

connection.close()
