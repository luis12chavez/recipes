from flask import render_template,redirect,request,session,flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/recipes/new")
def recipe_index():
    if 'user_id' not in session:
        flash('Login to add new recipe.')
        return redirect('/')

    return render_template('recipe_create.html')

@app.route("/create/recipe", methods=['POST'])
def add_recipe():
    print(session['user_id'])

    if not Recipe.validate_data(request.form):
        return redirect('/recipes/new')

    data = {
        "user_id" : session['user_id'],
        "name" : request.form['name'],
        "description" : request.form['description'],
        "instruction" : request.form['instruction'],
        "date_cooked" : request.form['date_cooked'],
        "cook_time" : request.form['cook_time'],
    }
    Recipe.create_recipe(data)
    return redirect('/dashboard')


@app.route('/recipes/<int:recipe_id>')
def view_recipe(recipe_id):
    print(recipe_id)
    user_recipes = User.recipes_per_user(recipe_id)
    user = User.get_user_by_id({"user_id" : session['user_id']})
    # recipe = User.recipe_user_by_id(recipe_id)

    return render_template("recipe_detail.html", user_recipes=user_recipes, user=user)

@app.route('/recipes/edit/<int:recipe_id>')
def edit_page(recipe_id):
    user_recipes = User.recipes_per_user(recipe_id)
    return render_template("edit.html", user_recipes=user_recipes)

@app.route('/update', methods = ['POST'])
def edit_recipe():
    if 'user_id' not in session:
        flash('Login to edit recipe.')
        return redirect('/')

    data = {
        "user_id" : session['user_id'],
        "name" : request.form['name'],
        "description" : request.form['description'],
        "instruction" : request.form['instruction'],
        "date_cooked" : request.form['date_cooked'],
        "cook_time" : request.form['cook_time'],
        "recipe_id" :request.form['recipe_id']
    }
    Recipe.update_recipe(data)
    return redirect('/dashboard')

@app.route('/delete/<int:recipe_id>')
def delete(recipe_id):
    id = recipe_id
    print("Recipe_Id:",id)
    Recipe.destroy(recipe_id)

    return redirect('/dashboard')