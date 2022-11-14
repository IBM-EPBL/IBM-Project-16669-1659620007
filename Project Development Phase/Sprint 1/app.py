from flask import Flask, render_template, url_for, redirect, session, request, flash
import re
from datetime import *
import ibm_db

app = Flask(__name__)
app.secret_key='a'

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=6667d8e9-9d4d-4ccb-ba32-21da3bb5aafc.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30376;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=kkt29633;PWD=w2Nriolg1HfcHAwB", '', '')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    global userid
    msg = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        sql = "SELECT * FROM users WHERE username=? AND password=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session['Loggedin'] = True
            session['id'] = account['USERNAME'] #USERNAME
            userid = account['USERNAME']
            session['username'] = account['USERNAME']
            # msg = "Logged in successfully!"
            return render_template('dashboard.html', msg=username)
        else:
            msg = "Invalid login credentials!"
    return render_template('login.html', msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = "Please fill out the form."
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        sql = "SELECT * FROM users WHERE username=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = "Username already exists!"
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = "Invalid email address!"
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = "Username must contain only letters and numbers!"
        else:
            insertsql = "INSERT INTO users VALUES(?,?,?)"
            prepstmt = ibm_db.prepare(conn, insertsql)
            ibm_db.bind_param(prepstmt, 1, username)
            ibm_db.bind_param(prepstmt, 2, email)
            ibm_db.bind_param(prepstmt, 3, password)
            ibm_db.execute(prepstmt)
            msg = "You have successfully created an account!"
            flash(msg)
            return redirect(url_for('index'))    
    return render_template('register.html', msg=msg)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/newdonor')
def newdonor():

    return render_template('newdonor.html')

@app.route('/regdonor', methods=['GET', 'POST'])
def regdonor():
    msg = ""
    if request.method == "POST":
        username = userid
        print(userid, "\t", session['id'])
        sql = "SELECT * FROM donor WHERE username=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print("reached account here 1", account)
        if account:
            msg = "Register as a donor only once!"
            flash(msg)
            return redirect(url_for('dashboard'))
        
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        phno = request.form['phone']
        addr = request.form['address']
        city = request.form['city']
        state = request.form['state']
        bgp = request.form['bloodgp']
        dop = request.form['dop']
        don = request.form['don']
        if int(age)<18:
            msg="You have to be an adult to donate plasma!"
        elif not valiDate(dop, don):
            msg="Your Covid Negative test should have been received atleast 14 days ago!"
        else:
            insertsql = "INSERT INTO donor VALUES(?,?,?,?,?,?,?,?,?,?,?)"
            prepstmt = ibm_db.prepare(conn, insertsql)
            ibm_db.bind_param(prepstmt, 1, username)
            ibm_db.bind_param(prepstmt, 2, name)
            ibm_db.bind_param(prepstmt, 3, age)
            ibm_db.bind_param(prepstmt, 4, gender)
            ibm_db.bind_param(prepstmt, 5, phno)
            ibm_db.bind_param(prepstmt, 6, addr)
            ibm_db.bind_param(prepstmt, 7, city)
            ibm_db.bind_param(prepstmt, 8, state)
            ibm_db.bind_param(prepstmt, 9, bgp)
            ibm_db.bind_param(prepstmt, 10, dop)
            ibm_db.bind_param(prepstmt, 11, don)
            print("prep insert - "+dop+"--"+don+"--"+addr)
            ibm_db.execute(prepstmt)
            msg = "You have successfully applied as a donor."
            print("executed insert")
            # session['isDonor'] = True
            # TEXT = "Hello,a new application for job position" +jobs+"is requested"
            # print("here2 :: ", TEXT)
        
    # elif request.method == 'POST':
    #     msg = "Please fill out the form"
    flash(msg)
    return redirect(url_for('dashboard'))

def valiDate(dop, don):
    d,m,y = [int(x) for x in dop.split('-')]
    d1 = date(d,m,y)
    d,m,y = [int(x) for x in don.split('-')]
    d2 = date(d,m,y)
    if d2>d1 and date.today()>d2+timedelta(days=14):
        return True
    return False

@app.route('/logout')
def logout():
    session.pop('Loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # session.pop('isDonor', None)
    userid = None
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)