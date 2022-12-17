import sqlite3

connection = sqlite3.connect('skripsi.db')



cur = connection.cursor()


# print(cur.execute("DELETE FROM list_cluster"))
print(cur.execute("SELECT * FROM list_cluster LIMIT 5").fetchall())
# print(cur.fetchall())

connection.commit()
connection.close()