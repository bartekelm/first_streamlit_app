import streamlit as st
import pandas as pd

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

# Display the table on the page.
st.dataframe(fruits_selected)
