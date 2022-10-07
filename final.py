# Cargar librerias
import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base64
import geojson
# Configuraciones de la pagina
st.set_page_config(page_title="Turismo en Bogotá", page_icon="https://www.shd.gov.co/plantillas/images/logo-bogota.png", initial_sidebar_state="expanded", menu_items={"About":"DashBoard sobre la actualidad turistica de Bogotá, generado para al clase de Analitica I, UdeA 2022-1. Grupo: Dayan Marin, Vladimir Martin"},layout="wide")


#se cargan las bases de datos, para algunas se hace necesario especificar el separador y el encoding.
rnt_1=pd.read_csv('rnt_1.csv')
rnt_2=pd.read_csv('rnt_2.csv')
rnt_3=pd.read_csv('rnt_3.csv')
rnt_u1 = pd.concat([rnt_1, rnt_2])
rnt=pd.concat([rnt_u1,rnt_3])
arpro = pd.read_csv('areas_protegidas_1.csv', sep = ';')
teatro = pd.read_csv('teatrosyauditorios_3.csv',encoding='latin-1',sep=";")
museos = pd.read_csv('museos_5.csv',encoding='latin-1',sep=";")
centros = pd.read_csv('centrosculturalesartisticos_7.csv',encoding='latin-1',sep=";")
salacine = pd.read_csv('salascinecinematecas_6.csv',encoding='latin-1',sep=";")
salaexpo = pd.read_csv('salasexposiciongalerias_4.csv',encoding='latin-1',sep=";")
avion = pd.read_csv("pasajeros.csv",encoding='latin-1',sep=";")
avion_int = pd.read_csv("pasajeros_int.csv",encoding='latin-1',sep=";")
comidas = pd.read_csv('comidas_bog.csv',encoding='latin-1',sep=",")
# importar geojson
with open('Area Protegida.geojson') as f:
  gj_com = geojson.load(f)
#CREACION COLUMNA PARA DISCRIMINAR
teatro["PLAN"] = "Teatros y Auditorios"
museos["PLAN"] = "Museos"
centros["PLAN"] = "Centros Culturales y Artisticos"
salacine["PLAN"] = "Salas de Cine y Cinematecas"
salaexpo["PLAN"] = "Salas de Exposiciones y Galerias"
#se crea base de datos unida
db_unida = pd.concat([salaexpo, salacine, centros,museos,teatro]) 

#cambiar formato a fecha
rnt["ANO"]=pd.to_datetime(rnt["ANO"],format='%Y')
rnt["MES"]=pd.to_datetime(rnt["MES"],format="%m")

#remplazo valores nulos por la leyenda "NO TIENE"
rnt["RAZON_SOCIAL_ESTABLECIMIENTO"].fillna("NO TIENE", inplace=True)

#CREAR COLUMNA CON MES EN NOMBRE
rnt["MES_N"]=rnt['MES'].dt.strftime('%B')


#se remplazan comas por puntos, como separador decimal
arpro["SHAPE_AREA"]=arpro["SHAPE_AREA"].str.replace(",",".")
arpro["SHAPE_LEN"]=arpro["SHAPE_LEN"].str.replace(",",".")
#se remplaza valor mal escrito
arpro["TIPO"]=arpro["TIPO"].replace(["Parque Ecologico Distrital de Monta??a"],"Parque Ecologico Distrital de Montaña")


#Se eliminan columnas que no aportan al analisis
centros=centros.drop(['LECCONTACTO', "LECESTADO","LECTELEFON","LECEMAIL","LECPAGWEB","LECANIO"], axis=1)


#Se eliminan columnas que no aportan al analisis
museos=museos.drop(['LECPAGWEB', "LECEMAIL","LECCODSEC","LECNOMSEC","LECCONTACTO","LECANIO"], axis=1)

#Se eliminan columnas que no aportan al analisis
salacine=salacine.drop(['LECPAGWEB', "LECEMAIL","LECCODSEC","LECNOMSEC","LECCONTACTO","LECANIO","LECTELEFON","LECCODUPZ","LECNOMUPZ","LECESTADO"], axis=1)


#Se eliminan columnas que no aportan al analisis
salaexpo=salaexpo.drop(['LECESTADO', "LECCONTACTO","LECANIO"], axis=1)


#Se detecta una misma localidad escrita de 2 formas diferentes, se remplaza
teatro['LECNOMLOC']=teatro['LECNOMLOC'].replace(["USAQUÉN"],"USAQUEN")

