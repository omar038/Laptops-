import pandas as pd  # Import pandas for data manipulation
import streamlit as st  # Import Streamlit for UI elements
import plotly.express as px  # Import Plotly for interactive visualizations
import plotly.graph_objects as go  # Import Plotly graph objects
import os  # Import OS module for file operations
from functools import reduce  # Import reduce for filtering conditions

# Configure Streamlit page settings
st.set_page_config(page_title='Laptops', layout="wide", page_icon='💻')

# Apply custom styles from CSS file (if exists)
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Function to load laptop data
@st.cache_data
def load_data():
    # Load data from CSV file
    df = pd.read_csv('laptops.csv')
    return df

df = load_data()

# Preprocessing Data
df['Price'] = df['Price'] * 0.012  # Convert price to appropriate currency
df['Price'] = df['Price'].round(decimals=0).astype(int)  # Round and convert to integer
df['year_of_warranty'] = df['year_of_warranty'].replace('No information', 'No Warranty')  # Standardize warranty information

# Extract unique values for filtering options
brand_list = df["brand"].unique().tolist()
ratinglist = df["Rating"].unique().tolist()
processor_tier = df["processor_tier"].unique().tolist()
OS_list = df["OS"].unique().tolist()
Chip_list = df["processor_brand"].unique().tolist()
Ram_list = df["ram_memory"].unique().tolist()
primary_storage_list = df['primary_storage_type'].unique().tolist()
gpu_type_list = df['gpu_type'].unique().tolist()

# Display main page title
st.write("# Available Laptops")

# Sidebar filters for user selection
Desired_os = st.sidebar.selectbox('What is your desired OS', OS_list, index=None)
Chip = st.sidebar.selectbox('What Chip Do You Want', Chip_list, index=None)
Brand = st.sidebar.selectbox('Which Brand would you like', brand_list, index=None)
processor = st.sidebar.selectbox('Which processor you would like', processor_tier, index=None)
gpu_type = st.sidebar.selectbox('Which GPU type you would like', gpu_type_list, index=None)
Ram = st.sidebar.selectbox('Select your memory', Ram_list, index=None)
Primary_storage = st.sidebar.selectbox('Select your Primary Storage', primary_storage_list, index=None)
Secondary_storage = st.sidebar.selectbox('Select your Secondary Storage', primary_storage_list, index=None)
years_of_warranty = st.sidebar.selectbox('Warranty', ['No Warranty', '1', '2', '3'], index=None)
Price = st.sidebar.slider('Price', 0, 5000)  # Slider for price range
Rating = st.sidebar.slider('Rating', 0, 85)  # Slider for rating filter
touchscreen_filter = st.sidebar.radio("Touch Screen", ["All", "Touchscreen", "Non-Touchscreen"])  # Radio buttons for touchscreen filter

# Initialize list to store filtering conditions
filter_conditions = []

# Apply filters based on user input
if processor:
    filter_conditions.append(df['processor_tier'] == processor)
if Price:
    filter_conditions.append(df['Price'] > Price)
if Rating:
    filter_conditions.append(df['Rating'] > Rating)
if Brand:
    filter_conditions.append(df['brand'] == Brand)
if Desired_os:
    filter_conditions.append(df['OS'] == Desired_os)
if Chip:
    filter_conditions.append(df['processor_brand'] == Chip)
if Ram:
    filter_conditions.append(df['ram_memory'] == Ram)
if Primary_storage:
    filter_conditions.append(df['primary_storage_type'] == Primary_storage)
if Secondary_storage:
    filter_conditions.append(df['secondary_storage_type'] == Secondary_storage)
if gpu_type:
    filter_conditions.append(df['gpu_type'] == gpu_type)
if years_of_warranty:
    filter_conditions.append(df['year_of_warranty'] == years_of_warranty)

# Apply touchscreen filter
elif touchscreen_filter == "Touchscreen":
    filter_conditions.append(df['is_touch_screen'] == True)
elif touchscreen_filter == "Non-Touchscreen":
    filter_conditions.append(df['is_touch_screen'] == False)

# Apply filtering if conditions exist
if filter_conditions:
    filtered_df = df[reduce(lambda x, y: x & y, filter_conditions)]  # Use reduce to combine conditions
    st.dataframe(filtered_df.head(20), use_container_width=True)  # Display filtered results
else:
    filtered_df = df  # Show all data if no filters applied
    st.dataframe(filtered_df.head(20), use_container_width=True)


