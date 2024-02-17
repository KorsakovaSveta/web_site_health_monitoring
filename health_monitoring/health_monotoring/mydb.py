import mysql.connector
dataBase = mysql.connector.connect(user = 'root',
                                   password = '451df62G956#H26',
                                   host = 'localhost',
)

cursorObjet = dataBase.cursor()

cursorObjet.execute('CREATE DATABASE health_database')

print('Database created')
 