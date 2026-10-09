
import streamlit as st
import pandas as pd
from supabase import create_client

st.set_page_config(
    page_title="Festival Radar",
    page_icon="🎪",
    layout="wide"
)

st.title("🎪 Festival Radar")
st.caption("Descubre artistas para tu próximo cartel.")


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
        "name": "Metrika",
        "city": "Castellón",
        "genre": "Urbano",
        "spotify": "",
        "instagram": "",
        "potential": 8,
        "favorite": False
    },
    {
        "name": "Gara Durán",
        "city": "Madrid",
        "genre": "Pop",
        "spotify": "",
        "instagram": "",
        "potential": 7,
        "favorite": False
    },
    {
        "name": "Teo Planell",
        "city": "Madrid",
        "genre": "Indie",
        "spotify": "",
        "instagram": "",
        "potential": 7,
        "favorite": False
    },
    {
        "name": "Alcalá Norte",
        "city": "Madrid",
        "genre": "Indie rock",
        "spotify": "",
        "instagram": "",
        "potential": 9,
        "favorite": False
    },
    {
        "name": "Julieta",
        "city": "Barcelona",
        "genre": "Pop urbano",
        "spotify": "",
        "instagram": "",
        "potential": 8,
        "favorite": False
    },
    {
        "name": "Barry B",
        "city": "Aranda de Duero",
        "genre": "Urbano",
        "spotify": "",
        "instagram": "",
        "potential": 8,
        "favorite": False
    },
    {
        "name": "Vera GRV",
        "city": "Almería",
        "genre": "Urbano",
        "spotify": "",
        "instagram": "",
        "potential": 7,
        "favorite": False
    },
    {
        "name": "céro",
        "city": "Sevilla",
        "genre": "Indie",
        "spotify": "",
        "instagram": "",
        "potential": 6,
        "favorite": False
    },
    {
        "name": "LUSILLON",
        "city": "Madrid",
        "genre": "Pop",
        "spotify": "",
        "instagram": "",
        "potential": 7,
        "favorite": False
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


# ─────────────────────────────────────────────
# IMPORTACIÓN INICIAL
# ─────────────────────────────────────────────

try:
    artistas = cargar_artistas()

    if len(artistas) == 0:
        supabase.table("artists").insert(ARTISTAS_INICIALES).execute()
        artistas = cargar_artistas()

except Exception as e:
    st.error(f"No se pudieron cargar los artistas: {e}")
    st.stop()


# ─────────────────────────────────────────────
# BUSCADOR Y FILTROS
# ─────────────────────────────────────────────

st.subheader("🔎 Explorar artistas")

c1, c2, c3 = st.columns(3)

with c1:
    search = st.text_input("Buscar por nombre")

with c2:
    genres = sorted(
        set((a.get("genre") or "Otro") for a in artistas)
    )

    genre = st.selectbox(
        "Género",
        ["Todos"] + genres
    )

with c3:
    min_score = st.slider(
        "Potencial mínimo",
        1,
        10,
        1
    )


favorites_only = st.checkbox(
    "⭐ Mostrar solo favoritos"
)


# ─────────────────────────────────────────────
# FILTRAR
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


st.write(
    f"**{len(filtered)} artistas encontrados**"
)


# ─────────────────────────────────────────────
# TABLA
# ─────────────────────────────────────────────

if filtered:

    df = pd.DataFrame(filtered)

    df["favorite"] = df["favorite"].apply(
        lambda x: "⭐" if x else ""
    )

    st.dataframe(
        df[
            [
                "name",
                "city",
                "genre",
                "potential",
                "favorite"
            ]
        ].rename(
            columns={
                "name": "Artista",
                "city": "Ciudad",
                "genre": "Género",
                "potential": "Potencial",
                "favorite": "Favorito"
            }
        ),
        use_container_width=True,
        hide_index=True
    )


    # ─────────────────────────────────────────
    # FICHAS
    # ─────────────────────────────────────────

    st.subheader("🎧 Fichas de artistas")

    for artist in filtered:

        favorito = artist.get(
            "favorite",
            False
        )

        with st.expander(
            f"{'⭐ ' if favorito else ''}"
            f"{artist['name']} · "
            f"Potencial {artist.get('potential', 5)}/10"
        ):

            st.write(
                f"📍 Ciudad: "
                f"{artist.get('city') or 'Sin especificar'}"
            )

            st.write(
                f"🎵 Género: "
                f"{artist.get('genre') or 'Otro'}"
            )

            if artist.get("spotify"):
                st.markdown(
                    f"[Abrir Spotify]"
                    f"({artist['spotify']})"
                )

            if artist.get("instagram"):
                st.markdown(
                    f"[Abrir Instagram]"
                    f"({artist['instagram']})"
                )


            if st.button(
                "Quitar favorito"
                if favorito
                else "Añadir a favoritos",
                key=f"fav_{artist['id']}"
            ):

                try:

                    supabase.table(
                        "artists"
                    ).update(
                        {
                            "favorite": not favorito
                        }
                    ).eq(
                        "id",
                        artist["id"]
                    ).execute()

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"No se pudo actualizar "
                        f"el favorito: {e}"
                    )

else:

    st.info(
        "No hay artistas que coincidan "
        "con esos filtros."
    )


# ─────────────────────────────────────────────
# AÑADIR ARTISTA
# ─────────────────────────────────────────────

st.divider()

st.subheader("➕ Añadir artista")


with st.form(
    "new_artist",
    clear_on_submit=True
):

    name = st.text_input(
        "Nombre del artista *"
    )

    city = st.text_input(
        "Ciudad"
    )

    new_genre = st.selectbox(
        "Género musical",
        [
            "Indie",
            "Pop",
            "Rock",
            "Electrónica",
            "Urbano",
            "Hip-hop",
            "Flamenco",
            "Reggaetón",
            "Otro"
        ]
    )

    spotify = st.text_input(
        "Enlace de Spotify (opcional)"
    )

    instagram = st.text_input(
        "Enlace de Instagram (opcional)"
    )

    score = st.slider(
        "Potencial estimado",
        1,
        10,
        5
    )

    submitted = st.form_submit_button(
        "Guardar artista"
    )


if submitted:

    if not name.strip():

        st.error(
            "Escribe el nombre del artista."
        )

    elif any(
        a["name"].lower() == name.strip().lower()
        for a in artistas
    ):

        st.warning(
            "Ese artista ya está en la lista."
        )

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

            supabase.table(
                "artists"
            ).insert(
                nuevo
            ).execute()

            st.success(
                f"¡{name.strip()} guardado "
                f"permanentemente!"
            )

            st.rerun()

        except Exception as e:

            st.error(
                f"No se pudo guardar el artista: {e}"
            )


st.caption(
    "Festival Radar · Prototipo en desarrollo"
)