teatro=teatro.drop(['LECESTADO', "LECCONTACTO"], axis=1)


#CSS style tag para apariencias de la pagina, los data-testid se encuentran mediante las devtools del navegador. tutorial: https://www.youtube.com/watch?v=pyWqw5yCNdo
page_bg_img="""
<style>
[data-testid="stAppViewContainer"]{
    background-image: url("https://i.imgur.com/RxSYZvG.jpeg");
background-size:cover;
    }
[data-testid="stHeader"]{
    background-color: rgba(0,0,0,0);
background-size:cover;
    }
[data-testid="stToolbar"]{
    right:2rem;
    }
[data-testid="stSidebar"]{
    background-image: url("https://i.imgur.com/WYMnjGX.jpeg");
background-size:cover;
# =============================================================================
# [data-testid="stSidebar"]>div:first-child{{
#     background-image: url("data:image/png;base64,{img}");
# background-size:cover;
# =============================================================================
    }}
</style>
"""


#Cambiar apariencia de la pagina
st.markdown(page_bg_img,unsafe_allow_html=True)

c1, c2, c3, c4, c5= st.columns((1,1,1,1,1)) 

c3.image("https://www.shd.gov.co/plantillas/images/logo-bogota.png")

#Crear Sidebar
with st.sidebar:   
    st.markdown("<h1 style='text-align: center; color: #e4032e;'>EL TURISMO EN CIFRAS", unsafe_allow_html=True)

# Título principal
st.markdown("<h1 style='text-align: center; color: #e4032e;'>🏙️Panorama Turistico de Bogotá🏙️</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: #fab62d;'>🗺️¿Que puedo hacer en la Ciudad?🗺️ </h2>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: #fab62d;'> </h2>", unsafe_allow_html=True)

##CREACION DEL DATASET DE REGISTROS TURISTICOS
rnt_dep=rnt.groupby(["DEPARTAMENTO"])[["CODIGO_RNT"]].count().rename(columns={"CODIGO_RNT":"REGISTROS"}).reset_index().sort_values('REGISTROS',ascending=False)
rnt_dep_f=rnt_dep[rnt_dep["REGISTROS"]>20000].reset_index(drop=True).set_index("DEPARTAMENTO")
##CREACION DEL DATAFRAME PASAJEROS NACIONALES AVION 
avion=avion.sort_values('PASAJEROS',ascending=False).reset_index(drop=True).replace({'BOGOTç, D. C.':"BOGOTA DC","BOLêVAR":"BOLIVAR","ARCHIPI\x83LAGO DE SAN ANDR\x83S, PROVIDENCIA Y SANTA CATALINA":"SAN ANDRES"})
avion=avion.head(6).set_index("DEPARTAMENTO")
##CREACION DE DATAFRAME PASAJEROS INTERNACIONALES AVION
avion_int["DEPARTAMENTO"].unique()
avion_int=avion_int.sort_values('PASAJEROS',ascending=False).reset_index(drop=True).replace({"ATLçNTICO":"ATLANTICO",'BOGOTç, D. C.':"BOGOTA DC","BOLêVAR":"BOLIVAR","ARCHIPI\x83LAGO DE SAN ANDR\x83S, PROVIDENCIA Y SANTA CATALINA":"SAN ANDRES"})
avion_int=avion_int.head(6).set_index("DEPARTAMENTO")

#CARGAR TABLAs A SIDEBAR
with st.sidebar: 
    st.markdown("<h2 style= color: #fab62d;'>Negocios registrados para turismo", unsafe_allow_html=True)    
    st.write(rnt_dep_f)
    st.markdown("<h2 style= color: #fab62d;'>Entradas Nacionales de pasajeros por ✈️ Año 2021", unsafe_allow_html=True)    
    st.write(avion) 
    st.markdown("<h2 style= color: #fab62d;'>Entradas Internacionales de pasajeros por ✈️ Año 2021", unsafe_allow_html=True)    
    st.write(avion_int) 

#grafica ubicacion por departamento
# =============================================================================
st.markdown("<h2 style='text-align: center; color: #646363;'>🌐Departamentos con mayor numero de registros de empresas de turismo", unsafe_allow_html=True)
c1,c2=st.columns((4,6))
#creacion del dataset
rnt_dep=rnt.groupby(["DEPARTAMENTO"])[["CODIGO_RNT"]].count().rename(columns={"CODIGO_RNT":"REGISTROS"}).reset_index().sort_values('REGISTROS',ascending=False)
rnt_dep_f=rnt_dep[rnt_dep["REGISTROS"]>20000]
#grafica
# crear gráfica:
rnt_dep_fig = px.pie(rnt_dep_f , values = 'REGISTROS', names = 'DEPARTAMENTO')

