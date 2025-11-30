import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Netflix App", layout="wide")

# 1. CONSUMO DE DATOS (Simulación API)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/SahilChachra/Netflix-Data-Visualization/master/netflix_titles.csv"
    df = pd.read_csv(url)
    df['date_added'] = pd.to_datetime(df['date_added'].str.strip(), errors='coerce')
    return df

df = load_data()

# 2. SIDEBAR Y FILTROS
st.sidebar.header("Filtros")
page = st.sidebar.radio("Navegación", ["Dashboard", "Datos", "Feedback"]) # Comp 1
pais = st.sidebar.multiselect("País", df['country'].value_counts().index[:10]) # Comp 2
anio = st.sidebar.slider("Año", 2000, 2021, (2015, 2021)) # Comp 3

# Lógica de Filtrado
data = df[(df['release_year'].between(anio[0], anio[1]))]
if pais: data = data[data['country'].str.contains('|'.join(pais), na=False)]

# 3. ESTRUCTURA PRINCIPAL
if page == "Dashboard":
    st.title("📊 Dashboard Netflix")
    
    # KPIs
    c1, c2, c3 = st.columns(3)
    c1.metric("Total", len(data)) # Comp 4
    c2.metric("Películas", len(data[data['type']=='Movie'])) # Comp 5
    c3.metric("Series", len(data[data['type']=='TV Show'])) # Comp 6

    tab1, tab2 = st.tabs(["Tendencias", "Detalles"]) # Comp 7

    with tab1: # Gráficos 1 y 2
        col_a, col_b = st.columns(2)
        with col_a:
            st.plotly_chart(px.pie(data, names='type', title="Películas vs Series"), use_container_width=True)
            st.info("Mayoría de contenido son películas.") # Interpretación
        with col_b:
            conteo_anio = data.groupby(data['date_added'].dt.year)['show_id'].count().reset_index()
            st.plotly_chart(px.area(conteo_anio, x='date_added', y='show_id', title="Evolución Temporal"), use_container_width=True)
            st.info("Crecimiento sostenido desde 2015.") # Interpretación

    with tab2: # Gráficos 3 y 4
        col_c, col_d = st.columns(2)
        with col_c:
            st.plotly_chart(px.bar(data['rating'].value_counts().head(), title="Top Ratings"), use_container_width=True)
        with col_d:
            st.plotly_chart(px.histogram(data[data['type']=='Movie'], x='duration', title="Duración"), use_container_width=True)
        st.success("El contenido para adultos (TV-MA) es el más frecuente.") # Interpretación

elif page == "Datos":
    st.title("📂 Datos Crudos")
    ver = st.checkbox("Ver todo") # Comp 8
    st.dataframe(data if ver else data.head(50)) # Comp 9
    st.download_button("Descargar CSV", data.to_csv(), "data.csv") # Comp 10

elif page == "Feedback":
    st.title("📝 Opinión")
    with st.form("f"): # Comp 11
        st.text_input("Nombre") # Comp 12
        st.form_submit_button("Enviar") # Comp 13