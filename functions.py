from setup_database_azure import SessionLocal, Dish, Ingredient, DishIngredient,  Waste
from datetime import datetime
import logging

# Function to get dish and its ingredients
def get_dish_with_ingredients(dish_name):
    with SessionLocal() as session:
        dish = session.query(Dish).filter_by(name=dish_name).first()
        if dish is None:
            return None, []  # Return None and an empty list if the dish is not found

        dish_ingredients = session.query(DishIngredient, Ingredient).join(Ingredient).filter(DishIngredient.dish_id == dish.id).all()
        ingredients = [{"name": ingredient.name, "amount": dish_ingredient.amount, "amount_type": ingredient.amount_type, "storage_type": ingredient.storage_type} for dish_ingredient, ingredient in dish_ingredients]
        return dish, ingredients

# Function to fetch dishes
def get_dishes():
    with SessionLocal() as session:
        dishes = session.query(Dish).all()
        return dishes

# Function to fetch ingredients based on selected dish
def get_ingredients_for_dish(dish_id):
    with SessionLocal() as session:
        dish_ingredients = session.query(DishIngredient).filter(DishIngredient.dish_id == dish_id).all()
        ingredients = [session.query(Ingredient).get(di.ingredient_id) for di in dish_ingredients]
        # No need to close the session explicitly when using 'with'
        return ingredients

# Function to add waste data to the database
def add_waste(dish_id, ingredient_id, amount, date, name):
    with SessionLocal() as session:
        try:
            dish = session.query(Dish).get(dish_id)
            ingredient = session.query(Ingredient).get(ingredient_id)
            if ingredient is None:
                raise ValueError(f"No ingredient found with ID {ingredient_id}")
            current_time = datetime.now().time()
            waste_type = ingredient.waste_type

            waste_data = Waste(dish_id=dish_id, dish_name=dish.name, ingredient_id=ingredient_id, ingredient_name=ingredient.name, amount=amount, waste_type=waste_type, date=date, entry_time=current_time, name=name)
            session.add(waste_data)
            session.commit()
            return "Waste data submitted successfully."
        except Exception as e:
            logging.error(f"Error: {e}")
            session.rollback()  # Rollback the changes on error
            return f"Error adding waste data: {e}"

# Function to choose all ingredients and add zero waste to database for each ingredient
def add_base_waste_entries_for_all_dishes(name):
    dishes = get_dishes()
    date_now = datetime.now().date()  # Get today's date
    success_count = 0
    error_count = 0
    
    for dish in dishes:
        ingredients = get_ingredients_for_dish(dish.id)
        for ingredient in ingredients:
            # Use the base waste amount if defined, otherwise default to zero
            base_waste_amount = base_waste_amounts.get(ingredient.name, 0)
            result = add_waste(dish.id, ingredient.id, base_waste_amount, date_now, name)
            if "successfully" in result:
                success_count += 1
            else:
                error_count += 1
    
    return success_count, error_count  

def calculate_average_waste(dish_id, ingredient_id):
    with SessionLocal() as session:
        # Query to find all waste entries for the specified dish and ingredient
        waste_data = session.query(Waste).filter_by(dish_id=dish_id, ingredient_id=ingredient_id).all()
        
        # Calculate the average if waste_data is not empty
        if waste_data:
            total_waste = sum(entry.amount for entry in waste_data)
            average_waste = total_waste / len(waste_data)
            return average_waste
        else:
            return None  # Return None or 0 if there are no waste entries


# Example dictionary for base waste amounts
base_waste_amounts = {
    'Birria': 100.0,
     # 'IngredientName': base_amount,
}