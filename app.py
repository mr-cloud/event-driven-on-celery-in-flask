import os
import sys

from flask import Flask, jsonify
from flask_mail import Mail

from service.arithm_producer import sub
from task.arithm.tasks import add

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret!'

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = 'flask@example.com'


# Initialize extensions
mail = Mail(app)


@app.route('/arithm/add', methods=['GET'])
def compute_add():
    # serializable
    # add.apply_async([direct_hub], serializer='pickle')
    # add()
    add.apply_async()
    return jsonify({'code': 0}), 202


@app.route('/arithm/sub', methods=['GET'])
def compute_sub():
    # serializable
    # add.apply_async([direct_hub], serializer='pickle')
    # add()
    res = sub()
    return jsonify({'code': 0, 'data': res}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5001 if len(sys.argv) < 2 else int(sys.argv[1]))
