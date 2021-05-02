#!/usr/bin/env python3

from flask import Flask, send_file, request, Response
from flask_socketio import SocketIO
import json
import bcrypt
import base64

# Load config
with open("config.json") as config_file:
    config = json.load(config_file)

# Load config
app = Flask(__name__)
app.config['SECRET_KEY'] = config['secret_key']
socketio = SocketIO(app)

# This is where we'll store data.
memory = {}

@app.route('/')
def index():
    return "<h1>Coming Soon</h1>"

@app.route('/api/data')
def data():
    try:
        creds = request.authorization
        if validateKey(creds["username"], creds["password"]):
            return Response(json.dumps(memory), mimetype="application/json")
        else:
            return createError(403, "Incorrect credentials.")
    except:
        return createError(401, "Please set Authorization header.")

def createError(code, message):
    return Response(json.dumps({"error": code, "reason": message}), mimetype="application/json", status=code)

def validateKey(name, password):
    current_db = config["keys"]

    try:
        hashed = config["keys"][name]
    except:
        return False

    return bcrypt.checkpw(password.encode(encoding="ascii"), base64.b64decode(hashed))

def addKey(name, key):
    # Hash password and add to the "database"
    password = base64.b64encode(bcrypt.hashpw(key.encode(encoding="ascii"), bcrypt.gensalt())).decode()
    current_db = config["keys"]
    current_db[name] = password

    # Update the file
    config["keys"] = current_db

    with open("config.json", "w+") as config_file:
        config_file.write(json.dumps(config))

if __name__ == '__main__':
    addKey("cat", "uwsu")
    socketio.run(app, host="0.0.0.0", port=config["port"], debug=config["debug"])