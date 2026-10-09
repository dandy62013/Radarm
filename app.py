
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Festival Radar", page_icon="🎪", layout="wide")

st.title("🎪 Festival Radar")
st.subheader("Radar de talento para festivales de España")
st.write("Descubre artistas, compara estilos y encuentra talento emergente.")

if "artistas" not in st.session_state:
    st.session_state.artistas = [
        {"Artista": "Metrika", "Ciudad": "Castellón", "Género": "Urbano"},
        {"Artista": "Gara Durán", "Ciudad": "", "Género": "Pop"},
        {"Artista": "Teo Planell", "Ciudad": "Madrid", "Género": "Alternativo"},
        {"Artista": "Alcalá Norte", "Ciudad": "Madrid", "Género": "Indie / rock"},
        {"Artista": "Julieta", "Ciudad": "", "Género": "Pop electrónico"},
        {"Artista": "Barry B", "Ciudad": "Aranda de Duero", "Género": "Alternativo"},
        {"Artista": "Vera GRV", "Ciudad": "Almería", "Género": "Urbano"},
        {"Artista": "céro", "Ciudad": "Sevilla", "Género": "Pop / urbano"},
        {"Artista": "LUSILLON", "Ciudad": "Madrid", "Género": "Pop alternativo"},
    ]

df = pd.DataFrame(st.session_state.artistas)
busqueda = st.text_input("🔎 Buscar artista, ciudad o género")
generos = ["Todos"] + sorted(df["Género"].unique().tolist())
genero = st.selectbox("Filtrar por género", generos)

if busqueda:
    df = df[df.astype(str).apply(
        lambda fila: fila.str.contains(busqueda, case=False).any(), axis=1
    )]

if genero != "Todos":
    df = df[df["Género"] == genero]

st.metric("Artistas en pantalla", len(df))
st.dataframe(df, use_container_width=True, hide_index=True)

st.divider()
st.subheader("➕ Añadir artista")
with st.form("nuevo_artista"):
    nombre = st.text_input("Nombre artístico")
    ciudad = st.text_input("Ciudad")
    estilo = st.text_input("Género musical")
    guardar = st.form_submit_button("Añadir a la sesión")

if guardar:
    if nombre.strip():
        st.session_state.artistas.append({
            "Artista": nombre.strip(),
            "Ciudad": ciudad.strip(),
            "Género": estilo.strip() or "Sin clasificar"
        })
        st.success("Artista añadido durante esta sesión.")
        st.rerun()
    else:
        st.warning("Escribe el nombre del artista.")

st.caption("MVP en pruebas. Los datos deben verificarse; los artistas añadidos aún no se guardan de forma permanente.")
