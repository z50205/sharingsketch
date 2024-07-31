from flask import render_template,redirect,url_for,session,flash
from PSS.extensions import Loginform,Registerform
from flask_login import login_user,logout_user,login_required,current_user
from PSS import db
from PSS.models.user import User

def index():
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    form=Loginform(meta={'csrf': False})
    if form.validate_on_submit():
        u=User.query.filter_by(username=form.username.data).first()
        if u is None or not u.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for('index'))
        session.clear()
        login_user(u,remember=form.remember_me.data)
        session['roomname']=form.roomname.data
        session['username']=form.username.data
        return redirect(url_for('room'))
    return render_template('index.html',form=form)

def register():
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    form=Registerform(meta={'csrf': False})
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash("Username already taken. Please choose a different one.")
            return redirect(url_for('register'))
        user=User(username=form.username.data,email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('register.html',title="Register",form=form)

def intro():
    return render_template('intro.html')

@login_required
def room():
    username = session.get('username')
    roomname = session.get('roomname')
    if not username or not roomname:
        return redirect(url_for('index'))
    return render_template('room.html', username=username, roomname=roomname)
