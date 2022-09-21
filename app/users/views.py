from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from app.users.forms import RegisterForm, LoginForm, UserForm
from app.users.models import User
from app.users.decorators import requires_login
from app.users.tables import UsersTable

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
    if g.user:
        return redirect(url_for('users.home'))
    form = LoginForm(request.form)
    # checking that data is valid (except password)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        # validate password with werzeug.security
        if user and check_password_hash(user.password, form.password.data):
            # session can't be modified as it signed, safe place to store user id
            session['user_id'] = user.id
            flash('Welcome %s' % user.username)
            return redirect(url_for('users.home'))
        flash('Wrong email or password', 'error-message')
    return render_template("users/login.html", form=form)


@users.route('/register/', methods=['GET', 'POST'])
def register():
    """
    Registartion Form
    """
    if g.user:
        return redirect(url_for('users.home'))
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

# TODO fix save changes
def save_changes(user, form, new=False):
    """
    Save the changes to the database
    """
    user = User()
    user.username = form.username.data
    user.email = form.email.data
    user.role = form.role.data
    user.status = form.status.data
    if new:
        # Add the new user to the database
        db.session.add(user)
    # commit the data to the database
    db.session.commit()


@users.route('/<user_id>/', methods=['POST', 'GET'])
def edit(user_id):
    qry = db.session.query(User).filter(User.id == user_id)
    user = qry.first()
    if user:
        form = UserForm(formdata=request.form, obj=user)
        print('before1 save')
        if request.method == 'POST' and form.validate():
            print('before2 save')
            save_changes(user, form)
            print('after save')
            flash('User updated successfully!')
            return redirect(url_for('users.edit', user_id=user_id))
        return render_template("users/edit_user.html", form=form)
    return render_template('404.html'), 404

#
# @users.route('/', methods=['GET', 'POST'])
# def index():
#     search = UserSearchForm(request.form)
#     if request.method == 'POST':
#         return all_users(search)
#     return render_template('users/users.html', form=search)


@users.route('/')
def all_users():
    qry = db.session.query(User)
    users_result = qry.all()
    if not users_result:
        flash('No users found!')
        return redirect('/users/')
    table = UsersTable(users_result)
    table.border = True
    return render_template('users/users.html', table=table)


@users.route('/delete/<user_id>', methods=['GET', 'POST'])
def delete(user_id):
    """
    Delete the item in the database that matches the specified
    id in the URL
    """
    qry = db.session.query(User).filter(User.id == user_id)
    user = qry.first()
    if user:
        form = RegisterForm(formdata=request.form, obj=user)
        if request.method == 'POST' and form.validate():
            # delete the item from the database
            db.session.delete(user)
            db.session.commit()
            flash('User deleted successfully!')
            return redirect('/')
        return render_template('users/delete_user.html', form=form)
    return 'Error deleting #{id}'.format(id=user_id)


@users.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("home"))
