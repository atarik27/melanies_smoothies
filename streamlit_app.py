# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

st.title("Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!""")

name_on_order = st.text_input("Name on Smoothie:" )

from snowflake.snowpark.functions import col

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))

ingredients_list = st.multiselect('choose up to 5 fruits' , my_dataframe , max_selections = 5)
                   
if ingredients_list:
    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + '  '
        

my_insert_stmt = """ insert into smoothies.public.orders(ingredients , name_on_order)
            values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

time_to_insert = st.button('submit order')
if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered,' + " " + name_on_order +"!", icon="✅")