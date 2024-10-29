# Import python packages
import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

# Initialize the Snowflake session
session = Session.builder.configs(st.secrets["connections"]["snowflake"]).create()

st.title("Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name on Smoothie:")

# Query the fruit options from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))

# Allow user to select fruits
ingredients_list = st.multiselect('Choose up to 5 fruits', my_dataframe, max_selections=5)

if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)

# Create SQL insert statement
my_insert_stmt = f"""INSERT INTO smoothies.public.orders (ingredients, name_on_order)
                     VALUES ('{ingredients_string}', '{name_on_order}')"""

# Insert order when button is pressed
time_to_insert = st.button('Submit Order')
if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
