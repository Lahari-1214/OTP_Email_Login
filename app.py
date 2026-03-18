from flask import Flask, render_template, request
app = Flask(__name__)
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/welcome', methods=['POST'])
def welcome():
    username = request.form['username']
    return render_template('dashboard.html', username=username)



if __name__ == '__main__':
    app.run(debug=True)