from flask import render_template,redirect,request,session,flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('main.html')


@app.route('/create', methods = ['POST'])
def create_user():

    data = {"email": request.form['email']}
    user_with_email = User.check_email(data)
    if user_with_email:
        flash("Email already in use.")
        return redirect('/')
    
    if not User.validate_data(request.form):
        return redirect('/')

    if request.form['password'] != request.form['confirm']:
        flash("Passwords did not match.")
        return redirect('/')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "fname" : request.form['fname'],
        "lname" : request.form['lname'],
        "email" : request.form['email'],
        "password" : pw_hash
    }

    user_id = User.add_user(data)
    session['user_id'] = user_id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard_page():
    if 'user_id' not in session:
        flash("Login to load page.")
        return redirect('/')

    user = User.get_user_by_id({"user_id" : session['user_id']})
    recipes = Recipe.show_all_recipes()
    users_recipes = User.users_recipes()
    
    return render_template('dashboard.html', user=user, users_recipes=users_recipes)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/login', methods = ['POST'])
def login_user():
    data = {"email": request.form['email']}
    user_with_email = User.check_email(data)

    if not user_with_email:
        flash("Incorrect email/password")
        return redirect('/')
    if not bcrypt.check_password_hash(user_with_email.password, request.form['password']):
        flash("Incorrect email/password")
        return redirect('/')

    session['user_id'] = user_with_email.id
    return redirect('/dashboard')
