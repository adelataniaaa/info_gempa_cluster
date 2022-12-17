import sqlite3

connection = sqlite3.connect('skripsi.db')


with open('schema.sql') as f:
    sql_script = f.read()

cur = connection.cursor()

cur.executescript(sql_script)

cur.execute("INSERT INTO list_cluster (tgl, ot, lat, lon, depth, mag, remark, cluster) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",('26-11-2022', 'test', 0.6, 0.7, 12, 'test', 'test', 1))


# cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
#             ('Second Post', 'Content for the second post')
#             )

connection.commit()
connection.close()