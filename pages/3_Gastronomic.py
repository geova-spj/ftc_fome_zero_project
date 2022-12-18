#====================================================================================================
# BIBLIOTECAS
#====================================================================================================

import pandas as pd
import numpy as np
import inflection
import folium
from folium.plugins import MarkerCluster
from matplotlib import pyplot as plt
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import streamlit as st
from streamlit_folium import folium_static


#====================================================================================================
# FUNÇÕES
#====================================================================================================

# Renomear e padronizar as colunas

def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new

    return df

# Nomear os países por meio do código

COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}

def country_name(country_id):
    return COUNTRIES[country_id]

# Categorizar os intervalos de preço

def create_price_tye(price_range):
    if price_range == 1:
        return "Cheap"
    elif price_range == 2:
        return "Normal"
    elif price_range == 3:
        return "Expensive"
    else:
        return "Gourmet"

# Nomear as colunas por meio de código
COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}

def color_name(color_code):
    return COLORS[color_code]

#====================================================================================================
# CARREGANDO ARQUIVO
#====================================================================================================

df = pd.read_csv('zomato.csv')

#====================================================================================================
# ORGANIZAÇÃO E LIMPEZA
#====================================================================================================

data = df.copy()

# Renomeando os arquivos
data = rename_columns(data)

# Criação de colunas
data['country'] = data.loc[:,'country_code'].apply(lambda x: country_name(x))
data['price_type'] = data.loc[:, 'price_range'].apply(lambda x: create_price_tye(x))
data['color'] = data.loc[:, 'rating_color'].apply(lambda x: color_name(x))

# Pegando apenas o primeiro elemento do tipo de cozinha
data = data.loc[data['cuisines'].notnull(), :]
data['cuisines'] = data.loc[:, 'cuisines'].astype(str).apply(lambda x: x.split(',')[0])

# Removendo colunas desnecessárias
data = data.drop(columns = ['country_code','locality_verbose', 'switch_to_order_menu','rating_color'])

# Removendo dados duplicados
data = data.drop_duplicates(subset='restaurant_id', keep='first')
data = data.loc[data['average_cost_for_two'] != 0, :]

# Resetando o index
data = data.reset_index(drop = True)

#====================================================================================================
# SIDEBAR - Topo
#====================================================================================================

st.set_page_config(layout="wide", page_icon=":knife_fork_plate:")

st.header ('🍽️ Gastronomic Background')

# Barra Lateral: Cabeçalho - Logo e nome da empresa
image_path = 'fome_zero_logo_new.png'
image = Image.open(image_path)
st.sidebar.image(image)

st.sidebar.markdown ("<h3 style='text-align: center; color: red;'> World Gastronomic Best Experiences</h3>", unsafe_allow_html=True)
st.sidebar.markdown ('''___''')

#====================================================================================================
# FILTROS SIDEBAR
#====================================================================================================

st.sidebar.markdown ('# Filtros')

# País
paises = list (data['country'].unique())
country_options = st.sidebar.multiselect('Selecione os países: ', paises, default = paises)

#---------------------------------------------------------
# Habilidatação dos filtros
#---------------------------------------------------------

# Filtro País

linhas = data['country'].isin(country_options)
data = data.loc[linhas, :]

#====================================================================================================
# SIDEBAR - Final
#====================================================================================================
st.sidebar.markdown ('''___''')
st.sidebar.markdown ('###### Powered by Comunidade DS')
st.sidebar.markdown ('###### Data Analyst: Geová Silvério')
#====================================================================================================
# Layout - Visão país
#====================================================================================================

with st.container():
    
    st.markdown('### As 10 culinárias mais ofertadas')
    st.text('Quantidade de restaurantes a ofertar a culinária')
    
    contagem = data[['cuisines', 'restaurant_id']].groupby('cuisines').count().sort_values('restaurant_id', ascending = False).reset_index().head(10)
    contagem.columns=['Gastronomia', 'Qt. Restaurantes']

    fig = px.funnel(contagem, x='Qt. Restaurantes', y='Gastronomia', color='Gastronomia', template='plotly_white')
    fig.update(layout_showlegend=False)

    st.plotly_chart(fig, use_container_width = True, theme='streamlit')
    

with st.container():
    
    col1, col2= st.columns(2)
    
    with col1:
        
        st.markdown('#### As 10 culinárias pior avaliadas')
        
        contagem = data[['cuisines', 'aggregate_rating']].groupby('cuisines').mean().sort_values('aggregate_rating', ascending = True).reset_index().head(10)
        contagem.columns=['Gastronomia', 'Avaliação Média']

        plt.figure(figsize = (12,5))
        fig = px.bar(contagem, x='Gastronomia', y='Avaliação Média', template='plotly_white',
                     color ='Avaliação Média', color_continuous_scale='YlGnBu', text='Avaliação Média')
        fig.update(layout_coloraxis_showscale=False)
        fig.update_traces(textangle=0, texttemplate='%{text:.2f}')
    
        st.plotly_chart(fig, use_container_width = True, theme='streamlit')
        
    with col2:
        
        st.markdown('#### As 10 culinárias mais bem avaliadas')
        
        contagem = data[['cuisines', 'aggregate_rating']].groupby('cuisines').mean().sort_values('aggregate_rating', ascending = False).reset_index().head(10)
        contagem.columns=['Gastronomia', 'Avaliação Média']

        plt.figure(figsize = (12,5))
        fig = px.bar(contagem, x='Gastronomia', y='Avaliação Média', template='plotly_white',
                     color ='Avaliação Média', color_continuous_scale='YlGnBu', text='Avaliação Média')
        fig.update(layout_coloraxis_showscale=False)
        fig.update_traces(textangle=0, texttemplate='%{text:.2f}')

        st.plotly_chart(fig, use_container_width = True, theme='streamlit')
        

with st.container():
    
    col1,col2 = st.columns(2)
    
    with col1:
        
        st.markdown('#### 20 Culinárias mais caras e pior avaliadas')
        st.text('Price Type: Expensive or Gourmet e Aggregate Rating <= 2.5')

        linhas= ((data['price_type'] == 'Expensive') | (data['price_type'] == 'Gourmet')) & (data['aggregate_rating'] <= 2.5)
        df1 = data.loc[linhas, ['cuisines', 'aggregate_rating']].groupby('cuisines').mean().sort_values('aggregate_rating', ascending=True).reset_index().head(20)
        df1.columns=['Culinárias', 'Avaliação Média']
        st.dataframe(df1.style.format(subset='Avaliação Média', formatter="{:.2f}"))
       
        
    with col2:
        
        st.markdown('#### 20 Culinárias mais baratas e melhor avaliadas')
        st.text('Price Type: Cheap or Normal e Aggregate Rating >=4 ')
        
        
        linhas= ((data['price_type'] == 'Normal') | (data['price_type'] == 'Cheap')) & (data['aggregate_rating'] >= 4)
        df1 = data.loc[linhas, ['cuisines', 'aggregate_rating']].groupby('cuisines').mean().sort_values('aggregate_rating', ascending=False).reset_index().head(20)
        df1.columns=['Culinárias', 'Avaliação Média']
        st.dataframe(df1.style.format(subset='Avaliação Média', formatter="{:.2f}"))
        
        
    
        
    
        
        
        
        
        
        
        
        
        
        