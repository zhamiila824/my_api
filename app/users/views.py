from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from app.users.forms import RegisterForm, LoginForm, UserEditForm
from app.users.models import User
from app.users.decorators import requires_login

users = Blueprint('users', __name__, url_prefix='/users')


@users.route('/me/')
@requires_login
def home():
    return render_template("users/profile.html", user=g.user)


@users.route('/login/', methods=['GET', 'POST'])
def login():
    """
    Login form
    """
    form = LoginForm(request.form)
    # checking that data is valid (except password)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        # validate password with werzeug.security
        if user and check_password_hash(user.password, form.password.data):
            # session can't be modified as it signed, safe place to store user id
            session['user_id'] = user.id
            flash('Welcome %s' % user.name)
            return redirect(url_for('users.home'))
        flash('Wrong email or password', 'error-message')
    return render_template("users/login.html", form=form)


@users.route('/register/', methods=['GET', 'POST'])
def register():
    """
    Registartion Form
    """
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        # create user instance, but not store in database yet
        user = User(username=form.username.data, email=form.email.data,
                    password=generate_password_hash(form.password.data))
        # insert record in database and commit
        db.session.add(user)
        db.session.commit()

        # log user in, and store id in session
        session['user_id'] = user.id
        flash('Thanks for registering')
        # redirect user to the 'home' method of user module
        return redirect(url_for('users.home'))
    return render_template("users/register.html", form=form)

# TODO
@users.route('edit/<user_id>', methods=['PUT', 'GET'])
def edit(user_id):
    form = UserEditForm(request.form)
    exists = db.session.query(db.exists().where(User.id == user_id)).scalar()
    user = db.session.query(User).filter(User.id == user_id)
    if exists:
        print('tut')
        if request.method == 'POST' and form.validate():
            print(form.username.data)
            if form.username.data:
                db.session.query(User).filter(User.id == user_id).update({'username': form.username.data})
                db.session.commit()

            return redirect(url_for('users.edit(user_id)'))
        else:
            print(form.validate())
        return render_template("users/edit_user.html", user=user, form=form)
    return render_template('404.html'), 404

