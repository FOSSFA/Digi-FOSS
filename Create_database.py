import sqlite3

con = sqlite3.connect('database.db')
Cur = con.cursor()
Cur.execute('''CREATE TABLE USERS 
                (name text, username text, num_id int NOT NULL unique, is_admin blob, warn int, status text)''')

con.commit()
con.close()
