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
st.header('Fruityvice Fruit Advice!')

def get_fruityvice_data(fruit):
  fruityvice_response = requests.get(f'https://fruityvice.com/api/fruit/{fruit}')
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

try:
  fruit_choice = st.text_input('What fruit would you like information about?')
  if not fruit_choice:
    st.error('Please select a fruit to get information.')
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    st.dataframe(back_from_function)
except URLError as e:
  st.error()

# snowflake
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute('select * from fruit_load_list')
    return my_cur.fetchall()


st.header('View our Fruit List - add your favorites!')
if st.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**st.secrets['snowflake'])
  my_data_rows = get_fruit_load_list()
  st.dataframe(my_data_rows)


# Allow the end user to add a fruit to the list
def insert_fruit_load_list(fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute(f"insert into fruit_load_list values ('{fruit}')")
    return f"Thanks for adding {fruit}"

if st.button('Add a Fruit to the list!'):
  my_cnx = snowflake.connector.connect(**st.secrets['snowflake'])
  my_fruit = st.text_input('What fruit would you like to add?','Kiwi')
  st.write(insert_fruit_load_list(my_fruit))



