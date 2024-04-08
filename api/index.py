from flask import Flask
from auth_route import auth_api



app = Flask(__name__)



app.register_blueprint(auth_api)


@app.route('/')
def home():
    return 'Hello, World! from server'

@app.route('/about')
def about():
    return 'About'

# if __name__ == '__main__':
#     app.run(debug=True)