# agregar detalles a la gráfica:
rnt_dep_fig.update_layout(
    template = 'ggplot2',
    legend_title = 'DEPARTAMENTOS',
    title_x = 0.5,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)')

c2.plotly_chart(rnt_dep_fig)
c1.markdown("<h1 style='text-align: center;'<br> </h1>", unsafe_allow_html= True)
c1.image("https://pbs.twimg.com/media/ELmHWGsX0AAyRbZ.jpg",width=600)



#prestadores de servicios turisticos
# =============================================================================
st.markdown("<h2 style='text-align: center; color: #646363;'>🖊️Tipos de negocio registados para turismo en la Ciudad", unsafe_allow_html=True)
c4,c5= st.columns((7,6))
#se genera el dataframe
rnt_bog=rnt[rnt["DEPARTAMENTO"].str.contains("BOGOTA")]
rnt_cat=rnt_bog.groupby(["CATEGORIA"])[["CODIGO_RNT"]].count().reset_index().rename(columns={"CODIGO_RNT":"LUGARES"}).sort_values('LUGARES',ascending=False)
#se modifica para hacerlo amigable al grafico
rnt_cat["CATEGORIA"]=rnt_cat["CATEGORIA"].replace({"ESTABLECIMIENTOS DE ALOJAMIENTO TURISTICO":"ALOJAMIENTO TURISTICO","ESTABLECIMIENTO DE GASTRONOMIA Y SIMILARES":"GASTRONOMIA Y SIMILARES","OPERADORES PROFESIONALES DE CONGRESOS FERIAS Y CONVENCIONES":"OPERADORES DE CONGRESOS FER Y CONVENCI","OFICINAS DE REPRESENTACION TURISTICA":"OF REPRESENTACION TURISTICA","OTROS TIPOS DE HOSPEDAJE TURISTICOS NO PERMANENTES":"HOSPEDAJE TURISTICOS TEMP",
                                                        "EMPRESA DE TRANSPORTE TERRESTRE AUTOMOTOR":"TRANSPORTE TERRESTRE AUTO","ARRENDADORES DE VEHICULOS PARA TURISMO NACIONAL E INTERNACIONAL":"ARRENDADORES DE VEHICULOS","EMPRESA DE TIEMPO COMPARTIDO Y MULTIPROPIEDAD":"TIEMPO COMPARTIDO","EMPRESAS CAPTADORAS DE AHORRO PARA VIAJES":"AHORRO PARA VIAJES","COMPANIA DE INTERCAMBIO VACACIONAL":"INTERCAMBIO VACACIONAL","CONCESIONARIOS DE SERVICIOS TURISTICOS EN PARQUE":"SERVICIOS TURISTICOS EN PARQUE",
                                                         "USUARIOS INDUSTRIALES DE SERVICIOS TURISTICOS EN ZONAS FRANCAS":"SERV TURISTICOS EN ZONAS FRANCAS","OPERADORES PROFESIONALES DE CONGRESOS FERIAS Y CONVENCIONES":"OPERADORES DE CONGRESOS"})
# se crea la grafica
rnt_cat_fig = px.bar(rnt_cat, x='CATEGORIA', y='LUGARES')
rnt_cat_fig.update_layout(
    xaxis_title = 'Categorias',
    yaxis_title = 'Cantidad',
    template = 'simple_white',
    title_x = 0.2,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)')

c4.plotly_chart(rnt_cat_fig)


c5.image("https://bogota.gov.co/sites/default/files/styles/1050px/public/field/image/Recorrido-turistico.jpg",caption="Recorridos Turisticos en el barrio la Candelaria",width=700)
 

#reservas naturales de la Ciudad
# =============================================================================
st.markdown("<h2 style='text-align: center; color: #646363;'>🏞️Reservas Naturales de la Ciudad", unsafe_allow_html=True)
c4,c5= st.columns((6,7))
#creacion del dataframe
arpro_tipo=arpro.groupby(["TIPO"])[["NOMBRE"]].count().reset_index().rename(columns={"NOMBRE":"CANTIDAD"})
#Se corrige error en una categoria
arpro_tipo["TIPO"]=arpro_tipo["TIPO"].replace("Parque Ecologico Distrital de Monta??a","Parque Ecologico Distrital de Montaña")
#se saca el total de areas protegicas
total_arpro=arpro["TIPO"].count()
c5.markdown("<h4 style='text-align: center; color: #646363;'>Porcentajes por Tipo de Reserva", unsafe_allow_html=True)
# elaborar el grafico
arpro_tipo_fig = px.pie(arpro_tipo , values = 'CANTIDAD', names = 'TIPO', template = 'ggplot2',
             hole = .5)
