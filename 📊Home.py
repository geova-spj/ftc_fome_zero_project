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
import streamlit as st
from streamlit_folium import folium_static
from streamlit_option_menu import option_menu

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
st.set_page_config(page_title='Home',
                   layout="wide",
                   page_icon=':bar_chart:')

st.header ('Fome Zero')
st.header ('O Melhor lugar para encontrar seu mais novo restaurante favorito!')

st.subheader ('Temos as seguintes marcas dentro da nossa plataforma:')


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
# Layout - Visão Home
#====================================================================================================

    
    
with st.container():
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        
        
        contagem = data['restaurant_id'].nunique()
        col1.metric('Restaurantes Cadastrados', value = contagem)
        
        
        contagem = data.loc[data['has_table_booking'] == 1,:].shape[0]
        col1.metric('Restaurantes que aceitam reserva', value = contagem)
        
    with col2:
        
        
        contagem = data.loc[data['has_online_delivery'] == 1,:].shape[0]
        col2.metric('Restaurantes com pedido online', value = contagem)

        
        contagem = data.loc[data['is_delivering_now'] == 1,:].shape[0]
        col2.metric('Restaurantes que fazem entrega', value = contagem)

    with col3:
        
        
        contagem = data['country'].nunique()
        col3.metric('Países Cadastrados', value = contagem)
    
        contagem = data['city'].nunique()
        col3.metric('Cidades Cadastradas', value = contagem)
        
    with col4:
        
        contagem = data['cuisines'].nunique()
        col4.metric('Culinárias Ofertadas', value = contagem)
        
        contagem = data['votes'].sum()
        col4.metric('Avaliações feitas na plataforma', value = contagem)


with st.container():

    # Armazenamento dos dados

    datamapa = data[['restaurant_name', 'longitude', 'latitude', 'cuisines', 'average_cost_for_two', 'currency', 'aggregate_rating', 'color']].reset_index(drop = True)

    # Criando o mapa
    mapa = folium.Map(zoom_start = 15)

    #Criando os clusters
    cluster = MarkerCluster().add_to(mapa)

    icon = 'fa-cutlery'

    #Colocando os pinos
    for index, location_info in datamapa.iterrows():
        folium.Marker([location_info['latitude'],       
                       location_info['longitude']],
                       icon = folium.Icon(color=location_info['color'], icon=icon, prefix='fa'),
                       popup = folium.Popup(f"""<h6> <b> {location_info['restaurant_name']} </b> </h6> <br>
                                            Cozinha: {location_info['cuisines']} <br>
                                            Preço médio para dois: {location_info['average_cost_for_two']} ({location_info['currency']}) <br>
                                            Avaliação: {location_info['aggregate_rating']} / 5.0 <br> """,
                                            max_width= len(f"{location_info['restaurant_name']}")*20)).add_to(cluster)

    # Exibindo o mapa
    folium_static(mapa, width = 1024, height = 600)
        

with st.container():
    
   
    st.markdown('#### Top 10 restaurantes')
    
    df1 = data[['restaurant_id', 'restaurant_name', 'country', 'city', 'cuisines', 'currency', 'average_cost_for_two', 'aggregate_rating', 'votes']].sort_values(['aggregate_rating', 'restaurant_id'], ascending = [False, True]).reset_index(drop=True).head(10)
    df1.columns=['ID','Nome','País','Cidade','Culinária', 'Moeda', 'Preço Médio - Prato p/2', 'Avaliação Média', 'Qt. Votos']
    st.dataframe(df1.style.format(subset=['Preço Médio - Prato p/2', 'Avaliação Média'], formatter="{:.2f}"))
        
        
        
    
        
    
        
        
        
        
        
        
        
        
        
        
