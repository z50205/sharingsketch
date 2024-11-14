from flask import request,url_for
from flask_socketio import emit,join_room
from PSS.extensions import socketio
import threading
from threading import Lock
from PSS.extensions import Loginform
import logging
import redis
import json
# dict users->sid(keys)----[username,roomname]
typing_timers={}
done_typing_interval =60*15
typing_timers_lock = Lock()
logging.basicConfig(level=logging.INFO)  # 或者其他日志级别
logger = logging.getLogger(__name__)

redis_client = redis.StrictRedis(host='redis', port=6379, db=0)

@socketio.on("user_join")
def joinUser(data):
    username=data['username']
    room = data['room']
    users_data = redis_client.get('users')
    if users_data is None:
        users = {} 
    else:
        users = json.loads(users_data)
    join_room(room)
    users[request.sid]=[username,room]
    redis_client.set('users', json.dumps(users))
    start_typing_timer(request.sid,room)
    room_memberlist=[]
    room_canvassids=[]
    users=json.loads(redis_client.get('users'))
    for key, value in users.items():
        # print(f'Key: {key}, Value1: {value[0]}, Value2: {value[1]}')
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
    users=json.loads(redis_client.get('users'))
    print("users message:"+str(users))
    emit("chat",{"message":message,"username":users[request.sid][0]},to=room)

@socketio.on("new_img")
def newImg(data):
    img=data['can_proj_data']
    room=data['room']
    start_at=data['start_at']
    heartbeat(request.sid,room)
    # emit("updateImg",{"updateimg":img,"UpdateSid":request.sid},to=room, include_self=False)
    emit("updateImg",{"updateimg":img,"UpdateSid":request.sid,"start_at": start_at},to=room, include_self=False)

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
    del typing_timers[request.sid]
    with typing_timers_lock:
        users=json.loads(redis_client.get('users'))
        del users[request.sid]
        redis_client.set('users', json.dumps(users))
        print(f'Deleted user with sid={request.sid}')
    room_memberlist=[]
    for key, value in users.items():
        if value[1] == room:
            room_memberlist.append(value[0])
    socketio.emit ("memberslistUpdate",{"memberslist":room_memberlist},to=room)
    socketio.emit ("leaveRemoveCanvas",{"LeaveSid":request.sid},to=room)

def start_typing_timer(sid,room):
    typing_timers[sid] = threading.Timer(done_typing_interval, delete_user, args=[sid,room])
    typing_timers[sid].start()

def heartbeat(sid,room):
    typing_timers[sid].cancel()
    del typing_timers[sid]
        # print(f'previous typing_timer {sid} stop')
    start_typing_timer(sid,room)
    # print(f'typing_timer {sid} heartbeat')
    # print(typing_timers)

def delete_user(sid,room):
    typing_timers[sid].cancel()
    del typing_timers[sid]
    with typing_timers_lock:
        users=json.loads(redis_client.get('users'))
        del users[sid]
        redis_client.set('users', json.dumps(users))
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
    users=json.loads(redis_client.get('users'))
    room_memberlist=[]
    for key, value in users.items():
        if value[1] == room:
            room_memberlist.append(value[0])
    emit("initUpdateImg",{"UpdateSid":request.sid},to=room, include_self=False)
    emit ("memberslistUpdate",{"memberslist":room_memberlist},to=room)
    # emit("initChat",{"message":message,"username":users[request.sid]},broadcast=True)