# poner detalles a la gráfica
arpro_tipo_fig.update_layout(    
    title_x = 0.5,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    annotations = [dict(text = str(total_arpro), x=0.5, y = 0.5, font_size = 40, showarrow = False )],
    legend=dict(orientation="h",
                yanchor="bottom",
                y=-0.3,
                xanchor="left",
                x=0))

c5.plotly_chart(arpro_tipo_fig)
c4.image("https://contenidos.civico.com/wp-content/uploads/2014/03/sumapaz-ex_magician.jpg",caption="Páramo Natural de Sumapaz",width=600)

#mapa areas protegidas
token_map = "pk.eyJ1IjoidmxhZGlnb3NwZWwiLCJhIjoiY2w4YW95aXNmMDdjejN1bWh2bjNkYjNqMyJ9.ScoXk60DLIaoYQq-uXNU3w"
px.set_mapbox_access_token(token_map)
#generar grafico
fig = px.choropleth_mapbox(arpro, # dataframe que tiene el indicador
              geojson = gj_com, # archivo json con el shape
              color = 'TIPO', # columna que contiene el indicador: valor sobre el cual se va dar la tonalidad del color
              locations = 'NOMBRE', # llave del dataframe para hacer el join con el shape
              featureidkey = 'properties.NOMBRE', # llave del shape para hacer el join con el dataframe
              hover_name = 'NOMBRE', # información que se va a observar cuando se pase el cursor por el poligono
              center = {'lat':4.29, 'lon':-74.21}, # centro en el cual se va ubicar el mapa (en este caso centroíde de Medellin)
              zoom = 7.9, # zoom de la imagen
              mapbox_style="streets",
              opacity=0.5)
fig.update_layout(    
    title_x = 0.5,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    margin={"r":0,"t":0,"l":0,"b":0},
    legend=dict(orientation="h",
                yanchor="bottom",
                y=-0.1,
                xanchor="left",
                x=0))
      
fig.update_geos(fitbounds = 'locations', visible = False) # ajustar a los limites del shape
st.plotly_chart(fig,use_container_width=True)

#planes por localidad
# =============================================================================
st.markdown("<h2 style='text-align: center; color: #646363;'>🚶‍♂️Planes en Bogotá por localidad", unsafe_allow_html=True)
#creacion del dataframe
db_unida_loc=db_unida.groupby(["LECNOMLOC","PLAN"])[["LECCODIGO"]].count().reset_index().rename(columns={"LECNOMLOC":"LOCALIDAD","LECCODIGO":"CANTIDAD"}).sort_values(by='CANTIDAD', ascending=False)
# se crea la grafica
db_unida_loc_fig = px.bar(db_unida_loc, x='LOCALIDAD', y='CANTIDAD',color="PLAN",template = 'plotly_dark')
db_unida_loc_fig.update_layout(
    xaxis_title = '<b>Localidad<b>',
    yaxis_title = "<b># de Planes<b>",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    title_x = 0.2,
    font_size = 16)
st.plotly_chart(db_unida_loc_fig,use_container_width=True)

#Galerias por zona
# =============================================================================
st.markdown("<h2 style='text-align: center; color: #646363;'>🖼️Galerias de Arte y Salas de exposiciones", unsafe_allow_html=True)
c1,c2=st.columns((6,4))
#creando el dataframe
salaexpo_gen=salaexpo.groupby(["LECNOMUPZ","LECCLASIF"])[["LECCODIGO"]].count().reset_index().rename(columns={"LECCLASIF":"TIPO","LECNOMUPZ":"ZONA-UPZ","LECCODIGO":"CANTIDAD"}).sort_values('CANTIDAD',ascending=False)
salaexpo_gen_fig = px.bar(salaexpo_gen, x='ZONA-UPZ', y='CANTIDAD',template = 'plotly_dark',color="TIPO",barmode="stack")
salaexpo_gen_fig.update_layout(
    xaxis_title = '<b>Zona-UPZ<b>',
    yaxis_title = '<b>Cantidad<b>',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    title_x = 0.2,
    legend=dict(orientation="h",
                yanchor="top",
                y=1.1,
                xanchor="left",
                x=0))
