from flask import Flask
from auth_route import auth_api
import sqlite3

app = Flask(__name__)

def create_table():
    conn = sqlite3.connect('prediction.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    username TEXT UNIQUE,
                    email TEXT UNIQUE,
                    password TEXT

              )''')
    conn.commit()
    conn.close()

create_table()

app.register_blueprint(auth_api)


@app.route('/')
def home():
    return 'Hello, World! from server'

@app.route('/about')
def about():
    return 'About'

if __name__ == '__main__':
    app.run(debug=True)
