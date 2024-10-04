from flask import render_template,redirect,url_for,session,jsonify,request,flash
from PSS.extensions import Loginform,Registerform
from flask_login import login_user,logout_user,login_required,current_user
from PSS import db
from PSS.models.user import User
from PSS.events import users

def index():
    form=Loginform()

    # if request.method == 'GET':
    #     session['next'] = request.referrer
    # # print("request.referrer and request.host in request.referrer",request.referrer and request.host in request.referrer)
    # # print("request.referrer",request.referrer)
    # # print("request.host",request.host)
    # print("session['next']",session['next'])
    if form.validate_on_submit():
        u=User.query.filter_by(username=form.username.data).first()
        if u is None or not u.check_password(form.password.data):
            flash("Invalid username or password")
            print("invalid account")
            return render_template('index.html', form=form)
        session.clear()
        login_user(u,remember=form.remember_me.data)
        session['username']=form.username.data
        return redirect(url_for('room_choose'))
        # next_url = session.get('next', url_for('room_choose'))
        # return redirect(next_url)
    return render_template('index.html',form=form)

def register():
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    print("register")
    form=Registerform()
    if form.validate_on_submit():
        print("submit")
        existing_user = User.query.filter_by(username=form.username.data).first()
        print("query")
        if existing_user:
            flash("Username already taken. Please choose a different one.")
            return render_template('register.html', title="Register", form=form)  # 渲染頁面而不是重定向
        user=User(username=form.username.data,email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('register.html',title="Register",form=form)

@login_required
def room():

    username = session.get('username')
    roomname = session.get('roomname')
    if not username or not roomname or not current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('room.html', username=username, roomname=roomname)

@login_required
def room_choose():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    fetchSrc=request.cookies.get('src')
    roominfo=get_roomInfo()
    username = session.get('username')
    if request.method == 'POST':
        roomname = request.form.get('roomname')
        print('users',users)
        print('roominfo',roominfo)
        session['roomname']=roomname
        if not roomname:
            return "Roomname is required!", 400
        return redirect(url_for('room'))
    return render_template('room_choose.html',src=fetchSrc,roominfo=roominfo, username=username)

@login_required
def gallery_export():
    username = session.get('username')
    return render_template('gallery_export.html',username=username)


# def logout():
#     logout_user()
#     host = request.host
#     referer = request.referrer
#     if referer and host in referer:
#         return redirect(referer)
#     else:
#         return redirect(url_for('index')) 
def logout():
    logout_user()
    return redirect(request.referrer)

def membership():
    username = session.get('username')
    if current_user.is_authenticated:
        return jsonify({
            'status': 'success',
            'user': username
        }), 200
    else:
        return jsonify({
            'status': 'error',
            'message': 'Not authenticated'
        }), 401
    

def get_roomInfo():
    room_dict={}
    for key,values in users.items():
        if values[1] not in room_dict:
            room_dict[values[1]] = []  # 初始化為空列表
        room_dict[values[1]].append(values[0])
    return room_dict


    