c1.plotly_chart(salaexpo_gen_fig,use_container_width=True)
c2.image("https://cloudfront-us-east-1.images.arcpublishing.com/semana/SDYMMOXJJZEORETXTBZOJ5AKSE.jpg",caption="Galeria BETA",width=650)
#Cines por Marca
# =============================================================================
st.markdown("<h2 style='text-align: center; color: #646363;'>🎬Cines y Cinematecas", unsafe_allow_html=True)
c1,c2=st.columns((4,6))
#Creacion del dataframe
salacine_tot=salacine.groupby(["LECCLASIF"])[["LECCODIGO"]].count().reset_index().rename(columns={"LECCODIGO":"CANTIDAD","LECCLASIF":"MARCA"}).sort_values('CANTIDAD',ascending=False)
# se crea la grafica
salacine_tot_fig = px.bar(salacine_tot, x='MARCA', y='CANTIDAD',template = 'plotly_dark')
salacine_tot_fig.update_layout(
    xaxis_title = '<b>Marca<b>',
    yaxis_title = '<b>Cantidad<b>',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    title_x = 0.2)
c2.plotly_chart(salacine_tot_fig,use_container_width=True)
c1.image("https://www.eltiempo.com/files/image_640_428/uploads/2019/06/11/5d0031291de28.jpeg",caption="Cinemateca de Bogotá",width=500)

#mapa de comidas
# =============================================================================
#se agrega nueva base de datos de comida
st.markdown("<h2 style= 'text-align: center; color: #646363;'>🍝Ubicacion de sitios de comida en la Ciudad", unsafe_allow_html=True)
comidas=comidas.rename(columns={"amenity":"Tipo","name":"Nombre","cuisine":"Especialidad"})
comidas["Especialidad"]=comidas["Especialidad"].replace({'friture':"Comidas Rapidas", 'coffee_shop':"Cafe", 'regional':"Regional", 'burger':"Comidas Rapidas", 'heladeria':"Helados",
       'bread':"Panaderia", 'ice_cream':"Helados", 'panaderia':"Panaderia", 'chinese':"Comida China",
       'coffee_shop;juice;sandwiches;beer':"Cafe Bar",
       'coffee_shop;sandwich;mexican;regional':"Mexicana", 'coffee;bakery;juice':"Cafe",
       'coffee_shop;regional':"Cafe", 'CafÃ©_de_orÃ\xadgen':"Cafe", 'international':"Internacional",
       'cafeteria':"Cafe", 'spanish':"Española", 'pasteleria':"Pasteleria", 'Chocolate_shop':"Cafe", 'donut':"Pasteleria",
       'sandwich; coffee_shop':"Cafe", 'Postres':"Pasteleria", 'kebab':"Arabe", 'Pan':"Panaderia",})
comidas["Especialidad"]=comidas["Especialidad"].fillna("Varios")
comidas.loc[comidas["Especialidad"].str.contains("coffee_shop"),"Especialidad"]="Cafe"
token_map = "pk.eyJ1IjoidmxhZGlnb3NwZWwiLCJhIjoiY2w4dG44MGg5MDU5NzNvbzV6enIydXNsayJ9.qEL2CzwXjYhsrDroi9mi1w"
px.set_mapbox_access_token(token_map)
# generar mapa
mapa_1=px.scatter_mapbox(comidas, 
                  lat = 'latitude', lon = 'longitude', 
                  color ='Tipo',
                  hover_name = 'Tipo',
                  hover_data=["Nombre", "Especialidad"], 
                  mapbox_style  = 'streets',
                  color_continuous_scale = px.colors.cyclical.IceFire, size_max = 30, zoom = 10,
                  template = 'simple_white',
                  width=1200,
                  height=600)
mapa_1.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    legend_font_size=16,
    font_size = 50,
    legend=dict(orientation="h",
                yanchor="bottom",
                y=-0.1,
                xanchor="left",
                x=0))

st.plotly_chart(mapa_1,use_container_width=True) 





#cargar iamgen desde local
# =============================================================================
# from PIL import Image
# image = Image.open("/Users/Vlado/Documents/universidad/9_sem/Analitica/dash_board_final/image.jpg")
# 
# st.image(image, caption='Bogotá')
# =============================================================================

#importar imagen de disco local
# =============================================================================
# @st.experimental_memo
# def get_img_as_base64(file):
#     with open(file,"rb")as f:
#         data = f.read()
#     return base64.b64encode(data).decode()
# img=get_img_as_base64("image.jpg")
# =============================================================================






