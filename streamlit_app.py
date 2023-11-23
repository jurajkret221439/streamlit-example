import streamlit as st
from utils import load_css
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from setup_database import Dish, Ingredient, DishIngredient
import pickle
from sklearn.linear_model import LinearRegression
import numpy as np


def load_model(model_path):
    with open(model_path, "rb") as file:
        return pickle.load(file)
    
model_tacobeef =  load_model("models/TacoBeefModel1.pkl")
model_frietje_rendang = load_model("models/FrietjeRendangModel1.pkl")
model_tacoshrimp = load_model("models/TacoShrimpModel1.pkl")
model_popcorn_shrimp = load_model("models/PopcornShrimpModel1.pkl")
# Connect to the database
engine = create_engine('sqlite:///tsfc.db')
Session = sessionmaker(bind=engine)

# Function to get dish and its ingredients
def get_dish_with_ingredients(dish_name):
    session = Session()
    dish = session.query(Dish).filter_by(name=dish_name).first()
    if dish is None:
        return None, []  # Return None and an empty list if dish is not found
    dish_ingredients = session.query(DishIngredient).filter_by(dish_id=dish.id).all()
    ingredients = [{"name": di.ingredient.name, "amount": di.amount} for di in dish_ingredients]
    return dish, ingredients


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
            st.session_state["submitted"] = True

   
elif st.session_state['submitted']:
    with right:
        for _ in range(8):
            st.write("")
        st.metric(label="Dinner Reservations", value=int(st.session_state['reservation_input']))
    
    
    Fryer_tab, Cold_tab = st.tabs(["Fryer", "Cold"])

    with Fryer_tab:
        fryer_left, fryer_center1, fryer_center2, fryer_right = st.columns([2,3,3,1])
        dishes_fryer_db = ["Taco Beef", "Taco Shrimp", "Frietje Rendang", "Popcorn Shrimp",]
        dishes_fryer_path = ["images/TacoBeef.jpg", "images/Taco Shrimp.jpg", "images/Frietje Rendang.jpg", "images/Popcorn Shrimp.jpg"]

        with fryer_left:
            spaces_after_dish = [7, 8, 5, 3]  
            for _ in range(3):
                st.write("")
            for i, dish_name in enumerate(dishes_fryer_db):
                st.image(dishes_fryer_path[i], caption=dish_name, use_column_width=True)
                for _ in range(spaces_after_dish[i]):
                    st.write("")
                
                    
        with fryer_center1:
            # Display details of dishe  s
            for dish_name in dishes_fryer_db:
                dish, ingredients = get_dish_with_ingredients(dish_name)
                if dish:
                    st.subheader("Ingredients")
                    for ingredient in ingredients:
                        st.write(f"{ingredient['name']}: {ingredient['amount']} grams") 
                else:
                    st.write(f"Details for {dish_name} not found.") 
                st.markdown("---")


        with fryer_center2:
            spaces_after_dish = [9, 11, 9, 0]
           
            model_list =[model_tacobeef, model_tacoshrimp, model_frietje_rendang, model_popcorn_shrimp]
            for i in range(len(model_list)):
                
                st.subheader("Est. Sales")
                if "reservation_input" in st.session_state and st.session_state["reservation_input"]:
                    input_data = np.array([[st.session_state['reservation_input']]])
                    prediction = model_list[i].predict(input_data)
                    st.metric(label= "Metric",label_visibility="hidden",value =f"{int(prediction[0])}")
                for _ in range(spaces_after_dish[i]):
                    st.write(" ")



    with Cold_tab:
        st.write("Content for the other tab")
        # Include content for the other tab
        with left:
            for _ in range(10):
                st.write("")
            if st.button('Home'):
                reset_form()
    

# Footer (Optional)
st.markdown("---")
st.markdown("© 2023 Restaurant Dashboard")