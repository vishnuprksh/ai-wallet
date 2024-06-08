import streamlit as st

# Set the title of the web app
st.title('Simple Streamlit App')

# Create a text input widget
user_input = st.text_input('Enter some text:')

# Create a button widget
if st.button('Submit'):
    # Display the input text
    st.write('You entered:', user_input)
