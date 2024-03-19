import pandas as pd 
import streamlit as st 
import plotly.express as px
import plotly.graph_objects as go
st.set_page_config(layout="wide" ,page_title='Data Overview',page_icon="🧑‍💻")
# pandas analytics
df = pd.read_csv('laptops.csv')

#convert prices from rupee to Doller
df['Price'] = df['Price'] * 0.012
df['Price'] = df['Price'].round(decimals=0).astype(int)

#Counting number of laptops per Brand
laptops_per_brand = df['brand'].value_counts().reset_index()
laptops_per_brand.columns = ['brand', 'Count']

#avarage rating per Chip
avg_df = df[['processor_brand' , 'Rating' , 'Price']]
brands = ['amd', 'intel', 'apple']
avg_list = [df[df['processor_brand'] == brand]['Rating'].mean() for brand in brands]

#count number of laptops that has a touch screen
is_touch_screen = df['is_touch_screen'].value_counts().reset_index()
#opreating system distrubtion
operating_sys = df['OS'].value_counts().reset_index()[:4]
# Avarage price per brand
avg_price_by_brand = df[['brand' , 'Price']]
avg_price_by_brand = df.groupby('brand')['Price'].mean().reset_index()
sorted_avg_price_by_brand = avg_price_by_brand.sort_values(by='Price' ,ascending=False)

#Avarage rating per brand
avg_Rating_by_brand = df[['brand' , 'Rating']]
avg_Rating_by_brand = df.groupby('brand')['Rating'].mean().reset_index()
sorted_avg_Rating_by_brand = avg_Rating_by_brand.sort_values(by='Rating' ,ascending=False)



with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

brand_color_dict = {
    'tecno': '#006B8B',
    'hp': '#0095d9',
    'acer': '#ff9900',
    'lenovo': '#E2232A',
    'apple': '#555555',
    'infinix': '#6600cc',
    'asus': '#00539b',
    'dell': '#009933',
    'samsung': '#1428A0',
    'msi': '#000000',
    'wings': '#ff9966',
    'ultimus': '#cc6600',
    'primebook': '#ffcc99',
    'iball': '#99cc00',
    'zebronics': '#ff99cc',
    'chuwi': '#cc33ff',
    'gigabyte': '#005DAA',
    'jio': '#ccff00',
    'honor': '#ff3399',
    'realme': '#ccff66',
    'avita': '#ffcc66',
    'microsoft': '#F25022',
    'fujitsu': '#ff9933',
    'lg': '#ccffcc',
    'walker': '#ffccff',
    'axl': '#ccff99'
}

# Add a sidebar with widgets
st.sidebar.title("Laptops")
st.sidebar.image('img/laptop_transparent.png',width=200)
st.sidebar.write("A collection of laptops sourced from the 'Smartprix' website.")
st.sidebar.write(" Here's a Dataset Overview... You Can Browse and Apply Custom Filters On the Data in Browse Laptops Page.")

# Create a sidebar navigation
st.page_link('Pages/Browse_Laptops.py',label='Browse Laptops')


st.write("# Overview")
# Add your content for Page 1 here

c1 , c2 ,c3 , c4 =st.columns(4)
colors = ['#ED1C24' , '#0f7dc2' , '#555555']
with c1:
    st.metric('Number of Brands 🧮',df['brand'].nunique())
with c2:
    st.metric('Number Of Laptops 💻',df['Model'].nunique())
with c3:
    st.metric('The most expensive laptop 🫰',df['Price'].max())
with c4:
    st.metric('The Cheapest laptop 👇',df['Price'].min())



#create columns for pie charts
st.header('                 ')
cp1,cp2 = st.columns(2)
with cp1:
    fig = px.pie(is_touch_screen, values='count', names='is_touch_screen', title='Touch Screen Laptops',hole=0.7, color_discrete_sequence=px.colors.sequential.Pinkyl_r)
    fig.update_layout(showlegend=False  ,    title=dict(font=dict(color='#fe3b3b') ))
    st.plotly_chart(fig,use_container_width=True)
with cp2 :
    fig = px.pie(operating_sys, values='count', names='OS', title='Opreating Systems',hole=0.7)
    fig.update_layout(showlegend=False  ,    title=dict(font=dict(color='#fe3b3b') ))
    st.plotly_chart(fig,use_container_width=True)


# Create two columns with equal width
col1, col2 = st.columns(2)

with col1:
    st.header("        ")
    fig = px.bar(laptops_per_brand, x='brand', y='Count', title='Number Of Laptops Per Brand',color= 'brand',color_discrete_map=brand_color_dict)
    fig.update_layout(showlegend=False  ,    title=dict(font=dict(color='#fe3b3b') ))
    st.plotly_chart(fig,use_container_width=True)

with col2:
    st.header("        ")
    # Display the bar chart
    fig = go.Figure(data=[go.Bar(x=avg_list, y=brands,orientation='h',marker=dict(color=colors))])
    fig.update_layout(title="Average Rating by Chip")
    fig.update_layout(showlegend=False ,  title=dict(font=dict(color='#fe3b3b') ))
    st.plotly_chart(fig,use_container_width=True)
        
st.header("        ")
x1 ,x2 = st.columns(2)
with x1:
    fig = px.bar(sorted_avg_price_by_brand, x='brand', y='Price', title='Avarage Price Per Brand',color= 'brand',color_discrete_map=brand_color_dict)
    fig.update_layout(showlegend=False  ,    title=dict(font=dict(color='#fe3b3b') ))
    st.plotly_chart(fig,use_container_width=True)
with x2 :
    fig = px.scatter(sorted_avg_Rating_by_brand, x='brand', y='Rating', title='Avarage Rating Per Brand',color= 'brand',color_discrete_map=brand_color_dict)
    fig.update_layout(showlegend=False  ,    title=dict(font=dict(color='#fe3b3b') ))

    st.plotly_chart(fig,use_container_width=True)
