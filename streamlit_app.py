import streamlit as st
from utils import load_css
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from setup_database_azure import SessionLocal, Dish, Ingredient, DishIngredient,  Waste
import pickle
from sklearn.linear_model import LinearRegression
import numpy as np
from datetime import datetime, date
import os
import pyodbc
from dotenv import load_dotenv
import logging
from functions import get_dish_with_ingredients, get_dishes, get_ingredients_for_dish, add_waste, add_base_waste_entries_for_all_dishes, calculate_average_waste

logging.basicConfig(level=logging.INFO)


def navigate_to(dish_name):
    st.session_state['current_page'] = dish_name

def load_model(model_path):
    with open(model_path, "rb") as file:
        return pickle.load(file)

# Load Models    
model_tacobeef =  load_model("models/TacoBeefModel2.pkl")
model_frietje_rendang = load_model("models/FrietjeRendangModel1.pkl")
model_tacoshrimp = load_model("models/TacoShrimpModel1.pkl")
model_popcorn_shrimp = load_model("models/PopcornShrimpModel1.pkl")

load_dotenv()  # This loads the variables from .env into the environment

@st.cache_resource
def init_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
        + st.secrets["server"]
        + ";DATABASE="
        + st.secrets["database"]
        + ";UID="
        + st.secrets["username"]
        + ";PWD="
        + st.secrets["password"]
    )

conn = init_connection()


       

# Initialize session state
if 'submitted' not in st.session_state:
    st.session_state['submitted'] = False

if 'reservation_input' not in st.session_state:
    st.session_state['reservation_input'] = ''

# Defines columns 
left, center, right = st.columns([4,6,3])
# Header
with center:
    st.title('TSFC Version 1')

# Reset view to allow for new input
def reset_form():
    st.session_state['submitted'] = False
    st.session_state['reservation_input'] = ""


if not st.session_state['submitted']:
    with left:
        # Creates padding (shifts everything down)
        for _ in range(7):
            st.write("")   

    # Input for Dinner Reservations
        reservation_input = st.session_state['reservation_input'] = st.text_input("Dinner Reservations",value= st.session_state["reservation_input"])

    # Check if input is not empty
        is_input_empty = st.session_state['reservation_input'].strip() == ""

    # Submit button for the reservations
        if st.button('Submit'):
        # Ensure that the input is converted to numeric type
            try:
                st.session_state['reservation_input'] = float(reservation_input)
            except ValueError:
                st.error("Please enter a valid number for reservations.")
                logging.error("Please enter a valid number for reservations.")
            st.session_state["submitted"] = True

   
