import sqlite3

conn = sqlite3.connect('note.db')
print("数据库打开成功")
c = conn.cursor()

# select
cursor = c.execute("SELECT *  from jobs limit 1")
for row in cursor:
    print(row)
print("数据操作成功")


# update
c.execute("UPDATE jobs set d3_path = '/Users/caritasem/Downloads/tmp' where id='e04d5f86-a024-11ee-9839-186590cc0509'")
conn.commit()
print("Total number of rows updated :", conn.total_changes)

conn.close()
