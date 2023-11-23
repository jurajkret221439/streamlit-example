from sqlalchemy import create_engine, Float, Date, Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

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

# Waste model
class Waste(Base):
    __tablename__ = 'waste'
    id = Column(Integer, primary_key=True)
    dish_id = Column(Integer, ForeignKey("dishes.id"))
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"))
    amount = Column(Float, nullable=False)
    waste_type = Column(String)
    date = Column(Date)

    dish = relationship("Dish", back_populates="waste")
    ingredient = relationship("Ingredient", back_populates="waste")

Dish.waste = relationship("Waste", order_by=Waste.id, back_populates="dish")
Ingredient.waste = relationship("Waste", order_by=Waste.id, back_populates="ingredient")
    


def drop_all_tables_except_waste():
    try:
        session = Session()
        
        # Drop specific tables manually, except the 'waste' table
        Dish.__table__.drop(engine)
        Ingredient.__table__.drop(engine)
        DishIngredient.__table__.drop(engine)
        # Any other tables you have, except for 'Waste'

        session.commit()
        print("All tables except 'waste' dropped.")
    except Exception as e:
        print(f"Error occurred while dropping tables: {e}")
    finally:
        session.close()
drop_all_tables_except_waste()

# Create tables
def create_tables():
    Base.metadata.create_all(engine)
    print("CREATED TABLES")
create_tables()
'''
def create_specific_tables():
    try:
        session = Session()

        # Create specific tables manually, except the 'waste' table
        Dish.__table__.create(engine, checkfirst=True)
        Ingredient.__table__.create(engine, checkfirst=True)
        DishIngredient.__table__.create(engine, checkfirst=True)
        # Any other tables you have, except for 'Waste'

        session.commit()
        print("All tables except 'waste' created.")
    except Exception as e:
        print(f"Error occurred while creating tables: {e}")
    finally:
        session.close()
create_specific_tables()
'''


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

def add_waste(dish_id, ingredient_id, amount, waste_type, date):
    try:
        session = Session()
        waste_data = Waste(dish_id=dish_id, ingredient_id=ingredient_id, amount=amount, waste_type=waste_type, date=date)
        session.add(waste_data)
        session.commit()
        print(f"Waste data added for dish ID {dish_id} and ingredient ID {ingredient_id}")
    except Exception as e:
        print(f"Error adding waste data: {e}")
    finally:
        session.close()



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



def insert_initial_waste_data():

    # Add initial waste data
    add_waste(dish_id=taco_beef.id, ingredient_id=birria.id, amount=1800, waste_type="Meat", date=datetime.strptime("2023-11-04", "%Y-%m-%d").date())
    add_waste(dish_id=frietje_rendang.id,ingredient_id=rendang.id,amount=2300,waste_type="Meat",date=datetime.strptime("2023-11-04", "%Y-%m-%d").date())
    add_waste(dish_id=taco_beef.id, ingredient_id=birria.id, amount=1500, waste_type="Meat", date=datetime.strptime("2023-11-05", "%Y-%m-%d").date())
    add_waste(dish_id=frietje_rendang.id,ingredient_id=rendang.id,amount=2000,waste_type="Meat",date=datetime.strptime("2023-11-05", "%Y-%m-%d").date())
    add_waste(dish_id=taco_beef.id, ingredient_id=birria.id, amount=1000, waste_type="Meat", date=datetime.strptime("2023-11-06", "%Y-%m-%d").date())
    add_waste(dish_id=frietje_rendang.id,ingredient_id=rendang.id,amount=3500,waste_type="Meat",date=datetime.strptime("2023-11-07", "%Y-%m-%d").date())
    add_waste(dish_id=taco_beef.id, ingredient_id=birria.id, amount=2200, waste_type="Meat", date=datetime.strptime("2023-11-07", "%Y-%m-%d").date())
    add_waste(dish_id=frietje_rendang.id,ingredient_id=rendang.id,amount=3500,waste_type="Meat", date=datetime.strptime("2023-11-08", "%Y-%m-%d").date())
    add_waste(dish_id=taco_beef.id, ingredient_id=birria.id, amount=1500, waste_type="Meat", date=datetime.strptime("2023-11-08", "%Y-%m-%d").date())
    add_waste(dish_id=taco_beef.id, ingredient_id=birria.id, amount=800, waste_type="Meat", date=datetime.strptime("2023-11-09", "%Y-%m-%d").date())
    add_waste(dish_id=taco_beef.id, ingredient_id=birria.id, amount=600, waste_type="Meat", date=datetime.strptime("2023-11-10", "%Y-%m-%d").date())
    print("WASTE DATA HAVE BEEN SUCCESSFULLY ADDED")
