
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st

# --------------------------------------------------
# Configuración general
# --------------------------------------------------

st.set_page_config(
    page_title="SONIA | Orquestación Conversacional Inteligente",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

DB_PATH = Path(__file__).parent / "sonia_clicks.db"

FOREST = "#0E311F"
MINT = "#DDF4ED"
TURQUOISE = "#3FD0D5"
NIGHT = "#01111D"
SNOW = "#F5FFF9"

# --------------------------------------------------
# Estilos visuales
# --------------------------------------------------

st.markdown(
    f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

        html, body, [class*="css"] {{
            font-family: 'DM Sans', sans-serif;
        }}

        .stApp {{
            background-color: {SNOW};
            color: {NIGHT};
        }}

        #MainMenu, footer, header {{
            visibility: hidden;
        }}

        .block-container {{
            max-width: 1120px;
            padding-top: 1.5rem;
            padding-bottom: 3rem;
        }}

        .brand {{
            font-size: 1.55rem;
            font-weight: 700;
            color: {FOREST};
            letter-spacing: -0.8px;
        }}

        .brand span {{
            color: {TURQUOISE};
        }}

        .eyebrow {{
            color: {FOREST};
            font-weight: 700;
            font-size: 0.82rem;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 1rem;
        }}

        .hero {{
            background: {MINT};
            border-radius: 24px;
            padding: 3.5rem 3rem;
            margin-top: 1.2rem;
            margin-bottom: 2rem;
        }}

        .hero h1 {{
            color: {FOREST};
            font-size: clamp(2.5rem, 5vw, 4.5rem);
            line-height: 1.05;
            letter-spacing: -2px;
            margin: 0 0 1.4rem 0;
        }}

        .hero p {{
            color: {NIGHT};
            font-size: 1.15rem;
            line-height: 1.8;
            max-width: 690px;
        }}

        .section-title {{
            color: {FOREST};
            font-size: 2rem;
            font-weight: 700;
            letter-spacing: -0.8px;
            margin-top: 2.4rem;
            margin-bottom: 0.8rem;
        }}

        .section-copy {{
            font-size: 1.05rem;
            line-height: 1.8;
            color: {NIGHT};
        }}

        .info-card {{
            background: white;
            border: 1px solid #dce9e2;
            border-radius: 18px;
            padding: 1.5rem;
            min-height: 190px;
            height: 100%;
        }}

        .info-card h3 {{
            color: {FOREST};
            font-size: 1.15rem;
            margin-top: 0.5rem;
            margin-bottom: 0.7rem;
        }}

        .info-card p {{
            color: {NIGHT};
            line-height: 1.65;
            font-size: 0.97rem;
        }}

        .icon {{
            font-size: 1.8rem;
        }}

        .cta {{
            background: {FOREST};
            border-radius: 22px;
            color: {SNOW};
            padding: 2.5rem;
            margin-top: 2.5rem;
            margin-bottom: 1.5rem;
        }}

        .cta h2 {{
            color: {SNOW};
            font-size: 2rem;
            margin-bottom: 0.8rem;
        }}

        .cta p {{
            color: {MINT};
            font-size: 1.05rem;
            line-height: 1.7;
        }}

        div.stButton > button {{
            background: {TURQUOISE};
            color: {NIGHT};
            border: none;
            border-radius: 999px;
            padding: 0.8rem 1.5rem;
            font-weight: 700;
            min-height: 3rem;
            transition: opacity 0.2s ease;
        }}

        div.stButton > button:hover {{
            background: {TURQUOISE};
            color: {NIGHT};
            opacity: 0.85;
            border: none;
        }}

        .footer {{
            border-top: 1px solid #dce9e2;
            padding-top: 1.3rem;
            margin-top: 3rem;
            color: #52665c;
            font-size: 0.88rem;
        }}

        @media (max-width: 700px) {{
            .hero {{
                padding: 2rem 1.4rem;
                border-radius: 18px;
            }}

            .hero h1 {{
                letter-spacing: -1px;
            }}

            .cta {{
                padding: 1.6rem;
            }}
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Registro de interés
# --------------------------------------------------

def save_click():
    """Registra el clic en Supabase si está configurado.
    Si no, usa SQLite local para pruebas.
    """
    timestamp = datetime.now(timezone.utc).isoformat()

    # Opción recomendada para despliegue: Supabase
    try:
        supabase_url = st.secrets["SUPABASE_URL"].rstrip("/")
        supabase_key = st.secrets["SUPABASE_KEY"]

        import requests

        response = requests.post(
            f"{supabase_url}/rest/v1/early_adopter_clicks",
            headers={
                "apikey": supabase_key,
                "Authorization": f"Bearer {supabase_key}",
                "Content-Type": "application/json",
                "Prefer": "return=minimal",
            },
            json={"clicked_at": timestamp},
            timeout=8,
        )
        response.raise_for_status()
        return True, "supabase"

    except KeyError:
        # Supabase aún no está configurado.
        pass
    except Exception:
        # Si Supabase está configurado pero falla, no ocultamos
        # el error diciendo que el registro fue exitoso.
        return False, "error"

    # Modo local: útil para probar en tu computadora.
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS early_adopter_clicks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    clicked_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                "INSERT INTO early_adopter_clicks (clicked_at) VALUES (?)",
                (timestamp,),
            )
        return True, "local"
    except Exception:
        return False, "error"


# --------------------------------------------------
# Encabezado
# --------------------------------------------------

left, right = st.columns([3, 1])

with left:
    st.markdown(
        f'<div class="brand">SONIA<span>.</span></div>',
        unsafe_allow_html=True,
    )

with right:
    st.markdown(
        "<div style='text-align:right;padding-top:8px;color:#0E311F;'>"
        "IA conversacional para empresas</div>",
        unsafe_allow_html=True,
    )

# --------------------------------------------------
# Hero
# --------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">Orquestación conversacional inteligente</div>
        <h1>Tus conversaciones.<br>Mejor conectadas.</h1>
        <p>
            SONIA busca transformar la atención al cliente en una experiencia
            más fluida, organizada e inteligente. Una solución de IA pensada
            para ayudar a las pequeñas y medianas empresas a gestionar sus
            conversaciones y dedicar más tiempo a lo que realmente importa.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Problema
# --------------------------------------------------

st.markdown(
    '<div class="section-title">Cada conversación importa.</div>',
    unsafe_allow_html=True,
)
st.markdown(
    """
    <div class="section-copy">
        Responder consultas, hacer seguimiento de oportunidades y mantener
        una atención consistente puede consumir tiempo y dispersar información.
        SONIA nace para explorar una manera más inteligente de organizar
        esas interacciones sin perder la cercanía humana.
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

# --------------------------------------------------
# Propuesta de valor
# --------------------------------------------------

st.markdown(
    '<div class="section-title">¿Qué busca hacer SONIA?</div>',
    unsafe_allow_html=True,
)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        """
        <div class="info-card">
            <div class="icon">💬</div>
            <h3>Conversaciones organizadas</h3>
            <p>
                Ayudar a gestionar consultas y dar continuidad a las
                interacciones con clientes.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        """
        <div class="info-card">
            <div class="icon">🧠</div>
            <h3>Inteligencia contextual</h3>
            <p>
                Utilizar IA para interpretar consultas y responder teniendo
                en cuenta el contexto disponible.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        """
        <div class="info-card">
            <div class="icon">🤝</div>
            <h3>Un trato más humano</h3>
            <p>
                Facilitar la atención sin perder de vista la transparencia,
                el control y la intervención humana.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --------------------------------------------------
# Cómo funciona
# --------------------------------------------------

st.markdown(
    '<div class="section-title">Menos fragmentación. Más continuidad.</div>',
    unsafe_allow_html=True,
)
st.markdown(
    """
    <div class="section-copy">
        La propuesta de SONIA es integrar inteligencia conversacional en los
        procesos de atención y ventas. Su alcance se encuentra en desarrollo:
        queremos validar con empresas reales qué problemas son prioritarios
        y qué funcionalidades aportan mayor valor.
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Early Adopter
# --------------------------------------------------

st.markdown(
    """
    <div class="cta">
        <h2>Ayudanos a construir SONIA.</h2>
        <p>
            Estamos explorando esta propuesta y queremos conocer el interés
            de empresas que podrían beneficiarse de una mejor gestión de sus
            conversaciones. Sumate como early adopter y ayudanos a validar
            qué debería resolver SONIA.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

if st.button("Quiero sumarme como early adopter", use_container_width=True):
    success, storage = save_click()

    if success:
        st.info(
            "¡Gracias por tu interés! El programa Early Adopter todavía "
            "no está habilitado. Registramos tu interés para ayudar a "
            "validar la demanda por SONIA."
        )
        if storage == "local":
            st.caption(
                "Modo de prueba: el registro está guardado localmente y "
                "no es una métrica persistente en Streamlit Cloud."
            )
    else:
        st.warning(
            "Gracias por tu interés. En este momento no pudimos registrar "
            "el clic. Podés volver a intentarlo más tarde."
        )

# --------------------------------------------------
# Pie de página
# --------------------------------------------------

st.markdown(
    """
    <div class="footer">
        <strong>SONIA</strong> · Orquestación Conversacional Inteligente
        <br>
        Una propuesta en desarrollo para mejorar la gestión de conversaciones
        entre empresas y clientes.
    </div>
    """,
    unsafe_allow_html=True,
)