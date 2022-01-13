from flask import Flask, render_template, request, redirect, url_for
from flaskext.mysql import MySQL
from test import navnath

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'flaskapp'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users')
def users():
    conn = mysql.connect()
    cursor =conn.cursor()

    cursor.execute("SELECT * from users")
    data = cursor.fetchall()

    return render_template('users.html', users=data)

@app.route('/users/create')
def create():
    return render_template('create.html')

@app.route('/users/create-user', methods=['POST'])
def createUser():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    gender = request.form.get('gender')
    city = request.form.get('city')
    address = request.form.get('address')

    conn = mysql.connect()
    cursor =conn.cursor()

    cursor.execute("INSERT INTO users (`name`, `email`, phone , gender , address ) VALUES (%s, %s, %s ,%s ,%s)", (name, email,phone,gender,address))
    conn.commit()
    
    return redirect(url_for('users'))

@app.route('/users/<id>/view')
def view(id):
    cur = mysql.get_db().cursor()
    resultValue = cur.execute("SELECT * FROM users where id=%s", id)
    if resultValue> 0:
        userDetails=cur.fetchone()
        return render_template('view.html',user=userDetails) 

@app.route('/users/<id>/edit')
def edit(id):
    cur = mysql.get_db().cursor()
    resultValue = cur.execute("SELECT * FROM users where id=%s", id)
    userDetails =cur.fetchone()
    return render_template('edit.html', user=userDetails)


@app.route('/users/<id>/update', methods=['POST'])
def update(id):
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    address= request.form.get('address')
    gender = request.form.get('gender')
    
    cur = mysql.get_db().cursor()
    resultValue = cur.execute("UPDATE users  SET name= %s, email= %s, phone= %s,  address= %s, gender= %s  WHERE  id  = %s", (email, name, phone,address, gender,id))
    userDetails =cur.fetchone()
    
    return redirect(url_for('users'))

@app.route('/users/<id>/delete', methods=['GET'])
def delete(id):
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute("DELETE from users where id=%s", id)
    conn.commit()
    return redirect(url_for('users'))

@app.route('/test', methods=['GET'])
def test():
    print(navnath)
    print(type(navnath))
    return "..."

if __name__ == "__main__":
    app.run(debug=True)