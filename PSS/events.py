from flask import request
from flask_socketio import emit
from PSS.extensions import socketio

users={}

@socketio.on("connect")
def handle_connect():
    print("Client Connected!")
    emit ("setSelfSid",{"SelfSid":request.sid})

@socketio.on("user_join")
def joinUser(username):
    print(f"User {username} joined!")
    users[username]=request.sid
    memberlist=list(users.keys())
    canvassids=list(users.values())
    print(canvassids)
    emit ("memberslistUpdate",{"memberslist":memberlist},broadcast=True)
    emit ("createNewCanvas",{"canvassids":canvassids},broadcast=True)

@socketio.on("new_message")
def newMessage(message):
    print(f"New message:{message}")
    username=None
    for user in users:
        if users[user]==request.sid:
            username=user
    emit("chat",{"message":message,"username":username},broadcast=True)

@socketio.on("new_img")
def newImg(img):
    print(f"New ctx update!")
    username=None
    for user in users:
        if users[user]==request.sid:
            username=user
    emit("updateImg",{"updateimg":img,"UpdateSid":request.sid},broadcast=True, include_self=False)

@socketio.on("bye")
def bye():
    for user in users:
        if users[user]==request.sid:
            username=user
    del users[username] 
    print(f"User {username} leaved!")
    memberlist=list(users.keys())
    print(f"User sid {request.sid} leaved!")
    emit ("memberslistUpdate",{"memberslist":memberlist},broadcast=True)
    emit ("leaveRemoveCanvas",{"LeaveSid":request.sid},broadcast=True)

