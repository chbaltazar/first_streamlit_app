import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Mom´s New Helthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let´s put a pick list here so they can pick the fruit they want to include
fruits_selected = streamlit.multiselect("Pick come fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page
streamlit.dataframe(fruits_to_show)

# New section to display fruityvice API response
streamlit.header('Fruityvice Fruit Advice!')
fruit_choise = streamlit.text_input('What fruit would you like information about', 'Kiwi')
streamlit.write('The user entered ', fruit_choise)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choise)

# Take the json version of the response and normalize it
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

# Output it the screen as a table
streamlit.dataframe(fruityvice_normalized)

# dont run anything past here while we trobleshoot
streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit lad list contains:")
streamlit.dataframe(my_data_rows)

# New section to add a fruit to the list
add_my_fruit = streamlit.text_input('What fruit would you like to add', 'jackfruit')
streamlit.write('thanks for adding ', add_my_fruit)

my_cur.execute("INSERT INTO PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST (FRUIT_NAME) VALUES ('From Streamlit')")
