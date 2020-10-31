from flask import Flask, render_template, request
from cryptography.fernet import Fernet
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

db_name = "covid"
db_host = "localhost"
db_password = ""
db_user = "root"

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('')

@app.route('/')
def questionnaire():
   return render_template('')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
         name = request.form['name']
         ans1 = request.form['ans1']
         ans2 = request.form['ans2']
         ans3 = request.form['ans3']
         ans4 = request.form['ans4']
         ans5 = request.form['ans5']
   insert(n, ans1, ans2, ans3, ans4, ans5)
   

def insert(n, q1, q2, q3, q4, q5):
        try:
            connection = mysql.connector.connect(host= db_host,database= db_name,user= db_user,password= db_password)
            cursor = connection.cursor()

            if q1==1 :
                result="yes"
        
            
            query = """INSERT INTO questionnaire(name, ques1,ques2, ques3, ques4, result) VALUES (%s, %s, %s, %s, %s, %s) """
            record = (n, q1, q2, q3, q4, q5, r)
            cursor = connection.cursor()
            cursor.execute(query,record)

            connection.commit()
            print(cursor.rowcount, "successfull")
            cursor.close()
 
            except mysql.connector.Error as error:
                print("Failed".format(error))

            finally:
               if (connection.is_connected()):
                   connection.close()
                   print("Connection is closed")

ques()









