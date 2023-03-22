from flask_app import app
from flask_bcrypt import Bcrypt
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.tree import Tree

bcrypt = Bcrypt(app)

@app.route('/')
def route_to():
    return redirect('/login_and_reg')

@app.route('/login_and_reg')
def display_login_and_reg():
    return render_template('login_and_reg.html')

@app.route('/register', methods=['POST'])
def register_user():
    if not User.validate_user_reg(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        "password" : pw_hash
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/dashboard')


@app.route('/login', methods=['POST'])
def login_user():
    data = {
        "email" : request.form["email"]
    }
    user_in_db = User.get_user_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password.","invalid_info")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password.","invalid_info")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')

@app.route('/dashboard')
def display_dashboard_page():
    if 'user_id' in session:
        user_id = session['user_id']
        data = {
            "user_id" : user_id
        }
        current_user = User.get_user_by_id(data)
        all_trees = Tree.get_all_trees()
        return render_template('dashboard.html', current_user = current_user, all_trees = all_trees)
    else:
        return redirect('/')

@app.route('/logout')
def destroy_session():
    session.clear()
    return redirect('/')

@app.route('/user/account')
def display_user_info():
    if 'user_id' in session:
        user_id = session['user_id']
        user_data = {
            "user_id" : user_id
        }
        current_user = User.get_user_by_id(user_data)
        all_trees = Tree.get_all_trees_by_user_id(user_data)
        return render_template("user_account.html", current_user = current_user, all_trees = all_trees)
    else:
        return redirect('/')
    
@app.route('/add_visit_to_tree/<int:tree_id>/<int:user_id>')
def add_visit_to_tree(tree_id, user_id):
    if 'user_id' in session:
        data = {
            "tree_id" : tree_id,
            "user_id" : user_id
        }
        User.add_to_visit_count(data)
        Tree.update_tree_visit_count(data)
        return redirect(f'/show/{tree_id}')
    else:
        return redirect('/')


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")
