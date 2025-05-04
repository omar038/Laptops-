import pandas as pd
import streamlit as st
import os

st.set_page_config(page_title='Laptops', layout="wide", page_icon='💻')

# Load custom styles
if os.path.exists("style.css"):
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load laptop data efficiently."""
    if os.path.exists('laptops.csv'):
        df = pd.read_csv('laptops.csv')
        return df
    else:
        st.error("Error: 'laptops.csv' file not found!")
        return pd.DataFrame()

df = load_data()

# Data preprocessing
df['Price'] = (df['Price'] * 0.012).round().astype(int)
df['year_of_warranty'] = df['year_of_warranty'].replace('No information', 'No Warranty')

# Unique values for filtering
filters = {
    "OS": df["OS"].dropna().unique(),
    "Chip": df["processor_brand"].dropna().unique(),
    "Brand": df["brand"].dropna().unique(),
    "Processor": df["processor_tier"].dropna().unique(),
    "GPU Type": df["gpu_type"].dropna().unique(),
    "RAM": df["ram_memory"].dropna().unique(),
    "Primary Storage": df["primary_storage_type"].dropna().unique(),
    "Secondary Storage": df["secondary_storage_type"].dropna().unique(),
    "Warranty": ["No Warranty", "1", "2", "3"]
}

st.write("# Available Laptops")

# Sidebar Filters
user_filters = {
    "OS": st.sidebar.selectbox('Select OS', filters["OS"]),
    "Chip": st.sidebar.selectbox('Select Chip', filters["Chip"]),
    "Brand": st.sidebar.selectbox('Select Brand', filters["Brand"]),
    "Processor": st.sidebar.selectbox('Select Processor', filters["Processor"]),
    "GPU Type": st.sidebar.selectbox('Select GPU Type', filters["GPU Type"]),
    "RAM": st.sidebar.selectbox('Select RAM', filters["RAM"]),
    "Primary Storage": st.sidebar.selectbox('Select Primary Storage', filters["Primary Storage"]),
    "Secondary Storage": st.sidebar.selectbox('Select Secondary Storage', filters["Secondary Storage"]),
    "Warranty": st.sidebar.selectbox('Select Warranty', filters["Warranty"]),
    "Price": st.sidebar.slider('Max Price', 0, 5000),
    "Rating": st.sidebar.slider('Min Rating', 0, 85),
    "Touchscreen": st.sidebar.radio("Touch Screen", ["All", "Touchscreen", "Non-Touchscreen"])
}

# Apply filters dynamically
query_conditions = []
for key, value in user_filters.items():
    if value and key in df.columns:
        query_conditions.append(f"{key} == '{value}'")

if user_filters["Price"]:
    query_conditions.append(f"Price <= {user_filters['Price']}")
if user_filters["Rating"]:
    query_conditions.append(f"Rating >= {user_filters['Rating']}")
if user_filters["Touchscreen"] == "Touchscreen":
    query_conditions.append("is_touch_screen == True")
elif user_filters["Touchscreen"] == "Non-Touchscreen":
    query_conditions.append("is_touch_screen == False")

# Filter Data
if query_conditions:
    filtered_df = df.query(" & ".join(query_conditions))
else:
    filtered_df = df

st.table(filtered_df.head(20),use_container_width=True)
