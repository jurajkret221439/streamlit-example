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
