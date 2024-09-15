from flask import Flask, jsonify
from controllers.main_controller import main
from flask_cors import CORS

app = Flask(__name__, static_folder="./build/static", template_folder="./build")
app.register_blueprint(main)
CORS(app)

if __name__ == '__main__':
     app.run(debug=True)