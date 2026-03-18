from flask import Flask, render_template, request, session, redirect, url_for
import random
import smtplib
from email.message import EmailMessage

from utils.send_email import send_otp
app = Flask(__name__)
app.secret_key = "leela@123"
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
#    session['username'] = username
    return render_template('dashboard.html', username=session.get('username'))


# Generate OTP
@app.route('/send-otp', methods=['POST'])
def send_otp_route():
    email = request.form['email']
    username = request.form['username']

    otp = random.randint(100000, 999999)

    session['otp'] = str(otp)
    session['email'] = email
    session['username'] = username

    send_otp(email, otp)

    return render_template('verify.html')

# 🔹 Step 2: Verify OTP
@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    user_otp = request.form['otp']

    if user_otp == session.get('otp'):
        return redirect(url_for('dashboard'))
    else:
        return "Invalid OTP. Please try again."

if __name__ == '__main__':
    app.run(debug=True)