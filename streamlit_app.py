import streamlit
import pandas
import snowflake.connector
streamlit.title('My Parents New Healthy Diner');
streamlit.header('Breakfast Menu');
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal');
streamlit.text(' 🥗 Kale, Spinach & Rocket Smoothie');
streamlit.text('🐔 Hard-Boiled Free Range Egg');
streamlit.text('🥑🍞 Avocado Toast');
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇');

#bring in external CSV file from s3 bucket 
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt");
#set index of my_fruit_list to be the fruit name as opposed to a number 
my_fruit_list = my_fruit_list.set_index('Fruit');

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries']);
fruits_to_show = my_fruit_list.loc[fruits_selected];

# Display the table on the page.
streamlit.dataframe(fruits_to_show);

#new section to display fruityvice api response 
streamlit.header('Fruityvice Fruit Advice!');

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi");

#remove the json output 
#streamlit.text(fruityvice_response.json());

#lets tidyup the json and make it look nice 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json());

#now output to the screen as a table 
streamlit.dataframe(fruityvice_normalized);

#lets get snowflake connected
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
#streamlit.text("Hello from Snowflake:")
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

#lets create a fruit to add section 
#streamlit.text("What fruit would you like to add?")
add_my_fruit = streamlit.text_input("What fruit would you like to add?", "Jackfruit")


