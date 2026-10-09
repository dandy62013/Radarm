
import streamlit as st
import pandas as pd
from supabase import create_client

st.set_page_config(page_title="Festival Radar", page_icon="🎪", layout="wide")
st.title("🎪 Festival Radar")
st.caption("Tu radar de talento para festivales.")

@st.cache_resource
def conectar_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

try:
    supabase = conectar_supabase()
    st.success("Base de datos conectada")
except Exception as e:
    st.error("No se pudo conectar con Supabase. Revisa los Secrets.")
    st.stop()

def cargar_artistas():
    respuesta = supabase.table("artists").select("*").order("created_at", desc=True).execute()
    return respuesta.data

st.subheader("🔎 Buscar artistas")
try:
    artistas = cargar_artistas()

except Exception as e:
    st.error(f"Error al cargar artistas: {e}")
    st.stop()

busqueda = st.text_input("Buscar por nombre")
generos = sorted({a.get("genre") or "Otro" for a in artistas})
genero = st.selectbox("Género", ["Todos"] + generos)
minimo = st.slider("Potencial mínimo", 1, 10, 1)
solo_favoritos = st.checkbox("⭐ Solo favoritos")

filtrados = [
    a for a in artistas
    if busqueda.lower() in (a.get("name") or "").lower()
    and (genero == "Todos" or (a.get("genre") or "Otro") == genero)
    and (a.get("potential") or 5) >= minimo
    and (not solo_favoritos or a.get("favorite", False))
]

st.write(f"**{len(filtrados)} artistas encontrados**")

for artista in filtrados:
    with st.expander(f"{'⭐ ' if artista.get('favorite') else ''}{artista['name']} · Potencial {artista.get('potential') or 5}/10"):
        st.write("📍 Ciudad:", artista.get("city") or "Sin especificar")
        st.write("🎵 Género:", artista.get("genre") or "Otro")
        if artista.get("spotify"):
            st.markdown(f"[Abrir Spotify]({artista['spotify']})")
        if artista.get("instagram"):
            st.markdown(f"[Abrir Instagram]({artista['instagram']})")
        if st.button("Quitar favorito" if artista.get("favorite") else "Añadir a favoritos", key=f"fav_{artista['id']}"):
            supabase.table("artists").update(
                {"favorite": not artista.get("favorite", False)}
            ).eq("id", artista["id"]).execute()
            st.rerun()

st.divider()
st.subheader("➕ Añadir artista")

with st.form("nuevo_artista", clear_on_submit=True):
    nombre = st.text_input("Nombre del artista *")
    ciudad = st.text_input("Ciudad")
    genero_nuevo = st.selectbox(
        "Género musical",
        ["Indie", "Pop", "Rock", "Electrónica", "Urbano", "Hip-hop", "Flamenco", "Reggaetón", "Otro"]
    )
    spotify_link = st.text_input("Enlace de Spotify (opcional)")
    instagram_link = st.text_input("Enlace de Instagram (opcional)")
    potencial = st.slider("Potencial estimado", 1, 10, 5)
    guardar = st.form_submit_button("Guardar artista")

if guardar:
    if not nombre.strip():
        st.error("Escribe el nombre del artista.")
    else:
        try:
            supabase.table("artists").insert({
                "name": nombre.strip(),
                "city": ciudad.strip(),
                "genre": genero_nuevo,
                "spotify": spotify_link.strip(),
                "instagram": instagram_link.strip(),
                "potential": potencial,
                "favorite": False
            }).execute()
            st.success("¡Artista guardado permanentemente!")
            st.rerun()
        except Exception:
            st.error("No se pudo guardar. Comprueba los permisos de la tabla en Supabase.")

st.caption("Las puntuaciones son estimaciones manuales; verifica los datos antes de contratar.")
