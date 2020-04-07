import sqlite3

dbConn = sqlite3.connect('./data/userInfo.db')

dbConn.execute('''create table users(
                username varchar(10) primary key not null,
                password varchar(50) not null
                )''')

dbConn.close()