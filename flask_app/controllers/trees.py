from flask_app import app
from flask_bcrypt import Bcrypt
from flask import render_template,redirect,request,session,flash
from flask_app.models.tree import Tree
from flask_app.models.user import User


@app.route('/new/tree')
def display_create_page():
    if 'user_id' in session:
        user_id = session['user_id']
        data = {
            "user_id" : user_id
        }
        current_user = User.get_user_by_id(data)
        all_trees = Tree.get_all_trees()
        return render_template("new_tree.html", current_user = current_user, all_trees = all_trees)
    else:
        return redirect('/')

@app.route('/add_new_tree', methods=['POST'])
def add_new_tree():
    if not Tree.validate_tree(request.form):
        return redirect('/new/tree')
    if 'user_id' in session:
        user_id = session['user_id']
        data = {
            **request.form,
            "user_id" : user_id
        }
        tree_data = Tree.save(data)
    else:
        return redirect('/')
    return redirect('/dashboard')

@app.route('/show/<int:tree_id>')
def display_tree(tree_id):
    if 'user_id' in session:
        user_id = session['user_id']
        user_data = {
            "user_id" : user_id
        }
        current_user = User.get_user_by_id(user_data)
        tree_data = {
            "tree_id" : tree_id
        }
        tree_info = Tree.get_tree_by_id(tree_data)
        all_visitors = User.get_all_visitors_by_tree_id(tree_data)
        return render_template("tree_show.html", tree_info = tree_info, current_user = current_user, all_visitors = all_visitors)
    else:
        return redirect('/')

@app.route('/edit/<int:tree_id>')
def display_update_page(tree_id):
    if 'user_id' in session:
        user_id = session['user_id']
        data = {
            "user_id" : user_id,
            "tree_id" : tree_id
        }
        session['tree_id'] = tree_id
        current_user = User.get_user_by_id(data)
        current_tree = Tree.get_tree_by_id(data)
        return render_template("update_tree.html", current_tree = current_tree, current_user = current_user)
    else:
        return redirect('/')


@app.route('/update_tree', methods = ['POST'])
def edit_tree():
    if 'user_id' and 'tree_id' in session:
        user_id = session['user_id']
        tree_id = session['tree_id']
        data = {
            **request.form,
            "user_id" : user_id,
            "tree_id" : tree_id
        }
        if not Tree.validate_tree(request.form):
            return redirect(f'/edit/{tree_id}')
        Tree.update_tree(data)
    else:
        return redirect('/')
    return redirect('/dashboard')

@app.route('/delete/<int:tree_id>')
def delete_tree(tree_id):
    data = {
        "tree_id" : tree_id
    }
    Tree.delete_tree(data)
    return redirect('/user/account')
    