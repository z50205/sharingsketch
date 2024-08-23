from flask import request,url_for
from flask_socketio import emit,join_room,rooms
from PSS.extensions import socketio
import threading
from threading import Lock
from PSS.extensions import Loginform

users={}
typing_timers={}
done_typing_interval =60*15
typing_timers_lock = Lock()


# @socketio.on("connect")
# def handle_connect():
#     start_typing_timer(request.sid)
#     emit ("join",{"SelfSid":request.sid})

@socketio.on("user_join")
def joinUser(data):
    username=data['username']
    room = data['room']
    join_room(room)
    # dict users->sid(keys)----[username,roomname]
    users[request.sid]=[username,room]
    print(f"User {username} joined room {room}!")
    start_typing_timer(request.sid,room)
    room_memberlist=[]
    room_canvassids=[]
    for key, value in users.items():
        if value[1] == room:
            room_memberlist.append(value[0])
            room_canvassids.append(key)
    emit ("join",{"SelfSid":request.sid})
    emit ("memberslistUpdate",{"memberslist":room_memberlist},to=room)
    emit ("createNewCanvas",{"canvassids":room_canvassids},to=room)

@socketio.on("new_message")
def newMessage(data):
    message=data['message']
    room=data['room']
    heartbeat(request.sid,room)
    emit("chat",{"message":message,"username":users[request.sid][0]},to=room)

@socketio.on("new_img")
def newImg(data):
    img=data['can_proj_data']
    room=data['room']
    heartbeat(request.sid,room)
    emit("updateImg",{"updateimg":img,"UpdateSid":request.sid},to=room, include_self=False)

@socketio.on("init_new_img")
def initNewImg(data):
    img=data['can_proj_data']
    room=data['room']
    emit("updateImg",{"updateimg":img,"UpdateSid":request.sid},to=room, include_self=False)


@socketio.on("bye")
def bye(room):
    delete_user(request.sid,room)

@socketio.on("leave_room")
def leave_room(room):
    typing_timers[request.sid].cancel()
    with typing_timers_lock:
        del users[request.sid]
        print(f'Deleted user with sid={request.sid}')
    room_memberlist=[]
    for key, value in users.items():
        if value[1] == room:
            room_memberlist.append(value[0])
    socketio.emit ("memberslistUpdate",{"memberslist":room_memberlist},to=room)
    socketio.emit ("leaveRemoveCanvas",{"LeaveSid":request.sid},to=room)
    emit("redirect",{"url": url_for('index')} )

def start_typing_timer(sid,room):
    typing_timers[sid] = threading.Timer(done_typing_interval, delete_user, args=[sid,room])
    typing_timers[sid].start()

def heartbeat(sid,room):
    typing_timers[sid].cancel()
        # print(f'previous typing_timer {sid} stop')
    start_typing_timer(sid,room)
    # print(f'typing_timer {sid} heartbeat')
    print(typing_timers)

def delete_user(sid,room):
    typing_timers[sid].cancel()
    with typing_timers_lock:
        del users[sid]
        print(f'Deleted user with sid={sid}')
    room_memberlist=[]
    for key, value in users.items():
        if value[1] == room:
            room_memberlist.append(value[0])
    socketio.emit ("memberslistUpdate",{"memberslist":room_memberlist},to=room)
    socketio.emit ("leaveRemoveCanvas",{"LeaveSid":sid},to=room)
    socketio.emit ("disconnect",to=sid)


@socketio.on('update_old_content')
def updateOldContent(room):
    memberlist=list(users.values())
    room_memberlist=[]
    for key, value in users.items():
        if value[1] == room:
            room_memberlist.append(value[0])
    emit("initUpdateImg",{"UpdateSid":request.sid},to=room, include_self=False)
    emit ("memberslistUpdate",{"memberslist":room_memberlist},to=room)
    # emit("initChat",{"message":message,"username":users[request.sid]},broadcast=True)