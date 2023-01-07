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

# Limpeza e organização

def clean_code(df):
    
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
    
    return data

# Gráfico de barras

def bar_graph (data, x, y, color, text):
    
    plt.figure(figsize = (20,15))
    fig = px.bar(data, x=x, y=y, template='plotly_white', color=color,
           color_continuous_scale='YlGnBu', text=text)
    fig.update(layout_showlegend=False)
    fig.update_traces(textangle=0, textposition='outside')
    
    return fig

# Gráfico treemap

def treemap_graph(data, path, value, color):
    
    fig = px.treemap(data, path=[path], values=value, color = color, color_continuous_scale = 'RdBu',
           template ='plotly_white')
    fig.data[0].texttemplate = "<b>%{label}</b><br>Qt. Culinárias: %{value}<br>"
    
    return fig

#====================================================================================================
# CARREGANDO ARQUIVO E FAZENDO LIMPEZA
#====================================================================================================

df = pd.read_csv('zomato.csv')

data = clean_code(df)

#====================================================================================================
# SIDEBAR - Topo
#====================================================================================================

st.set_page_config(layout='wide', page_icon=':earth_africa:')
                   
st.header ('🌎 Country Background')

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
    
    st.markdown('### Quantidade de restaurantes por país')
    
    contagem = data[['restaurant_id', 'country']].groupby('country').count().sort_values('restaurant_id', ascending = True).reset_index()
    contagem.columns = ['Países', 'Qt. Restaurantes']

    fig = bar_graph(contagem, x='Países', y='Qt. Restaurantes', color='Países', text='Qt. Restaurantes')
    st.plotly_chart(fig, use_container_width = True, theme='streamlit')
    
with st.container():
    
    st.markdown('### Quantidade de cidades por país')
    
    contagem = data[['city', 'country']].groupby('country').nunique().sort_values('city', ascending = True).reset_index()
    contagem.columns = ['Países', 'Qt. Cidades']

    fig = bar_graph(contagem, x='Países', y='Qt. Cidades', color='Países', text='Qt. Cidades')
    st.plotly_chart(fig, use_container_width = True, theme='streamlit')

with st.container():
    
    col1, col2 = st.columns(2)
    
    with col1:
        
        st.markdown('#### Diversidade Gastronômica: ')
        st.markdown('###### Quantidade de culinárias únicas por país')
        
        contagem = data[['country','cuisines']].groupby('country').nunique().sort_values('cuisines', ascending = False).reset_index()
        contagem.columns=['País','Culinárias']

        fig = treemap_graph(contagem, path='País', value='Culinárias', color='Culinárias')
        st.plotly_chart(fig, use_container_width = True, theme='streamlit')
         
    with col2:
        
        st.markdown('#### Top 5 Países com maior quantitativo de avaliações')
        
        contagem = data[['country', 'votes']].groupby('country').sum().sort_values('votes', ascending = False).reset_index().head(5)
        contagem.columns = ['Países', 'Qt. Avaliações (Milhões)']
        
        fig= bar_graph(contagem, x='Qt. Avaliações (Milhões)', y='Países', color='Países', text='Qt. Avaliações (Milhões)')
        fig.update_traces(textposition=None)
        st.plotly_chart(fig, use_container_width = True, theme='streamlit')
        
with st.container():
    
    col1, col2 = st.columns(2)
    
    with col1:
        
        st.markdown('#### Avaliação média por país')
        
        contagem = data[['country', 'aggregate_rating']].groupby('country').mean().sort_values('aggregate_rating', ascending = True).reset_index()
        contagem.columns=['Países', 'Média das Avaliações']

        fig = bar_graph (contagem, x='Países', y='Média das Avaliações', color ='Países', text='Média das Avaliações')
        fig.update_traces(textangle=0, textposition='inside', texttemplate='%{text:.2f}')
        st.plotly_chart(fig, use_container_width = True, theme='streamlit')

    with col2:
   
        st.markdown('#### Média de custo e de avaliação dos países')
    
        df1 = data.loc[:, ['country', 'average_cost_for_two', 'aggregate_rating']].groupby('country').mean().sort_values('average_cost_for_two',ascending = False).reset_index()

        df2 = data.drop_duplicates(subset='country', keep='first')
        df2 = df2[['country','currency']].reset_index(drop=True)

        df3 = pd.merge(df2, df1, how = 'inner')
        df3 = df3.sort_values('average_cost_for_two', ascending = False).reset_index(drop = True)
        df3.columns = ['País', 'Moeda', 'Preço Médio - Prato p/2', 'Avaliação Média']

        st.dataframe(df3.style.format(subset=['Preço Médio - Prato p/2', 'Avaliação Média'], formatter="{:.2f}"))
