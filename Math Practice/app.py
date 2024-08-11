from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import random

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1qaz@'  # Replace with your MySQL password
app.config['MYSQL_DB'] = 'math_website'

# Initialize MySQL
mysql = MySQL(app)

# Secret key for sessions
app.secret_key = 'your_secret_key'  # Replace with your secret key

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# User Signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()

        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO users (username, password, email) VALUES (%s, %s, %s)', (username, password, email))
            mysql.connection.commit()
            cursor.execute('INSERT INTO stats (user_id) VALUES (LAST_INSERT_ID())')
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            return redirect(url_for('login'))
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('signup.html', msg=msg)

# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return redirect(url_for('index'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg)

# User Logout
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/addition', methods=['GET', 'POST'])
def addition():
    if 'loggedin' in session:
        user_id = session['id']
        msg = ''

        if request.method == 'POST':
            number1 = int(request.form['number1'])
            number2 = int(request.form['number2'])
            correct_answer = number1 + number2
            user_answer = int(request.form['answer'])

            if user_answer == correct_answer:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('UPDATE stats SET addition_correct = addition_correct + 1 WHERE user_id = %s', [user_id])
                msg = 'Correct!'
            else:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('UPDATE stats SET addition_wrong = addition_wrong + 1 WHERE user_id = %s', [user_id])
                msg = 'Incorrect!'
            mysql.connection.commit()

        else:
            number1 = random.randint(0, 10)
            number2 = random.randint(0, 10)

        return render_template('addition.html', number1 = random.randint(0, 10), number2 = random.randint(0, 10), msg=msg)
    return redirect(url_for('login'))


@app.route('/subtraction', methods=['GET', 'POST'])
def subtraction():
    if 'loggedin' in session:
        user_id = session['id']
        msg = ''

        if request.method == 'POST':
            number1 = int(request.form['number1'])
            number2 = int(request.form['number2'])
            correct_answer = number1 - number2
            user_answer = int(request.form['answer'])

            if user_answer == correct_answer:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('UPDATE stats SET subtraction_correct = subtraction_correct + 1 WHERE user_id = %s', [user_id])
                msg = 'Correct!'
            else:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('UPDATE stats SET subtraction_wrong = subtraction_wrong + 1 WHERE user_id = %s', [user_id])
                msg = 'Incorrect!'
            mysql.connection.commit()

        else:
            number1 = random.randint(0, 10)
            number2 = random.randint(0, 10)

        return render_template('subtraction.html', number1 = random.randint(0, 10), number2 = random.randint(0, 10), msg=msg)
    return redirect(url_for('login'))


@app.route('/multiplication', methods=['GET', 'POST'])
def multiplication():
    if 'loggedin' in session:
        user_id = session['id']
        msg = ''

        if request.method == 'POST':
            number1 = int(request.form['number1'])
            number2 = int(request.form['number2'])
            correct_answer = number1 * number2
            user_answer = int(request.form['answer'])

            if user_answer == correct_answer:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('UPDATE stats SET multiplication_correct = multiplication_correct + 1 WHERE user_id = %s', [user_id])
                msg = 'Correct!'
            else:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('UPDATE stats SET multiplication_wrong = multiplication_wrong + 1 WHERE user_id = %s', [user_id])
                msg = 'Incorrect!'
            mysql.connection.commit()

        else:
            number1 = random.randint(0, 10)
            number2 = random.randint(0, 10)

        return render_template('multiplication.html', number1 = random.randint(0, 10), number2 = random.randint(0, 10), msg=msg)
    return redirect(url_for('login'))


@app.route('/division', methods=['GET', 'POST'])
def division():
    if 'loggedin' in session:
        user_id = session['id']
        msg = ''

        if request.method == 'POST':
            number1 = int(request.form['number1'])
            number2 = int(request.form['number2'])
            correct_answer = round(number1 / number2, 2)
            user_answer = float(request.form['answer'])

            if round(user_answer, 2) == correct_answer:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('UPDATE stats SET division_correct = division_correct + 1 WHERE user_id = %s', [user_id])
                msg = 'Correct!'
            else:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('UPDATE stats SET division_wrong = division_wrong + 1 WHERE user_id = %s', [user_id])
                msg = 'Incorrect!'
            mysql.connection.commit()

        else:
            number1 = random.randint(1, 10)
            number2 = random.randint(1, 10)

        return render_template('division.html', number1 = random.randint(1, 10), number2 = random.randint(1, 10), msg=msg)
    return redirect(url_for('login'))


# Stats Page
@app.route('/stats')
def stats():
    if 'loggedin' in session:
        user_id = session['id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM stats WHERE user_id = %s', [user_id])
        stats = cursor.fetchone()
        return render_template('stats.html', stats=stats)
    return redirect(url_for('login'))


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
