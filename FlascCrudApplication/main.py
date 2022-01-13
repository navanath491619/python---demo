from flask import Flask,render_template,request, redirect, url_for
from flaskext.mysql import MySQL

import yaml


app = Flask (__name__)

#configure db
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_DATABASE_HOST'] = db['mysql_host']
app.config['MYSQL_DATABASE_USER'] = db['mysql_user']
app.config['MYSQL_DATABASE_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DATABASE_DB'] = db['mysql_db']
# app.config['MYSQL_DATABASE_CHARSET'] = 'utf-8'

print(app.config);

mysql = MySQL(autocommit=True)
mysql.init_app(app)


@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/users/create', methods=['GET','POST'])
def create():
    if request.method == 'POST':

        # fetch form data
        userDetails = request.form
        name = userDetails['name']
        email = userDetails['email']
        # cur = mysql.connection.cursor()
        cur = mysql.get_db().cursor()

        cur.execute("INSERT INTO users(name, email) VALUES(%s, %s)",(name,email))
        # mysql.connection.commit()
        cur.close()
        return redirect(url_for('users'))
    return render_template('create.html')

@app.route('/users')
def users():
    cur = mysql.get_db().cursor()
    resultValue = cur.execute("SELECT * FROM users")
    if resultValue > 0:
        userDetails =cur.fetchall()
        return render_template('users.html', userDetails=userDetails)

@app.route('/users/<id>')
def view(id):
    cur = mysql.get_db().cursor()
    resultValue = cur.execute("SELECT * FROM users where id=%s", id)
    if resultValue > 0:
        userDetails =cur.fetchall()
        return render_template('view.html', userDetails=userDetails)

@app.route('/users/<id>/edit')
def edit(id):
    cur = mysql.get_db().cursor()
    resultValue = cur.execute("SELECT * FROM users where id=%s", id)
    if resultValue > 0:
        userDetails =cur.fetchall()
        return render_template('edit.html', userDetails=userDetails)

@app.route('/users/<id>/update', methods=['POST'])
def update(id):
    cur = mysql.get_db().cursor()
    userDetails = request.form
    name = userDetails['name']
    email = userDetails['email']    
    cur.execute("UPDATE users SET name=%s, email=%s where id=%s", (name, email, id))

    cur.close()
    return redirect(url_for('users'))

@app.route('/users/<id>/delete', methods=['GET'])
def delete(id):
    cur = mysql.get_db().cursor()
    cur.execute("DELETE FROM users WHERE id=%s;", (id))
    cur.close()
    return redirect(url_for('users'))

if   __name__ == "__main__":
    app.run(debug=True)