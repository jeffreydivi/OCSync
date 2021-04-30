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

@app.route('/')
def index():
    return "hello there"

# From https://www.geeksforgeeks.org/python-program-for-binary-search/
def binSearchDict(arr, name):
    high = len(arr)
    low = 0
    mid = (high + low) // 2

    if high >= low:
        if arr[mid]["name"] < name:
            low = mid + 1
        # If x is smaller, ignore right half
        elif arr[mid]["name"] > name:
            high = mid - 1
        # means x is present at mid
        else:
            return mid
    return -1

def validateKey(name, password):
    current_db = config["keys"]

    idx = binSearchDict(current_db, name)
    if (idx == -1):
        return False

    hashed = config["keys"][idx]["key"]

    return bcrypt.checkpw(password.encode(encoding="ascii"), base64.b64decode(hashed))
    # hashed = name in config["keys"]

def addKey(name, key):
    # Hash password and add to the "database"
    password = base64.b64encode(bcrypt.hashpw(key.encode(encoding="ascii"), bcrypt.gensalt())).decode()
    current_db = config["keys"]
    current_db.append({"name": name, "key": password})

    # Sort the DB so we can do O(log n) search.
    current_db = sorted(current_db, key=lambda item: item['name'])

    # Update the file
    config["keys"] = current_db

    with open("config.json", "w+") as config_file:
        config_file.write(json.dumps(config))

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=config["port"], debug=config["debug"])