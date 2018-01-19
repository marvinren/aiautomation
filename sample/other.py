import pymysql

conn = pymysql.connect(host='10.12.1.23', port=3306, user='root', passwd='Yijiceshi4!', db='autotest')

cur = conn.cursor()
cur.execute("SELECT * FROM case_exec_log")
for r in cur.fetchall():
           print(r)
           #cur.close()
conn.close()

