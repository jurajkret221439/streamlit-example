# Tab navigation (optional)
tab1, tab2 = st.tabs(["Home", "Reservations"])

with tab1:
    # Use columns to create a grid layout
    col1, col2, col3 = st.columns([3, 1, 2])

    with col1:
        # Display the first image and its stats
        st.image('images/Taco Beef Demo.jpg', caption='Taco Beef')
        st.metric(label="Est. sales", value="52")

        # Display the second image and its stats
        st.image('images/Frietje Rendang demo.jpg', caption='Frietje Rendang')
        st.metric(label="Est. sales", value="0")

    with col2:
        # Add ingredients list or other information here
        st.subheader("Ingredients")
        st.write("birria (2.29 bag) - 4576 grams")
        # Add more ingredients

    with col3:
        # Display the number of reservations
        st.metric(label="Number of Dinner Reservations", value=input_reservations)



import streamlit as st
from utils import load_css


# Initialize session state
if 'submitted' not in st.session_state:
    st.session_state['submitted'] = False

if 'reservation_input' not in st.session_state:
    st.session_state['reservation_input'] = ''

# Defines columns 
left, center, right = st.columns([2,5,2])
# Header
with center:
    st.title('Restaurant Dashboard')

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
        st.session_state['reservation_input'] = st.text_input("Dinner Reservations",value= st.session_state["reservation_input"])

    # Check if input is not empty
        is_input_empty = st.session_state['reservation_input'].strip() == ""

    # Submit button for the reservations
        if st.button('Submit', disabled=is_input_empty):
            st.session_state['submitted'] = True

    # A 'Home' button to reset the form
elif st.session_state['submitted']:
    with center:
        st.metric(label="Number of Dinner Reservations", value=st.session_state['reservation_input'])
        if st.button('Home'):
            reset_form()

# Footer (Optional)
st.markdown("---")
st.markdown("© 2023 Restaurant Dashboard")