import sqlite3
conn = sqlite3.connect('sort.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM posts")
print(cursor.fetchall())
cursor.close()
conn.close()
print("Hello World")