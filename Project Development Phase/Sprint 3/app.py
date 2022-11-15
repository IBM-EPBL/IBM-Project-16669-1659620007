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

#----------------------------NORMAL USER ROUTES-----------------------------------

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
            session['id'] = account['USERNAME']
            userid = account['USERNAME']
            session['username'] = account['USERNAME']
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
    return render_template('dashboard.html', msg=userid)

@app.route('/newdonor')
def newdonor():
    return render_template('newdonor.html')

@app.route('/newrequest')
def newrequest():
    return render_template('newrequest.html')

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

@app.route('/regrequest', methods=['GET', 'POST'])
def regrequest():
    msg = ""
    if request.method == "POST":
        username = userid
        pname = request.form['pname']
        print(userid, "\t", session['id'], "pname = ", pname)
        sql = "SELECT * FROM requests WHERE username=? AND pname=?" #patient's name = pname
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.bind_param(stmt, 2, pname)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print("reached account here for pname", account)
        if account:
            msg = "Register for a patient only once!"
            flash(msg)
            return redirect(url_for('dashboard'))
        
        phno = request.form['phone']
        paddr = request.form['paddress']
        city = request.form['city']
        state = request.form['state']
        bgp = request.form['bloodgp']

        insertsql = "INSERT INTO requests VALUES(?,?,?,?,?,?,?)"
        prepstmt = ibm_db.prepare(conn, insertsql)
        ibm_db.bind_param(prepstmt, 1, username)
        ibm_db.bind_param(prepstmt, 2, pname)
        ibm_db.bind_param(prepstmt, 3, phno)
        ibm_db.bind_param(prepstmt, 4, paddr)
        ibm_db.bind_param(prepstmt, 5, city)
        ibm_db.bind_param(prepstmt, 6, state)
        ibm_db.bind_param(prepstmt, 7, bgp)
        print("prep insert - "+username+"--"+pname+"--"+bgp)
        ibm_db.execute(prepstmt)
        msg = "You have successfully requested plasma."
        print("executed insert")        
    flash(msg)
    return redirect(url_for('dashboard'))

@app.route('/pastrequests')
def pastrequests():
    username = userid
    flag = 0
    data = []
    sql = "SELECT pname,phone_number,paddress,city,state,blood_gp FROM requests WHERE username=?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, username)
    ibm_db.execute(stmt)
    request = ibm_db.fetch_tuple(stmt)
    while request != False:
        flag = 1 #atleast 1 match is found
        data.append(request)
        request = ibm_db.fetch_tuple(stmt)
    if not flag:
        msg = "You have made 0 requests!"
        flash(msg)
        return redirect(url_for('dashboard'))
    else:
        print("No of requests = ", len(data))
        data = tuple(data)
        headings = ("Patient's Name", "Emergency Contact", "Patient's Address", "City", "State", "Blood Group Requested", "Options")
        return render_template('userrequests.html', msg=userid, data=data, headings=headings)


#----------------------------ADMIN ROUTES-----------------------------------

@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    global adminid
    msg = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        sql = "SELECT * FROM admins WHERE username=? AND password=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session['Loggedin'] = True
            session['id'] = account['USERNAME']
            adminid = account['USERNAME']
            session['username'] = account['USERNAME']
            return render_template('admindashboard.html', msg=username)
        else:
            msg = "Invalid admin credentials!"
    return render_template('adminlogin.html', msg=msg)

@app.route('/admindashboard')
def admindashboard():
    return render_template('admindashboard.html', msg=adminid)

@app.route('/allrequests')
def allrequests():
    data, bgps = [], []
    flag = 0
    sql = "SELECT * FROM requests"
    stmt = ibm_db.exec_immediate(conn, sql)
    request = ibm_db.fetch_tuple(stmt)
    while request != False:
        flag = 1 #atleast 1 match is found
        data.append(request)
        request = ibm_db.fetch_tuple(stmt)
    if not flag:
        msg = "There are 0 requests!"
        flash(msg)
        return redirect(url_for('admindashboard'))
    else:
        print("No of requests = ", len(data))
        data = tuple(data)
        headings = ("Username", "Patient's Name", "Emergency Contact", "Patient's Address", "City", "State", "Blood Group Requested", "Options")
        return render_template('viewallreqs.html', msg=adminid, data=data, headings=headings)

@app.route('/approvereq', methods=['POST','GET'])
def approvereq():
    if request.method == "POST":
        bgp = request.form["bgp"]
        print("Request approved for bgp = ", bgp)

        pname = request.form['pname']
        phno = request.form['phone']
        state  = request.form['state']
        
        insertsql = "INSERT INTO approved_requests VALUES(?,?,?,?)"
        prepstmt = ibm_db.prepare(conn, insertsql)
        ibm_db.bind_param(prepstmt, 1, pname)
        ibm_db.bind_param(prepstmt, 2, phno)
        ibm_db.bind_param(prepstmt, 3, state)
        ibm_db.bind_param(prepstmt, 4, bgp)
        ibm_db.execute(prepstmt)
        msg = "You have successfully approved a request."
        print("executed insert")        
    flash(msg)
    return redirect(url_for('admindashboard'))


#----------------------------GENERAL LOGOUT ROUTES-----------------------------------

@app.route('/deletereq', methods=['GET','POST'])
def deletereq():
    if request.method == 'POST':
        username = request.form['username']
        pname = request.form['pname']
        delsql = "DELETE FROM requests WHERE username=? AND pname=?"
        prepstmt = ibm_db.prepare(conn, delsql)
        ibm_db.bind_param(prepstmt, 1, username)
        ibm_db.bind_param(prepstmt, 2, pname)
        ibm_db.execute(prepstmt)
        msg = "You have successfully deleted the request."
        print("executed delete: ", pname)
        flash(msg)
        if 'userid' in globals():
            return redirect(url_for('dashboard'))
        elif 'adminid' in globals():
            return redirect(url_for('admindashboard'))

@app.route('/logout')
def logout():
    session.pop('Loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # session.pop('isDonor', None)
    if 'userid' in globals():
        userid = None
    elif 'adminid' in globals():
        adminid = None
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)