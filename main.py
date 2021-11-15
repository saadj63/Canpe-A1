from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
import json

app = Flask(__name__)
 

app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'e721636c13e731'
app.config['MAIL_PASSWORD'] = 'b8959eef22be59'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'Loan'



mail = Mail(app)

mysql = MySQL(app)
@app.route("/Borrower_Info")
def hello_world():

     cur = mysql.connection.cursor()
     cur.execute('SELECT * FROM `bor`')
     row_headers=[x[0] for x in cur.description] #this will extract row headers
     rv = cur.fetchall()
     return render_template('borrower.html',data=rv)

@app.route("/mail")
def state_api():
    msg = Message('Hello from the other side!', sender ='peter@mailtrap.io', recipients = ['paul@mailtrap.io'])
    cur = mysql.connection.cursor()
    cur.execute('SELECT State, SUM(Loan_amt) as Total,SUM(Amt_paid) as Recoverd FROM bor GROUP BY State')
    rv = cur.fetchall()
   
    msg.html = render_template('test.html',data=rv)
    mail.send(msg)
    return "Message sent!"





@app.route("/graph")
def test():
    cur = mysql.connection.cursor()
    cur.execute('SELECT State, SUM(Loan_amt) as Total,SUM(Amt_paid) as Recoverd FROM bor GROUP BY State')
    rv = cur.fetchall()
    return render_template('bar_test.html',data=rv)


if __name__ == '__main__':
   app.run(debug=True)
