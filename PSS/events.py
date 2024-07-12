from flask import request
from flask_socketio import emit
from PSS.extensions import socketio
import threading


users={}
message={}
canves={}
done_typing_interval =20

@socketio.on("connect")
def handle_connect():
    print("Client Connected!")
    emit ("join",{"SelfSid":request.sid})

@socketio.on("user_join")
def joinUser(username):
    print(f"User {username} joined!")
    users[request.sid]=username
    memberlist=list(users.values())
    canvassids=list(users.keys())
    print(canvassids)
    emit ("memberslistUpdate",{"memberslist":memberlist},broadcast=True)
    emit ("createNewCanvas",{"canvassids":canvassids},broadcast=True)

@socketio.on("new_message")
def newMessage(message):
    print(f"New message:{message}")
    emit("chat",{"message":message,"username":users[request.sid]},broadcast=True)

@socketio.on("new_img")
def newImg(img):
    print(f"New ctx update!")
    emit("updateImg",{"updateimg":img,"UpdateSid":request.sid},broadcast=True, include_self=False)

typing_timer = None
@socketio.on("bye")
def bye(byepivot):
    global typing_timer
    if (byepivot):
        on_timeout(request.sid)
    else:
        typing_timer.cancel()
    
def on_timeout(id):
    global typing_timer
    typing_timer = threading.Timer(done_typing_interval, delete_user, args=(id,))
    typing_timer.start()

def delete_user(id):
    username=users[id] 
    del users[id]
    print(f'Deleted user with sid={id}')
    print(f"User {username} leaved!")
    memberlist=list(users.values())
    print(f"User sid {id} leaved!")
    socketio.emit ("memberslistUpdate",{"memberslist":memberlist})
    socketio.emit ("leaveRemoveCanvas",{"LeaveSid":id})

@socketio.on('update_old_content')
def updateOldContent(self_sid):
    memberlist=list(users.values())
    emit("initUpdateImg",{"UpdateSid":request.sid},broadcast=True, include_self=False)
    # emit("initChat",{"message":message,"username":users[request.sid]},broadcast=True)