from sqlalchemy import create_engine, Float, Date, Column, Integer, String, ForeignKey, Table, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
import pyodbc
import streamlit as st

server = st.secrets["server"]
database = st.secrets["database"]
username = st.secrets["username"]
password = st.secrets["password"]
driver = '{ODBC Driver 17 for SQL Server}'

# Connection string
connection_string = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"



# Database setup
engine = create_engine(connection_string)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Verifying the connection
try:
    # Attempt to connect to the database
    with engine.connect() as connection:
        print("Connection to the database was successful.")
except Exception as e:
    print(f"Database connection failed: {e}")
    
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
    amount_type = Column(String)
    storage_type = Column(String)
    waste_type = Column(String)

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
    dish_name = Column(String)
    ingredient_name = Column(String)
    amount = Column(Float, nullable=False)
    waste_type = Column(String)
    date = Column(Date)
    entry_time = Column(Time)

    dish = relationship("Dish", back_populates="waste")
    ingredient = relationship("Ingredient", back_populates="waste")
    
Dish.waste = relationship("Waste", order_by=Waste.id, back_populates="dish")
Ingredient.waste = relationship("Waste", order_by=Waste.id, back_populates="ingredient")
    

# Function to add a dish with context manager for session
def add_dish(name):
    with SessionLocal() as session:
        try:
            dish = Dish(name=name)
            session.add(dish)
            session.commit()
            print(f"Dish added: {dish.name}")
            return dish
        except Exception as e:
            session.rollback()
            print(f"Error adding dish {name}: {e}")

# Function to add an ingredient with context manager for session
def add_ingredient(name, amount_type, storage_type, waste_type):
    with SessionLocal() as session:
        try:
            ingredient = Ingredient(name=name, amount_type=amount_type, storage_type=storage_type, waste_type=waste_type)
            session.add(ingredient)
            session.commit()
            print(f"Ingredient added: {ingredient.name}")
            return ingredient
        except Exception as e:
            session.rollback()
            print(f"Error adding ingredient {name}: {e}")

# Function to associate a dish with an ingredient with context manager for session
def add_dish_ingredient(dish, ingredient, amount):
    with SessionLocal() as session:
        try:
            dish_ingredient = DishIngredient(dish_id=dish.id, ingredient_id=ingredient.id, amount=amount)
            session.add(dish_ingredient)
            session.commit()
            print(f"DishIngredient added: {dish.name} {ingredient.name} {amount} grams")
        except Exception as e:
            session.rollback()
            print(f"Error adding dish ingredient for {dish.name} and {ingredient.name}: {e}")

# Function to add waste with context manager for session
def add_waste(dish_id, ingredient_id, amount, date):
    with SessionLocal() as session:
        try:
            # Fetch the waste_type from the Ingredient model
            dish = session.query(Dish).get(dish_id)
            ingredient = session.query(Ingredient).get(ingredient_id)
            if dish is None or ingredient is None:
                raise ValueError(f"No dish or ingredient found with ID {dish_id} or {ingredient_id}")
            current_time = datetime.now().time()
            waste_type = ingredient.waste_type
            waste_data = Waste(
                dish_id=dish_id, 
                dish_name=dish.name, 
                ingredient_id=ingredient_id, 
                ingredient_name=ingredient.name, 
                amount=amount, 
                waste_type=waste_type, 
                date=date, 
                entry_time=current_time
            )
            session.add(waste_data)
            session.commit()
            print(f"Waste data added for dish ID {dish_id} and ingredient ID {ingredient_id}")
        except Exception as e:
            session.rollback()
            print(f"Error adding waste data: {e}")

