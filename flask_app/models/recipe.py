from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.name = data['name']
        self.description = data['description']
        self.instruction = data['instruction']
        self.date_cooked = data['date_cooked']
        self.cook_time = data['cook_time']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @staticmethod
    def validate_data(request_form):
        is_valid = True
        if len(request_form['name']) < 1:
            flash("Recipe name must not be blank.")
            is_valid = False
        elif len(request_form['name']) < 3:
            flash("Recipe name must be at least 3 characters.")
            is_valid = False
        if len(request_form['description']) < 1:
            flash("Description must not be blank.")
            is_valid = False
        elif len(request_form['description']) < 3:
            flash("Description must be at least 3 characters")
            is_valid = False
        if len(request_form['instruction']) < 1:
            flash("Instruction must not be blank.")
            is_valid = False
        elif len(request_form['instruction']) < 3:
            flash("Instruction must be at least 3 characters.")
            is_valid = False
        return is_valid

    @classmethod
    def create_recipe(cls,data):
        query = """
        Insert Into recipes (user_id, name, description, instruction, date_cooked, cook_time, created_at, updated_at)
        Values(%(user_id)s,%(name)s,%(description)s,%(instruction)s,%(date_cooked)s, %(cook_time)s, Now(), Now())
        """
        result = connectToMySQL('recipes_db').query_db(query,data)
        return result
    
    @classmethod
    def show_all_recipes(cls):
        query = "Select * From recipes"
        result = connectToMySQL('recipes_db').query_db(query)

        recipes = []
        for recipe in result:
            recipes.append(cls(recipe))
        return recipes
    
    @classmethod
    def update_recipe(cls, data):
        query = """
        Update recipes
        Set user_id = %(user_id)s, name = %(name)s, description = %(description)s, instruction = %(instruction)s, date_cooked = %(date_cooked)s, 
        cook_time = %(cook_time)s, created_at = Now(), updated_at = Now() Where user_id = %(user_id)s and id = %(recipe_id)s;
    """
        result = connectToMySQL('recipes_db').query_db(query,data)
        return result
    
    @classmethod
    def destroy(cls,recipe_id):
        query = f"DELETE FROM recipes WHERE id = {recipe_id}"
        result = connectToMySQL('recipes_db').query_db(query)
        return result


