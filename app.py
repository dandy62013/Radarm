import streamlit as st
import pandas as pd
from supabase import create_client
import requests
import base64

def obtener_token_spotify():
    import requests
    import base64
    import streamlit as st

    client_id = st.secrets["SPOTIFY_CLIENT_ID"]
    client_secret = st.secrets["SPOTIFY_CLIENT_SECRET"]

    credenciales = f"{client_id}:{client_secret}"
    codificadas = base64.b64encode(
        credenciales.encode()
    ).decode()

    respuesta = requests.post(
        "https://accounts.spotify.com/api/token",
        headers={
            "Authorization": f"Basic {codificadas}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={"grant_type": "client_credentials"},
        timeout=15,
    )

    respuesta.raise_for_status()
    return respuesta.json()["access_token"]

st.set_page_config(
    page_title="MUSEM — Música emergente",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# DISEÑO MUSEM
# ─────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
    --rosa: #F3B1C5;
    --lavanda: #C9C3F5;
    --menta: #B5E5D8;
    --amarillo: #FFE8A3;
    --melocoton: #FFD0B5;
    --azul: #B9D7F8;
    --tinta: #393448;
    --crema: #FFFCF7;
}

.stApp {
    background:
        radial-gradient(ellipse at 0% 0%, #FCE8EE 0%, transparent 32%),
        radial-gradient(ellipse at 100% 8%, #EAE7FF 0%, transparent 30%),
        var(--crema);
    color: var(--tinta);
    font-family: 'DM Sans', sans-serif;
}

h1, h2, h3 {
    font-family: 'Manrope', sans-serif !important;
    color: var(--tinta);
    letter-spacing: -1px;
}

.block-container {
    padding-top: 1.8rem;
    padding-bottom: 4rem;
    max-width: 1250px;
}

header[data-testid="stHeader"] {
    background: transparent;
}

#MainMenu, footer {
    visibility: hidden;
}

.musem-logo {
    font-family: 'Manrope', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -2px;
    color: #51477C;
}

.musem-logo span {
    color: #E58AA8;
}

.musem-tag {
    color: #80788D;
    font-size: 0.76rem;
    letter-spacing: 2px;
    font-weight: 700;
    text-transform: uppercase;
}

.hero {
    background: linear-gradient(
        120deg,
        #F8DCE6 0%,
        #F5E5FA 48%,
        #E0EAFB 100%
    );
    border: 1px solid #FFFFFF;
    border-radius: 28px;
    padding: 42px 38px;
    margin: 18px 0 28px 0;
    position: relative;
    overflow: hidden;
}

.hero-kicker {
    font-size: 0.76rem;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #75618B;
    margin-bottom: 12px;
}

.hero-title {
    font-family: 'Manrope', sans-serif;
    font-size: clamp(2.1rem, 5vw, 3.7rem);
    font-weight: 800;
    line-height: 1.08;
    letter-spacing: -2px;
    color: #393448;
    max-width: 760px;
}

.hero-title span {
    color: #C66F96;
}

.hero-copy {
    color: #675D75;
    font-size: 1.05rem;
    line-height: 1.7;
    max-width: 620px;
    margin-top: 18px;
}

.hero-decoration {
    font-size: 3.5rem;
    margin-top: 18px;
    letter-spacing: 8px;
}

.section-kicker {
    color: #9B7A98;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 0.72rem;
    font-weight: 800;
    margin-bottom: 5px;
}

.role-card {
    border-radius: 22px;
    padding: 25px;
    min-height: 185px;
    border: 1px solid rgba(255,255,255,0.9);
}

.role-card h3 {
    margin: 10px 0 8px 0;
    font-size: 1.35rem;
}

.role-card p {
    color: #5E576A;
    line-height: 1.55;
    font-size: 0.93rem;
}

.role-artist {
    background: #F8E0E8;
}

.role-festival {
    background: #DDF2EA;
}

.role-discover {
    background: #FFF0C7;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 18px;
}

div[data-testid="stExpander"] {
    background: rgba(255,255,255,0.68);
    border: 1px solid #EDE5EE;
    border-radius: 16px;
    margin-bottom: 10px;
}

div[data-testid="stExpander"] summary {
    font-weight: 700;
}

.stTextInput input,
.stSelectbox div[data-baseweb="select"],
.stNumberInput input {
    border-radius: 12px;
}

.stTextInput input:focus {
    border-color: #C7B7ED;
    box-shadow: 0 0 0 1px #C7B7ED;
}

.stButton button,
.stFormSubmitButton button {
    border-radius: 14px;
    border: 1px solid #E6DCEC;
    background: #F0EAF9;
    color: #51477C;
    font-weight: 700;
    min-height: 43px;
    transition: all 0.2s ease;
}

.stButton button:hover,
.stFormSubmitButton button:hover {
    background: #E3D8F5;
    border-color: #C7B7ED;
    color: #393448;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #EEE5EC;
    border-radius: 15px;
    overflow: hidden;
}

hr {
    border-color: #EDE4EC;
}

.musem-footer {
    background: #F1EBF7;
    border-radius: 18px;
    padding: 22px;
    margin-top: 36px;
    text-align: center;
    color: #776D83;
    font-size: 0.85rem;
}

@media (max-width: 700px) {
    .hero {
        padding: 27px 22px;
    }
    .hero-title {
        letter-spacing: -1px;
    }
    .hero-decoration {
        font-size: 2.5rem;
    }
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# CABECERA Y PORTADA
# ─────────────────────────────────────────────

st.markdown("""
<div class="musem-logo">musem></div>
<div class="musem-tag">Nuevos sonidos. Nuevos escenarios.</div>

<div class="hero">
    <div class="hero-kicker">La música que viene</div>
    <div class="hero-title">
        El próximo nombre<br>
        de tu festival <span>está aquí.</span>
    </div>
    <div class="hero-copy">
        Descubre artistas emergentes, encuentra nuevos sonidos
        y conecta el talento con los escenarios donde merece estar.
    </div>
  
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="section-kicker">Un punto de encuentro</div>
<h2 style="margin-top:0;">La música conecta.</h2>
""", unsafe_allow_html=True)

col_artista, col_festival = st.columns(2, gap="medium")

with col_artista:
    st.markdown("""
    <div class="role-card role-artist">
        <div style="font-size:2rem;"></div>
        <h3>Para artistas</h3>
        <p>Un espacio para descubrir nuevos proyectos
        musicales y dar visibilidad al talento emergente.</p>
    </div>
    """, unsafe_allow_html=True)

with col_festival:
    st.markdown("""
    <div class="role-card role-festival">
        <div style="font-size:2rem;"></div>
        <h3>Para festivales</h3>
        <p>Explora propuestas musicales, encuentra nuevos
        nombres y descubre quién podría formar parte del cartel.</p>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# CONEXIÓN CON SUPABASE
# ─────────────────────────────────────────────

@st.cache_resource
def conectar_supabase():
    url = st.secrets["SUPABASE_URL"].strip().rstrip("/")
    key = st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)


try:
    supabase = conectar_supabase()
except Exception as e:
    st.error(f"No se pudo conectar con Supabase: {e}")
    st.stop()


# ─────────────────────────────────────────────
# ARTISTAS INICIALES
# ─────────────────────────────────────────────

ARTISTAS_INICIALES = [
    {
        "name": "Metrika", "city": "Castellón",
        "genre": "Urbano", "spotify": "", "instagram": "",
        "potential": 8, "favorite": False
    },
    {
        "name": "Gara Durán", "city": "Madrid",
        "genre": "Pop", "spotify": "", "instagram": "",
        "potential": 7, "favorite": False
    },
    {
        "name": "Teo Planell", "city": "Madrid",
        "genre": "Indie", "spotify": "", "instagram": "",
        "potential": 7, "favorite": False
    },
    {
        "name": "Alcalá Norte", "city": "Madrid",
        "genre": "Indie rock", "spotify": "", "instagram": "",
        "potential": 9, "favorite": False
    },
    {
        "name": "Julieta", "city": "Barcelona",
        "genre": "Pop urbano", "spotify": "", "instagram": "",
        "potential": 8, "favorite": False
    },
    {
        "name": "Barry B", "city": "Aranda de Duero",
        "genre": "Urbano", "spotify": "", "instagram": "",
        "potential": 8, "favorite": False
    },
    {
        "name": "Vera GRV", "city": "Almería",
        "genre": "Urbano", "spotify": "", "instagram": "",
        "potential": 7, "favorite": False
    },
    {
        "name": "céro", "city": "Sevilla",
        "genre": "Indie", "spotify": "", "instagram": "",
        "potential": 6, "favorite": False
    },
    {
        "name": "LUSILLON", "city": "Madrid",
        "genre": "Pop", "spotify": "", "instagram": "",
        "potential": 7, "favorite": False
    }
]


# ─────────────────────────────────────────────
# CARGAR ARTISTAS
# ─────────────────────────────────────────────

def cargar_artistas():
    respuesta = (
        supabase
        .table("artists")
        .select("*")
        .order("created_at", desc=False)
        .execute()
    )
    return respuesta.data


try:
    artistas = cargar_artistas()

    if len(artistas) == 0:
        supabase.table("artists").insert(
            ARTISTAS_INICIALES
        ).execute()
        artistas = cargar_artistas()

except Exception as e:
    st.error(f"No se pudieron cargar los artistas: {e}")
    st.stop()


# ─────────────────────────────────────────────
# EXPLORAR ARTISTAS
# ─────────────────────────────────────────────

st.divider()

st.markdown("""
<div class="section-kicker">Descubre tu próximo fichaje</div>
<h2 style="margin-top:0;">Explorar artistas 🎧</h2>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1.4, 1, 1])

with c1:
    search = st.text_input(
        "Buscar por nombre",
        placeholder="Ej. Metrika, Julieta..."
    )

with c2:
    genres = sorted(
        set((a.get("genre") or "Otro") for a in artistas)
    )
    genre = st.selectbox(
        "Género musical",
        ["Todos"] + genres
    )

with c3:
    min_score = st.slider(
        "Potencial mínimo",
        1, 10, 1
    )

favorites_only = st.checkbox("⭐ Mostrar solo favoritos")


# ─────────────────────────────────────────────
# FILTRAR ARTISTAS
# ─────────────────────────────────────────────

filtered = [
    a for a in artistas
    if search.lower() in (a.get("name") or "").lower()
    and (
        genre == "Todos"
        or (a.get("genre") or "Otro") == genre
    )
    and (a.get("potential") or 5) >= min_score
    and (
        not favorites_only
        or a.get("favorite", False)
    )
]

st.markdown(
    f"**{len(filtered)} artistas** encontrados"
)

if filtered:
    df = pd.DataFrame(filtered)
    df["favorite"] = df["favorite"].apply(
        lambda x: "⭐" if x else ""
    )

    st.dataframe(
        df[
            ["name", "city", "genre", "potential", "favorite"]
        ].rename(columns={
            "name": "Artista",
            "city": "Ciudad",
            "genre": "Género",
            "potential": "Potencial",
            "favorite": "Favorito"
        }),
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### Fichas de artistas")

    for artist in filtered:
        favorito = artist.get("favorite", False)

        with st.expander(
            f"{'⭐ ' if favorito else '🎵 '}"
            f"{artist['name']} · "
            f"{artist.get('genre') or 'Otro'}"
        ):
            info1, info2 = st.columns(2)

            with info1:
                st.write(
                    f"📍 **Ciudad:** "
                    f"{artist.get('city') or 'Sin especificar'}"
                )
                st.write(
                    f"🎶 **Género:** "
                    f"{artist.get('genre') or 'Otro'}"
                )

            with info2:
                st.write(
                    f"✨ **Potencial:** "
                    f"{artist.get('potential', 5)}/10"
                )

            if artist.get("spotify"):
                st.markdown(
                    f"[🎧 Escuchar en Spotify]({artist['spotify']})"
                )

            if artist.get("instagram"):
                st.markdown(
                    f"[📸 Ver Instagram]({artist['instagram']})"
                )

            if st.button(
                "Quitar de favoritos" if favorito
                else "Añadir a favoritos ⭐",
                key=f"fav_{artist['id']}"
            ):
                try:
                    supabase.table("artists").update(
                        {"favorite": not favorito}
                    ).eq("id", artist["id"]).execute()

                    st.rerun()

                except Exception as e:
                    st.error(
                        f"No se pudo actualizar el favorito: {e}"
                    )

else:
    st.info(
        "No hay artistas que coincidan con esos filtros. "
        "Prueba a cambiar los criterios de búsqueda."
    )


# ─────────────────────────────────────────────
# AÑADIR ARTISTA
# ─────────────────────────────────────────────

st.divider()

st.markdown("""
<div class="section-kicker">La escena está creciendo</div>
<h2 style="margin-top:0;">Añadir artista </h2>
<p style="color:#776D83;">
Incorpora un nuevo proyecto musical a tu radar.
</p>
""", unsafe_allow_html=True)

with st.form("new_artist", clear_on_submit=True):
    name = st.text_input("Nombre del artista *")
    city = st.text_input("Ciudad")

    new_genre = st.selectbox(
        "Género musical",
        [
            "Indie", "Pop", "Rock", "Electrónica",
            "Urbano", "Hip-hop", "Flamenco",
            "Reggaetón", "Otro"
        ]
    )

    spotify = st.text_input("Enlace de Spotify (opcional)")
    instagram = st.text_input("Enlace de Instagram (opcional)")

    score = st.slider("Potencial estimado", 1, 10, 5)

    submitted = st.form_submit_button("Guardar artista ✨")


if submitted:
    if not name.strip():
        st.error("Escribe el nombre del artista.")

    elif any(
        (a.get("name") or "").lower() == name.strip().lower()
        for a in artistas
    ):
        st.warning("Ese artista ya está en la lista.")

    else:
        nuevo = {
            "name": name.strip(),
            "city": city.strip(),
            "genre": new_genre,
            "spotify": spotify.strip(),
            "instagram": instagram.strip(),
            "potential": score,
            "favorite": False
        }

        try:
            supabase.table("artists").insert(nuevo).execute()
            st.success(
                f"¡{name.strip()} ya forma parte de MUSEM!"
            )
            st.rerun()

        except Exception as e:
            st.error(f"No se pudo guardar el artista: {e}")


# ─────────────────────────────────────────────
# PIE DE PÁGINA
# ─────────────────────────────────────────────

st.markdown("""
<div class="musem-footer">
    <div style="font-size:1.35rem;font-weight:800;color:#51477C;">
        musem<span style="color:#E58AA8;">✳</span>
    </div>
    Nuevos sonidos. Nuevos escenarios.<br>
    <span style="font-size:0.75rem;">
        Prototipo en desarrollo
    </span>
</div>
""", unsafe_allow_html=True)


with st.expander("Explorar Spotify"):
    nombre_spotify = st.text_input(
        "Buscar artista en Spotify",
        placeholder="Ej. Alcalá Norte"
    )

    if st.button("Buscar en Spotify"):
        if not nombre_spotify.strip():
            st.warning("Escribe un nombre.")
        else:
            try:
                token = obtener_token_spotify()
                respuesta = requests.get(
                    "https://api.spotify.com/v1/search",
                    headers={"Authorization": f"Bearer {token}"},
                    params={
                        "q": nombre_spotify.strip(),
                        "type": "artist",
                        "limit": 1
                    },
                    timeout=15,
                )
                respuesta.raise_for_status()
                artistas_spotify = respuesta.json()["artists"]["items"]

                if not artistas_spotify:
                    st.info("No se encontraron artistas.")
                for artista in artistas_spotify:
                    st.write(artista["name"])
                    st.write(artista["external_urls"]["spotify"])
            except Exception as e:
                st.error(f"Error en la búsqueda: {e}")
