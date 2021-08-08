import sqlite3
conn = None
try:
    print("Connecting....")
    conn = sqlite3.connect('xyz.db')
    print("Connected")
except Error as e:
    print(e)

sql = '''SELECT * FROM MyData'''
cur = conn.cursor()

cur.execute(sql)

rows = cur.fetchall()

if len(rows)==0:
    print("Data Not Found  🙄 ")
else:
    for row in rows:
        print('''\nCourse Title : '''+row[0]+'''\nAuthor : '''+row[1]+'''\nCourse Rating : '''+str(row[2])+'''
Course Price : '''+str(row[3]))

conn.commit()
