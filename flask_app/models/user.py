from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.recipe import Recipe
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipe = None

    @staticmethod
    def validate_data(request_form):
        is_valid = True
        if len(request_form['fname']) < 2:
            flash("First name must be at least 2 characters.")
            is_valid = False
        if len(request_form['lname']) < 2:
            flash("Last name must be at least 2 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(request_form['email']):
            flash("Invalid email address.")
            is_valid = False
        if len(request_form['password']) < 5:
            flash("Password must be at least 5 characters.")
        return is_valid

    @classmethod
    def add_user(cls, data):
        query = "Insert Into users(first_name, last_name, email, password, created_at, updated_at) Values(%(fname)s, %(lname)s, %(email)s ,%(password)s, Now(), Now())"
        result = connectToMySQL('recipes_db').query_db(query,data)
        return result
    
    @classmethod
    def get_user_by_id(cls, data):
        query = "Select * from users where id = %(user_id)s"
        result = connectToMySQL('recipes_db').query_db(query,data)
        return cls(result[0])
    

    # grab user email to verify email exists in db
    @classmethod
    def check_email(cls, data):
        query = "Select * from users where email = %(email)s "
        result = connectToMySQL('recipes_db').query_db(query,data)
        print(result)

        if len(result) < 1:
            return False
        return(cls(result[0]))
    
    #grab all users with associated recipes:
    @classmethod
    def users_recipes(cls):
        query = "Select * From recipes join users on users.id = recipes.user_id"
        result = connectToMySQL('recipes_db').query_db(query)

        users = []
        if result:
            for row in result:
                user = cls(row)
                user.recipe = Recipe(row)
                users.append(user)
        return users
    

    @classmethod
    def recipes_per_user(cls,recipe_id):
        query = f"SELECT * FROM recipes join users on users.id = recipes.user_id WHERE recipes.id = {recipe_id};"
        result = connectToMySQL('recipes_db').query_db(query)

        recipes = []

        for row in result:
            user = cls(row)
            user.recipe = Recipe(row)
            recipes.append(user)
        return recipes
    

    # @classmethod
    # def recipe_user_by_id(cls,recipe_id):
    #     query = f"Select * From recipes where id = {recipe_id}"
    #     result = connectToMySQL('recipes_db').query_db(query)
    #     print(result)
    #     recipe = []

    #     for row in result:
    #         recipe.append(cls(row))
    #     print("RECIPE: ", recipe)
    #     return recipe
    

