from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


# Database setup
engine = create_engine(
    'sqlite:///tsfc.db', 
    connect_args={'check_same_thread': False}
)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Dish model
class Dish(Base):
    __tablename__ = 'dishes'
    id = Column(Integer, primary_key=True)
    name = Column(String,unique=True)

# Ingredient model
class Ingredient(Base):
    __tablename__ = 'ingredients'
    id = Column(Integer, primary_key=True)
    name = Column(String,unique=True) 

# DishIngredient model
class DishIngredient(Base):
    __tablename__ = 'dish_ingredients'
    id = Column(Integer, primary_key=True)
    dish_id = Column(Integer, ForeignKey('dishes.id'))
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'))
    amount = Column(Integer)  # Amount in grams

    dish = relationship("Dish")
    ingredient = relationship("Ingredient")

def drop_all_tables():
    Base.metadata.drop_all(engine)
    print("DROPPED, RESETTED VALUES")
drop_all_tables()

# Create tables
def create_tables():
    Base.metadata.create_all(engine)
    print("CREATED TABLES")
create_tables()

# Function to add a dish
def add_dish(name):
    try:
        session = Session()
        dish = Dish(name=name)
        session.add(dish)
        session.commit()
        print(f"Dish added: {dish.name}")
        return dish
    except Exception as e:
        print(f"Error adding dish {name}: {e}")
    finally:
        session.close()

# Function to add an ingredient
def add_ingredient(name):
    try:
        session = Session()
        ingredient = Ingredient(name=name)
        session.add(ingredient)
        session.commit()
        print(f"Ingredient added: {ingredient.name}")
        return ingredient
    except Exception as e:
        print(f"Error adding ingredient {name}: {e}")
    finally:
        session.close()

# Function to associate a dish with an ingredient
def add_dish_ingredient(dish, ingredient, amount):
    try:
        session = Session()
        dish_ingredient = DishIngredient(dish_id=dish.id, ingredient_id=ingredient.id, amount=amount)
        session.add(dish_ingredient)
        session.commit()
        print(f"DishIngredient added: {dish.name} {ingredient.name} {amount} grams")
    except Exception as e:
        print(f"Error adding dish ingredient for {dish.name} and {ingredient.name}: {e}")
    finally:
        session.close()

def insert_initial_data():
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


    # Add Frietje Rendang and its ingredients
    frietje_rendang = add_dish("Frietje Rendang")
    rendang = add_ingredient("Rendang")
    fries = add_ingredient("Fries")
    danish_cheese = add_ingredient("Danish Cheese")
    zz_kk = add_ingredient("SS Cucumber") 

    add_dish_ingredient(frietje_rendang, rendang, 120)
    add_dish_ingredient(frietje_rendang, fries, 80)
    add_dish_ingredient(frietje_rendang, danish_cheese, 50)
    add_dish_ingredient(frietje_rendang, zz_kk, 25)


    # Add Taco Shrimp and its ingredients
    taco_shrimp = add_dish("Taco Shrimp")
    shrimp = add_ingredient("Shrimp")
    salsa_verde = add_ingredient("Salsa Verde")
    pico_de_gallo = add_ingredient("Pico de Gallo")
    iceberg = add_ingredient("Iceberg Lettuce")
    tempura = add_ingredient("Tempura Batter")

    add_dish_ingredient(taco_shrimp, shrimp, 2) # fix it to be pieces
    add_dish_ingredient(taco_shrimp, salsa_verde, 30)
    add_dish_ingredient(taco_shrimp, pico_de_gallo, 40)
    add_dish_ingredient(taco_shrimp, iceberg, 25)
    add_dish_ingredient(taco_shrimp, tempura, 24) # not mixed


    # Add Popcorn Shrimp and its ingredients
    popcorn_shrimp = add_dish("Popcorn Shrimp")
    yuzu_mayo = add_ingredient("Yuzu Mayonaise")


    add_dish_ingredient(popcorn_shrimp, shrimp, 5)
    add_dish_ingredient(popcorn_shrimp, yuzu_mayo, 60)
    add_dish_ingredient(popcorn_shrimp, tempura, 60) # not mixed
insert_initial_data()
