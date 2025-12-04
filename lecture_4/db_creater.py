import sqlite3

conn = sqlite3.connect("school.db")
cursor = conn.cursor()

with open("queries.sql", 'r') as f:
    sql_script = f.read()

cursor.executescript(sql_script)

conn.commit()
conn.close()
