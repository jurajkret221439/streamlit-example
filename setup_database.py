from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


# Database setup
engine = create_engine('sqlite:///tsfc.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Dish model
class Dish(Base):
    __tablename__ = 'dishes'
    id = Column(Integer, primary_key=True)
    name = Column(String)

# Ingredient model
class Ingredient(Base):
    __tablename__ = 'ingredients'
    id = Column(Integer, primary_key=True)
    name = Column(String) 

# DishIngredient model
class DishIngredient(Base):
    __tablename__ = 'dish_ingredients'
    id = Column(Integer, primary_key=True)
    dish_id = Column(Integer, ForeignKey('dishes.id'))
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'))
    amount = Column(Integer)  # Amount in grams

    dish = relationship("Dish")
    ingredient = relationship("Ingredient")





# Create tables
Base.metadata.create_all(engine)





# Function to add a dish
def add_dish(name):
    session = Session()
    dish = Dish(name=name)
    session.add(dish)
    session.commit()
    return dish

# Function to add an ingredient
def add_ingredient(name):
    session = Session()
    ingredient = Ingredient(name=name)
    session.add(ingredient)
    session.commit()
    return ingredient

# Function to associate a dish with an ingredient
def add_dish_ingredient(dish, ingredient, amount):
    session = Session()
    dish_ingredient = DishIngredient(dish=dish, ingredient=ingredient, amount=amount)
    session.add(dish_ingredient)
    session.commit()


# Add Taco Beef and its ingredients
taco_beef = add_dish("Taco Beef")
birria = add_ingredient("Birria")
avo_smash = add_ingredient("Avo Smash")
onion_coriander = add_ingredient("Onion Coriander")
mojo_rojo = add_ingredient("Mojo Rojo")

add_dish_ingredient(taco_beef, birria, 80)
add_dish_ingredient(taco_beef, avo_smash, 25)
add_dish_ingredient(taco_beef, onion_coriander, 25)
add_dish_ingredient(taco_beef, mojo_rojo, 12)
