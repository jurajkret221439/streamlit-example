
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from setup_database import Dish, Ingredient, DishIngredient

# Connect to the database
engine = create_engine('sqlite:///tsfc.db')
Session = sessionmaker(bind=engine)

def get_dish_with_ingredients(dish_name):
    session = Session()
    dish = session.query(Dish).filter_by(name=dish_name).first()
    if dish is None:
        return None, []  # Return None and an empty list if dish is not found
    dish_ingredients = session.query(DishIngredient).filter_by(dish_id=dish.id).all()
    ingredients = [{"name": di.ingredient.name, "amount": di.amount} for di in dish_ingredients]
    return dish, ingredients

# Test the function with different dishes
test_dishes = ["Taco Beef", "Taco Shrimp", "Frietje Rendang", "Popcorn Shrimp"]
for dish_name in test_dishes:
    dish, ingredients = get_dish_with_ingredients(dish_name)
    if dish and ingredients:
        print(f"Dish: {dish.name}")
        for ingredient in ingredients:
            print(f"  Ingredient: {ingredient['name']}, Amount: {ingredient['amount']}")
    else:
        print(f"No ingredients found for dish: {dish_name}")
