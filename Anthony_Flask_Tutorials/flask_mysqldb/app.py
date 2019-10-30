from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = '10.101.100.97'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'user'
app.config['MYSQL_PASSWORD'] = '1188'
app.config['MYSQL_DB'] = 'myTestdb'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


@app.route('/')
def index():
    cur = mysql.connection.cursor()
    # cur.execute('''SELECT * FROM myTestdb.products''')
    cur.execute('''SELECT * FROM products''')
    rv = cur.fetchall()     # return value from cursor is a tuple Ex: ((1, 'Milk'), (2, 'Apple'), (3, 'chicken'))
    return str(rv)

@app.route("/addone/<string:insertRecord>")
def add(insertRecord):
    cur = mysql.connection.cursor()
    cur.execute('''SELECT MAX(id) FROM products''')
    maxid = cur.fetchone()  # Example: (10, )
    cur.execute('''INSERT INTO products(name) VALUES("{0}") '''.format(insertRecord))
    mysql.connection.commit()
    return "You inserted a neww data {0} with id{1}".format(insertRecord, maxid[0] + 1)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)