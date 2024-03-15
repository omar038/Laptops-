import pandas as pd 
import streamlit as st 
import plotly.express as px
import plotly.graph_objects as go
from functools import reduce


st.set_page_config(page_title='Laptops',layout="wide" ,page_icon='💻',)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

@st.cache_data
def load_data():
    # تحميل البيانات 
    df = pd.read_csv('laptops.csv')
    return df
df = load_data()

#constants for page two
df['Price'] = df['Price'] * 0.012
df['Price'] = df['Price'].round(decimals=0).astype(int)
df['year_of_warranty'] = df['year_of_warranty'].replace('No information', 'No Warranty')

brand_list = df["brand"].unique().tolist()
ratinglist = df["Rating"].unique().tolist()
processor_tier= df["processor_tier"].unique().tolist()
OS_list = df["OS"].unique().tolist()
Chip_list = df["processor_brand"].unique().tolist()
Ram_list = df["ram_memory"].unique().tolist()
primary_storage_list = df['primary_storage_type'].unique().tolist()
gpu_type_list = df['gpu_type'].unique().tolist()

st.write("# Available Laptops")
# Add your content for Page 2 here
Desired_os = st.sidebar.selectbox('What is your desierd OS ',OS_list ,index=None)
Chip = st.sidebar.selectbox('What Chip Do You Want ',Chip_list ,index=None)

Brand = st.sidebar.selectbox('which Brand would you like ',brand_list ,index=None)
processor = st.sidebar.selectbox('which processor you would like ',processor_tier,index=None)
gpu_type = st.sidebar.selectbox('which gpu type you would like ',gpu_type_list,index=None)
Ram = st.sidebar.selectbox('Select your memory ',Ram_list,index=None)
Primary_storage = st.sidebar.selectbox('Select your Primary Storage ',primary_storage_list,index=None)
Secondary_storage = st.sidebar.selectbox('Select your Secondary Storage ',primary_storage_list,index=None)
years_of_warranty = st.sidebar.selectbox('Warranty ',['No Warranty','1','2','3'],index=None)
Price = st.sidebar.slider('Price',0,5000)
Rating = st.sidebar.slider('Rating ',0,85)
touchscreen_filter  =  st.sidebar.radio("Touch Screen" ,["All", "Touchscreen", "Non-Touchscreen"] )

# Check if any selections have been made
filter_conditions = []
# Add conditions only if the corresponding input is provided
if processor:
    filter_conditions.append(df['processor_tier'] == processor)
if Price:
    filter_conditions.append(df['Price'] > Price)
if Rating:
    filter_conditions.append(df['Rating'] > Rating)
if Brand:
    filter_conditions.append(df['brand'] == Brand)
if Desired_os:
    filter_conditions.append(df['OS']== Desired_os )
if Chip:
    filter_conditions.append(df['processor_brand']== Chip )
if Ram:
    filter_conditions.append(df['ram_memory']== Ram )
if Primary_storage:
    filter_conditions.append(df['primary_storage_type']== Primary_storage )
if Secondary_storage:
    filter_conditions.append(df['secondary_storage_type']== Secondary_storage )
if gpu_type:
    filter_conditions.append(df['gpu_type']== gpu_type ) 
if years_of_warranty:
    filter_conditions.append(df['year_of_warranty']== years_of_warranty ) 
elif touchscreen_filter == "Touchscreen":
    filter_conditions.append(df['is_touch_screen'] == True) 
elif touchscreen_filter == "Non-Touchscreen":
    filter_conditions.append(df['is_touch_screen'] == False)
# Apply the cross-filtering conditions
if filter_conditions:
    filtered_df = df[reduce(lambda x, y: x & y, filter_conditions)]
    st.table(filtered_df[:50])
else:
    # Show all data by default
    filtered_df = df
    st.table(filtered_df[:50])

