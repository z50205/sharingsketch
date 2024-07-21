from flask import request
from flask_socketio import emit
from PSS.extensions import socketio
import threading
from threading import Lock

users={}
message={}
canves={}
typing_timers={}
done_typing_interval =60*10
typing_timers_lock = Lock()

@socketio.on("connect")
def handle_connect():
    print("Client Connected!")
    start_typing_timer(request.sid)
    print(f'typing_timer {request.sid} start')
    emit ("join",{"SelfSid":request.sid})

@socketio.on("user_join")
def joinUser(username):
    print(f"User {username} joined!")
    users[request.sid]=username
    memberlist=list(users.values())
    canvassids=list(users.keys())
    emit ("memberslistUpdate",{"memberslist":memberlist},broadcast=True)
    emit ("createNewCanvas",{"canvassids":canvassids},broadcast=True)

@socketio.on("new_message")
def newMessage(message):
    heartbeat(request.sid)
    emit("chat",{"message":message,"username":users[request.sid]},broadcast=True)

@socketio.on("new_img")
def newImg(img):
    heartbeat(request.sid)
    # print("updateImg")
    emit("updateImg",{"updateimg":img,"UpdateSid":request.sid},broadcast=True, include_self=False)

@socketio.on("init_new_img")
def initNewImg(img):
    # print("updateImg")
    emit("updateImg",{"updateimg":img,"UpdateSid":request.sid},broadcast=True, include_self=False)


@socketio.on("bye")
def bye():
    delete_user(request.sid)

def start_typing_timer(sid):
    typing_timers[sid] = threading.Timer(done_typing_interval, delete_user, args=[sid])
    typing_timers[sid].start()

def heartbeat(sid):
    print(f"typing_timers {typing_timers}")
    typing_timers[sid].cancel()
    print(f'typing_timer {sid} stop')
        # print(f'previous typing_timer {sid} stop')
    start_typing_timer(sid)
    print(f'typing_timer {sid} restart')
    # print(f'typing_timer {sid} heartbeat')
    # print(typing_timers)

def delete_user(sid):
    typing_timers[sid].cancel()
    with typing_timers_lock:
        print(users)
        del users[sid]
        print(f'Deleted user with sid={sid}')
        memberlist=list(users.values())
        socketio.emit ("memberslistUpdate",{"memberslist":memberlist})
        socketio.emit ("leaveRemoveCanvas",{"LeaveSid":sid})

@socketio.on('update_old_content')
def updateOldContent():
    memberlist=list(users.values())
    emit("initUpdateImg",{"UpdateSid":request.sid},broadcast=True, include_self=False)
    emit ("memberslistUpdate",{"memberslist":memberlist},broadcast=True)
    # emit("initChat",{"message":message,"username":users[request.sid]},broadcast=True)