from datetime import datetime, timedelta

from flask import Flask, flash, render_template, request, session, redirect, url_for
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

    otp = random.randint(100000, 999999) #or we can also use function inside utils to generate otp

    session['otp'] = str(otp)
    session['email'] = email
    session['username'] = username

    session['otp_expiry'] = (datetime.now() + timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")

    send_otp(email, otp)
    flash("OTP sent to your email ✅", "success")
    return render_template('verify.html')

# 🔹 Step 2: Verify OTP
@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    user_otp = request.form['otp']

    stored_otp = session.get('otp')
    expiry_time = session.get('otp_expiry')

    if not stored_otp or not expiry_time:
        flash("Session expired. Please try again.", "error")
        return redirect(url_for('login'))

    # Convert string back to datetime
    expiry_time = datetime.strptime(expiry_time, "%Y-%m-%d %H:%M:%S")

    if datetime.now() > expiry_time:
        flash("OTP expired ⏰. Please request a new one.", "error")
        return redirect(url_for('login'))

    if user_otp == stored_otp:
        flash("Login successful 🎉", "success")
        return redirect(url_for('dashboard'))
    else:
        flash("Invalid OTP ❌", "error")
        return redirect(url_for('login'))
    
@app.route('/resend-otp')
def resend_otp():
    email = session.get('email')

    if not email:
        flash("Session expired. Please login again.", "error")
        return redirect(url_for('login'))

    otp = str(random.randint(100000, 999999))

    session['otp'] = otp
    session['otp_expiry'] = (datetime.now() + timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")

    send_otp(email, otp)

    flash("New OTP sent 📩", "success")
    return render_template('verify_otp.html')

if __name__ == '__main__':
    app.run(debug=True)