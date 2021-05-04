#!/usr/bin/env python3
from flask import Flask, send_file, request, Response
from flask_socketio import SocketIO
import json
import bcrypt
import base64
import threading
import os

# Load config
with open("config.json") as config_file:
    config = json.load(config_file)

# Load config
app = Flask(__name__, static_url_path="/static")
app.config['SECRET_KEY'] = config['secret_key']
socketio = SocketIO(app)

# Note: Connect with a "normal" WebSockets connection with the following URL:
# ws://localhost:8080/socket.io/?EIO=3&transport=websocket

# This is where we'll store data.
memory = {}

@app.route('/')
def index():
    return send_file("static/index.html")

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

# Please, please, please! Use WSS (WebSockets Secure).
@socketio.on("get")
def getData(msg):
    try:
        creds = msg["auth"]
        if validateKey(creds["username"], creds["password"]):
            if msg["firstTime"]:
                status = "first"
            else:
                status = "update"
            # Logged in; update data.
            socketio.emit("response", {
                "user": creds["username"],
                "status": status,
                "data": memory
            })
        else:
            socketio.emit("response", createErrorDict(403, "Incorrect credentials."))
    except:
        socketio.emit("response", createErrorDict(401, "Please pass credentials in 'auth' key."))

@socketio.on("update")
def uploadData(msg):
    try:
        creds = msg["auth"]
        if validateKey(creds["username"], creds["password"]):
            # Logged in; update data.
            memory = {**memory, **msg["data"]}
        else:
            socketio.emit("response", createErrorDict(403, "Incorrect credentials."))
    except:
        socketio.emit("response", createErrorDict(401, "Please pass credentials in 'auth' key."))

def createError(code, message):
    return Response(json.dumps(createErrorDict(code, message)), mimetype="application/json", status=code)

def createErrorDict(code, message):
    return {"error": code, "reason": message}

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

def init():
    socketio.run(app, host="0.0.0.0", port=config["port"], debug=config["debug"], use_reloader=False)

# A command-line interface for admin stuffs.
def initConsoleMode():
    print("OCSync Console")
    print("(c) 2021 Jeffrey DiVincent.")
    print("Type \"help\" for a list of commands.")
    while True:
        cmd = input("OCSync: ").split(" ")

        first = cmd[0]

        if first == "help":
            print("Available commands: help, quit, users, report")
        elif first == "quit":
            print("Shutting down...")
            os._exit(os.EX_OK)
        elif first == "users":
            try:
                if cmd[1].lower() == "list":
                    print("Users: ", end="")
                    for user in config["keys"].keys():
                        print(user, end=" ")
                    print()
                elif cmd[1].lower() == "add":
                    try:
                        addKey(cmd[2], cmd[3])
                        print(f"Added user \"{cmd[2]}\" successfully!")
                    except:
                        print("Syntax: users add <username> <password>")
                else:
                    print(f"users {cmd[1].lower()}: invalid subcommand.")
            except:
                print("Syntax: users <list|add>")
        elif first == "report":
            print(memory)


if __name__ == '__main__':
    if config["debug"]:
        threading.Thread(target=init).start()
        initConsoleMode()
    else:
        init()