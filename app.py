from flask import Flask,render_template,request
from flask_mysqldb import MySQL

app=Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'users_db'

mysql = MySQL(app)

@app.route("/ad")
def ad():
    return render_template("add.html")
@app.route("/add", methods=["POST"])
def add():
    try:
        if request.method == "POST":
            name = request.form["name"]
            model = request.form["model"]
            price = request.form["price"]
            
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO cars (name, model, price) VALUES (%s, %s, %s)", (name, model, price))
            mysql.connection.commit()
            cursor.close()
            return "Car added successfully!"
    except Exception as e:
        return "An error occurred: " + str(e)

@app.route("/")
def index():
    return render_template("index.html")   

@app.route("/sale")
def sale():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT name, model, price FROM cars")
        cars_for_sale = cursor.fetchall()
        cursor.close()
        return render_template("sale.html", cars_for_sale=cars_for_sale)
    except Exception as e:
        return "An error occurred: " + str(e)
