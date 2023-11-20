import streamlit as st
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

df_fruit_list = pd.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
df_fruit_list.set_index('Fruit', inplace=True)

st.title('My Parents New Healthy Dinner')

st.header('Breakfast Menu')
st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')
st.text('🥑🍞 Avocado Toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = st.multiselect("Pick some fruits:", list(df_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = df_fruit_list.loc[fruits_selected]

def non_empty(obj1, obj2):
  if len(obj1) > 0:
    return obj1
  else: 
    return obj2
  
# New Section to display fruityvice api response
st.dataframe(non_empty(fruits_to_show, df_fruit_list))

# another section
st.header("Fruityvice Fruit Advice!")

fruit_choice = st.text_input('What fruit would you like information about?','Kiwi')
st.write('The user entered ', fruit_choice)
fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_choice}")
# take the json version of the response and normalize it
fruityvice_normalized = pd.json_normalize(fruityvice_response.json ()) #output it the screen as a table
st.dataframe (fruityvice_normalized)

# snowflake
my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_row = my_cur.fetchall()
st.text("The fruit load list contains:")
st.dataframe(my_data_row)

st.stop()
# Allow the end user to add a fruit to the list
add_my_fruit = st.text_input('What fruit would you like to add?','Kiwi')
st.write('Thanks for adding ', add_my_fruit)
my_cur.execute(f"insert into fruit_load_list values ({add_my_fruit})")



