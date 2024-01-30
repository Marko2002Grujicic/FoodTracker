import html
from flask import Flask, redirect, render_template, request, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import mariadb
import mysql.connector

konekcija = mysql.connector.connect(
    passwd="",
    user="root",
    database="food_tracker",
    port="3306",
    auth_plugin="mysql_native_password"
)

kursor = konekcija.cursor(dictionary=True)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def render_login() -> 'html':
    return render_template('login.html')

@app.route('/home', methods=['GET'])
def render_home() -> 'html':
    upit="select * from accounts"
    return render_template('dashboard.html')

@app.route('/edit', methods=['GET','POST', 'DELETE'])
def render_edit() -> 'html':
   if request.method == 'GET':
      upit = "select * from accounts where id=%s"
      vrednost = (7, )
      kursor.execute(upit, vrednost)
      account = kursor.fetchone()

      return render_template('edit-user.html', account = account)

   if request.method == 'POST':
      upit = """ update accounts set 
                name = %s, weight = %s, height = %s, gender = %s, activity = %s, email = %s, password = %s, calories = %s, role = %s
                where id = %s
      """
      forma = request.form
      vrednosti = (
            forma['name'],
            forma['weight'],
            forma['height'],
            forma['gender'],
            forma['activity'],
            forma['email'],
            forma['password'],
            forma['calories'],
            forma['role'],
            7
            )
      kursor.execute(upit, vrednosti)
      konekcija.commit()
      return redirect(url_for('render_home'))
   
   if request.method == 'DELETE':
      upit = """ DELETE FROM accounts WHERE id=%s """
      vrednost = (7, )
      kursor.execute(upit, vrednost)
      konekcija.commit()
      return redirect(url_for('render_login'))      

@app.route('/create', methods=['GET', 'POST'])    
def render_create_account() -> 'html':
    if request.method == "GET":
     return render_template('create-user.html')
    
    if request.method == "POST":
     forma = request.form
     hesovana_lozinka = generate_password_hash(forma['password'])
     vrednosti = (
            forma['name'],
            forma['weight'],
            forma['height'],
            forma['gender'],
            forma['activity'],
            forma['email'],
            hesovana_lozinka,
            forma['calories'],
            forma['role']
            )
     upit = """insert into 
            accounts(name, weight, height, gender, activity, email, password, calories, role)
            values(%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
     kursor.execute(upit, vrednosti)
     konekcija.commit()
     return redirect(url_for('render_home'))

app.run(debug=True)