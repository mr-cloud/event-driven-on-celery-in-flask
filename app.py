import os
import sys

from flask import Flask, jsonify, request
from flask_mail import Mail

from service.arithm_producer import sub, add, unclaimed_msg

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret!'


@app.route('/arithm/add', methods=['POST'])
def compute_add():
    content = request.get_json()
    add(content['a'], content['b'])
    return jsonify({'code': 0}), 202


@app.route('/arithm/sub', methods=['GET'])
def compute_sub():
    res = sub()
    return jsonify({'code': 0, 'data': res}), 200


@app.route('/arithm/none', methods=['GET'])
def compute_none():
    res = unclaimed_msg()
    return jsonify({'code': 0, 'data': res}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5001 if len(sys.argv) < 2 else int(sys.argv[1]), threaded=True)
