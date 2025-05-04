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
        df['Price'] = (df['Price'] * 0.012).round().astype(int)
        df['year_of_warranty'] = df['year_of_warranty'].replace('No information', 'No Warranty')
        return df
    else:
        st.error("Error: 'laptops.csv' file not found!")
        return pd.DataFrame()

df = load_data()

# Unique values for filtering
filters = {col: df[col].dropna().astype(str).unique() for col in ["OS", "processor_brand", "brand", "processor_tier", "gpu_type", "ram_memory", "primary_storage_type", "secondary_storage_type"]}
filters["Warranty"] = ["No Warranty", "1", "2", "3"]

st.write("# Available Laptops")

# Sidebar Filters
user_filters = {key: st.sidebar.selectbox(f"Select {key}", filters[key]) for key in filters.keys()}
user_filters["Price"] = st.sidebar.slider('Max Price', min_value=df["Price"].min(), max_value=df["Price"].max())
user_filters["Rating"] = st.sidebar.slider('Min Rating', min_value=df["Rating"].min(), max_value=df["Rating"].max())
user_filters["Touchscreen"] = st.sidebar.radio("Touch Screen", ["All", "Touchscreen", "Non-Touchscreen"])

# Apply filters dynamically
query_conditions = []

# Apply categorical filters
for key, value in user_filters.items():
    if key in filters and value: 
        query_conditions.append(f"{key}.astype(str) == '{value}'")

# Apply numerical filters
query_conditions.append(f"Price <= {user_filters['Price']}")
query_conditions.append(f"Rating >= {user_filters['Rating']}")

# Apply touchscreen filter
if user_filters["Touchscreen"] == "Touchscreen":
    query_conditions.append("is_touch_screen == True")
elif user_filters["Touchscreen"] == "Non-Touchscreen":
    query_conditions.append("is_touch_screen == False")

# Filter Data
if query_conditions:
    filtered_df = df.query(" & ".join(query_conditions))
else:
    filtered_df = df

st.dataframe(filtered_df.head(20), use_container_width=True)
