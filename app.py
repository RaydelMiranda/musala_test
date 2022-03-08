from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

if __name__ == '__main__':
    # Debug activated by default for testing purpose only.
    app.run(debug=True)
