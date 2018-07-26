from flask import Flask, render_template, flash, redirect, url_for, session, logging,request
from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)
#This is configuring the DATABASE
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)



Articles = Articles()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    return render_template('articles.html', articles = Articles)


@app.route('/article/<string:id>/')
def article(id):
    return render_template('article.html', id=id)

@app.route('/login')
def logger():
    return render_template('login.html')

class RegistrationForm(Form):
    name = StringField('Name', [validators.Length(min=3, max=100)])
    username = StringField('Username', [validators.Length(min=5, max=100)])
    email = StringField('Email', [validators.Length(min=10, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords Do not match')
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/reg', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        cur = mysql.connection.cursor()

        #Executing the INSERT command to send the provided information to the database.
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        #Commiting the Changes to the Database
        mysql.connection.commit()

        #Closing the Connection to the data base after registration
        cur.close()
        flash('Registration Successfull','success')


        redirect(url_for('index'))
    return render_template('register.html', form=form)



if __name__=='__main__':
    app.secret_key='12344'
    app.run(debug=True, port=5430)
