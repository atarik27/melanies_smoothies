# Import necessary packages
import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

# Initialize the Snowflake session using Streamlit secrets
session = Session.builder.configs(st.secrets["connections"]["snowflake"]).create()

# Streamlit app title and introductory text
st.title("Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Input field for the name on the smoothie order
name_on_order = st.text_input("Name on Smoothie:")

# Query the available fruit options from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))

# Allow user to select fruits from the available options
ingredients_list = st.multiselect('Choose up to 5 fruits', my_dataframe, max_selections=5)

# Initialize ingredients_string with a default value if no fruits are selected
ingredients_string = ' '.join(ingredients_list) if ingredients_list else 'No ingredients selected'

# Create SQL insert statement to log the order
my_insert_stmt = f"""INSERT INTO smoothies.public.orders (ingredients, name_on_order)
                     VALUES ('{ingredients_string}', '{name_on_order}')"""

# Insert the order when the button is pressed
time_to_insert = st.button('Submit Order')
if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
