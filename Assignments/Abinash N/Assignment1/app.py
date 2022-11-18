# Store this code in 'app.py' file

from flask import Flask, render_template, request, redirect, url_for, session
import re
from randimage import get_random_image, show_array
import matplotlib
from email_validator import validate_email, EmailNotValidError
import phonenumbers
import wikipedia
from quoters import Quote


app = Flask(__name__)


app.secret_key = 'IBM'


@app.route('/')
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if(request.method=='GET'):
        img_size = (128,128)
        img = get_random_image(img_size)  #returns numpy array
        matplotlib.image.imsave("static//profile.png", img)
        text=Quote.print()
        return render_template('register.html',quote=text)
    if request.method == 'POST' and 'username' in request.form  and 'email' in request.form and 'phone' in request.form :
        msg={}
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        msg['username']=username
        msg['email']=email
        msg['phone']=phone
        desc=wikipedia.summary(username,sentences=4)
        is_new_account = True # False for login pages
        try:
            z = phonenumbers.parse(phone, None)
        except:
            return render_template('register.html', msg = "Phone number not valid")
        try:
            validation = validate_email(email, check_deliverability=is_new_account)
            email = validation.email
        except EmailNotValidError as e:
            return render_template('register.html', msg = "Email id not valid")
        return render_template('login.html', msg = msg,desc=desc)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
        return render_template('register.html', msg = msg)


if __name__ == '__main__':
    app.run(debug=True)