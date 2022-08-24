# import pyodbc
# conn = pyodbc.connect('DRIVER={KingbaseES 7 ODBC Driver};SERVER=127.0.0.1;port=54321;DATABASE=CINA_MBGZ;UID=system;PWD=cinasoft')
# cursor = conn.cursor()
# #cursor.execute( "update mbxt set name='pdw' where id=3" )
# cursor.execute( "select * from mbxt" )
# ertu = cursor.fetchall()
# print(ertu[0])

import ksycopg2
conn = ksycopg2.connect(database="CINA_MBGZ", user="SYSTEM", password="cinasoft", host="127.0.0.1", port="54321")
if conn:
        print('chenggong!!!')
# cur = conn.cursor()
# cur.execute("select * from mbxt")
# row = cur.fetchone()
# while row:
#         print("ID = ", row[0])
#         print("NAME = ", row[1], "\n")
#         row = cur.fetchone()
# conn.close()


# import psycopg2
# conn = psycopg2.connect( database="CINA_MBGZ", user="system", password="cinasoft", host="127.0.0.1",  port="54321" )
# cursor = conn.cursor()
# cursor.execute( "select * from mbxt" )
# ertu = cursor.fetchone()  #cursor.fetchall()
# print(ertu)