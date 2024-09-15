from flask import Flask, jsonify
from controllers.main_controller import main
from flask_cors import CORS
from waitress import serve

app = Flask(__name__, static_folder="./build/static", template_folder="./build")
app.register_blueprint(main)
CORS(app, supports_credentials=True)

if __name__ == '__main__':
     # app.run(debug=True)
     serve(app, host='0.0.0.0', port=5000)