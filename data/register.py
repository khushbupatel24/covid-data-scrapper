from cryptography.fernet import Fernet
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

db_name = "covid"
db_host = "localhost"
db_password = ""
db_user = "root"

def user():
    n="amrit"
    e="abd@gmail.com"
    d=2132132
    p="kjdsakdjsk"
    insert(n,e,p,d)

def insert(n,e,p,id):
        try:
            connection = mysql.connector.connect(host= db_host,database= db_name,user= db_user,password= db_password)
            cursor = connection.cursor()
           
            e=p.encode()
            key = Fernet.generate_key()
            f=Fernet(key)
            safe = f.encrypt(e)
            
            query = """INSERT INTO user(name,email,password,ID) VALUES (%s, %s, %s, %s) """
            record = (n, e, safe, id)
            cursor = connection.cursor()
            cursor.execute(query,record)

            connection.commit()
            print(cursor.rowcount, "Registration successfull")
            cursor.close()

        except mysql.connector.Error as error:
            print("Failed to signup".format(error))

        finally:
            if (connection.is_connected()):
                connection.close()
                print("Connection is closed")

user()