elif st.session_state['submitted']:
    with right:
        for _ in range(8):
            st.write("")
        st.metric(label="Dinner Reservations", value=int(st.session_state['reservation_input']))
    
    
    Fryer_tab, Cold_tab, Waste_tab = st.tabs(["Fryer", "Cold", "Waste"])

    with Fryer_tab:
        fryer_left, fryer_center1, fryer_center2, fryer_right = st.columns([2,3,3,1])
        dishes_fryer_db = ["Taco Beef", "Taco Shrimp", "Frietje Rendang", "Popcorn Shrimp",]
        dishes_fryer_path = ["images/TacoBeef.jpg", "images/Taco Shrimp.jpg", "images/Frietje Rendang.jpg", "images/Popcorn Shrimp.jpg"]

        estimated_sales = []
        with fryer_left:
            spaces_after_dish = [7, 8, 5, 3]  
            for _ in range(2):
                st.write("")
            for i, dish_name in enumerate(dishes_fryer_db):
                st.image(dishes_fryer_path[i], caption=dish_name, use_column_width=True)              
                for _ in range(spaces_after_dish[i]):
                    st.write("")
                

        with fryer_center2:
            estimated_sales.clear()
            spaces_after_dish = [9, 11, 9, 0]
           
            model_list =[model_tacobeef, model_tacoshrimp, model_frietje_rendang, model_popcorn_shrimp]
            for i, model in enumerate(model_list):
                
                st.subheader("Est. Sales")
                if "reservation_input" in st.session_state and st.session_state["reservation_input"]:
                    input_data = np.array([[st.session_state['reservation_input']]])
                    prediction = model_list[i].predict(input_data)
                    sales_prediction = int(prediction[0])
                    estimated_sales.append(sales_prediction)
                    st.metric(label= "Metric",label_visibility="hidden",value =f"{sales_prediction}")
                for _ in range(spaces_after_dish[i]):
                    st.write(" ")

        with fryer_center1:
            # Display details of dishe  s
            for i, dish_name in enumerate(dishes_fryer_db):
                dish, ingredients = get_dish_with_ingredients(dish_name)
                if dish and estimated_sales[i] > 0:
                    st.subheader("Ingredients")
                    multiplier = estimated_sales[i]

                    for ingredient in ingredients:
                        adjusted_amount = ingredient['amount'] * multiplier
                        st.write(f"{ingredient['name']}: {adjusted_amount} {ingredient['amount_type']} ")
                        #st.write(f"{ingredient['name']}: {ingredient['amount']} grams") (ADD AMOUNT {ingredient['storage_type']})"
                else:
                    st.write(f"Details for {dish_name} not found.") 
                st.markdown("---")

    
          


    with Cold_tab:
        st.write("Content for the other tab")
        # Include content for the other tab
        with left:
            for _ in range(10):
                st.write("")
            if st.button('Home'):
                reset_form()
    


    with Waste_tab:
        st.markdown("""
        <h1 style="padding-left: 90px;">Waste</h1>
    """, unsafe_allow_html=True)
        Waste_left, Padding, Waste_right = st.columns([3,1,3])
        with Waste_left:
            name = st.text_input("Name", value="", placeholder="Enter name here")
            # Dropdown for dish selection
            dishes = get_dishes()
            dish_options = {d.name: d.id for d in dishes}
            selected_dish_name = st.selectbox("Select Dish", options=list(dish_options.keys()))
            
            # Update session state for selected dish
            if 'selected_dish_id' not in st.session_state or st.session_state.selected_dish_name != selected_dish_name:
                st.session_state.selected_dish_id = dish_options[selected_dish_name]
                st.session_state.selected_dish_name = selected_dish_name
            
            # Dropdown for ingredient selection based on selected dish
            # Fetch the selected dish and ingredient IDs
            ingredients = get_ingredients_for_dish(st.session_state.selected_dish_id)
            ingredient_options = [i.name for i in ingredients]
            selected_ingredient = st.selectbox("Select Ingredient", options=ingredient_options)
            selected_ingredient_id = next(i.id for i in ingredients if i.name == selected_ingredient)
            selected_dish_id = dish_options[selected_dish_name]
            # Inputs for amount, type of waste, and date
            amount = st.number_input("Amount of Waste in Grams", min_value=0)
            waste_date = date.today()

            if st.button('Submit Waste Data'):
                if name.strip():
                    if selected_ingredient_id is not None:
                        # Call the add_waste function and handle the response
                        response = add_waste(dish_id=selected_dish_id, ingredient_id=selected_ingredient_id, amount=amount, date=waste_date, name=name)
                        if response.startswith("Error"):
                            st.error(response)
                        else:
                            st.success(response)
                    else:
                        st.error("Please select a valid ingredient.")
                else:
                    # If the name is empty, display an error message
                    st.error("Please enter a name before submitting waste data.") 
            # Button to add zero waste for all ingredients of all dishes
            if st.button('Add Zero Waste for All Ingredients'):
                if name.strip():
                    successes, errors = add_base_waste_entries_for_all_dishes(name)
                    if errors == 0:
                        st.success(f"All zero waste entries added successfully for {successes} ingredients.")
                    else:
                        st.error(f"Added {successes} zero waste entries with {errors} errors. Check logs for details.")
                else:
                    st.error("Please enter a name before adding zero waste entries.")
        with Padding:
            st.markdown("  ")
        with Waste_right:
            # When a dish and ingredient are selected, calculate and display the average waste
            if st.session_state.selected_dish_id and selected_ingredient:
                average_waste = calculate_average_waste(st.session_state.selected_dish_id, selected_ingredient_id)
                if average_waste is not None:
                    
                    #st.markdown(
                        #f"The average waste for **{selected_ingredient}** is **{average_waste:.2f} grams.**", 
                    # unsafe_allow_html=True)
                    st.metric(label=f"Average waste of {selected_ingredient}", value=f"{average_waste:.2f} grams")
                else:
                    st.write("No waste data available for the selected dish and ingredient.")
# Footer (Optional)
st.markdown("---")
st.markdown("© 2023 Restaurant Dashboard")