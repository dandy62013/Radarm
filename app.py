

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Festival Radar", page_icon="🎪", layout="wide")

st.title("🎪 Festival Radar")
st.caption("Descubre artistas para tu próximo cartel.")

if "artists" not in st.session_state:
    st.session_state.artists = [
        {"Artista": "Metrika", "Ciudad": "Castellón", "Género": "Urbano", "Spotify": "", "Instagram": "", "Potencial": 8, "Favorito": False},
        {"Artista": "Gara Durán", "Ciudad": "Madrid", "Género": "Pop", "Spotify": "", "Instagram": "", "Potencial": 7, "Favorito": False},
        {"Artista": "Teo Planell", "Ciudad": "Madrid", "Género": "Indie", "Spotify": "", "Instagram": "", "Potencial": 7, "Favorito": False},
        {"Artista": "Alcalá Norte", "Ciudad": "Madrid", "Género": "Indie rock", "Spotify": "", "Instagram": "", "Potencial": 9, "Favorito": False},
        {"Artista": "Julieta", "Ciudad": "Barcelona", "Género": "Pop urbano", "Spotify": "", "Instagram": "", "Potencial": 8, "Favorito": False},
        {"Artista": "Barry B", "Ciudad": "Aranda de Duero", "Género": "Urbano", "Spotify": "", "Instagram": "", "Potencial": 8, "Favorito": False},
        {"Artista": "Vera GRV", "Ciudad": "Almería", "Género": "Urbano", "Spotify": "", "Instagram": "", "Potencial": 7, "Favorito": False},
        {"Artista": "céro", "Ciudad": "Sevilla", "Género": "Indie", "Spotify": "", "Instagram": "", "Potencial": 6, "Favorito": False},
        {"Artista": "LUSILLON", "Ciudad": "Madrid", "Género": "Pop", "Spotify": "", "Instagram": "", "Potencial": 7, "Favorito": False},
    ]

artists = st.session_state.artists

st.subheader("🔎 Explorar artistas")
c1, c2, c3 = st.columns(3)

with c1:
    search = st.text_input("Buscar por nombre")
with c2:
    genres = sorted(set(a["Género"] for a in artists))
    genre = st.selectbox("Género", ["Todos"] + genres)
with c3:
    min_score = st.slider("Potencial mínimo", 1, 10, 1)

favorites_only = st.checkbox("⭐ Mostrar solo favoritos")

filtered = [
    a for a in artists
    if search.lower() in a["Artista"].lower()
    and (genre == "Todos" or a["Género"] == genre)
    and a["Potencial"] >= min_score
    and (not favorites_only or a["Favorito"])
]

st.write(f"**{len(filtered)} artistas encontrados**")

if filtered:
    df = pd.DataFrame(filtered)
    st.dataframe(
        df[["Artista", "Ciudad", "Género", "Potencial", "Favorito"]],
        use_container_width=True,
        hide_index=True
    )

    st.subheader("🎧 Fichas de artistas")
    for artist in filtered:
        with st.expander(f"{'⭐ ' if artist['Favorito'] else ''}{artist['Artista']} · Potencial {artist['Potencial']}/10"):
            st.write(f"📍 Ciudad: {artist['Ciudad']}")
            st.write(f"🎵 Género: {artist['Género']}")
            if artist["Spotify"]:
                st.markdown(f"[Abrir Spotify]({artist['Spotify']})")
            if artist["Instagram"]:
                st.markdown(f"[Abrir Instagram]({artist['Instagram']})")
            if st.button("Quitar favorito" if artist["Favorito"] else "Añadir a favoritos", key=f"fav_{artist['Artista']}"):
                artist["Favorito"] = not artist["Favorito"]
                st.rerun()
else:
    st.info("No hay artistas que coincidan con esos filtros.")

st.divider()
st.subheader("➕ Añadir artista")

with st.form("new_artist", clear_on_submit=True):
    name = st.text_input("Nombre del artista *")
    city = st.text_input("Ciudad")
    new_genre = st.selectbox(
        "Género musical",
        ["Indie", "Pop", "Rock", "Electrónica", "Urbano", "Hip-hop", "Flamenco", "Reggaetón", "Otro"]
    )
    spotify = st.text_input("Enlace de Spotify (opcional)")
    instagram = st.text_input("Enlace de Instagram (opcional)")
    score = st.slider("Potencial estimado", 1, 10, 5)
    submitted = st.form_submit_button("Guardar artista")

    if submitted:
        if not name.strip():
            st.error("Escribe el nombre del artista.")
        elif any(a["Artista"].lower() == name.strip().lower() for a in artists):
            st.warning("Ese artista ya está en la lista.")
        else:
            artists.append({
                "Artista": name.strip(),
                "Ciudad": city.strip() or "Sin especificar",
                "Género": new_genre,
                "Spotify": spotify.strip(),
                "Instagram": instagram.strip(),
                "Potencial": score,
                "Favorito": False
            })
            st.success(f"¡{name.strip()} añadido!")
            st.rerun()

st.caption("Prototipo en desarrollo · Verifica los datos y las puntuaciones antes de contratar artistas.")
