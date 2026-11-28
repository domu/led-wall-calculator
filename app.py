import streamlit as st
from novastar_catalog import (
    get_recommended_controller,
    calculate_panel_pixels,
)

st.set_page_config(
    page_title="LED Wall Calculator",
    page_icon="📺",
    layout="wide",
)

# ── Sidebar: configurazione pannelli ────────────────────────────────
with st.sidebar:
    st.title("⚙️ Specifiche Pannello")
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        panel_width_mm = st.number_input(
            "Larghezza pannello (mm)",
            min_value=100,
            value=960,
            step=10,
            help="Dimensione base del singolo pannello in millimetri",
        )
    with col2:
        panel_height_mm = st.number_input(
            "Altezza pannello (mm)",
            min_value=100,
            value=640,
            step=10,
            help="Dimensione altezza del singolo pannello in millimetri",
        )

    pixel_pitch = st.number_input(
        "Pixel Pitch (mm)",
        min_value=0.5,
        max_value=100.0,
        value=2.5,
        step=0.5,
        help="Distanza tra due pixel adiacenti (pixel pitch) in millimetri",
    )

    panels_base = st.number_input(
        "N° pannelli di base (orizzontale)",
        min_value=1,
        value=4,
        step=1,
        help="Quanti pannelli affiancati sull'asse orizzontale",
    )
    panels_height = st.number_input(
        "N° pannelli in altezza (verticale)",
        min_value=1,
        value=3,
        step=1,
        help="Quanti pannelli impilati sull'asse verticale",
    )

    st.markdown("---")
    st.info(
        "💡 I calcoli vengono aggiornati automaticamente. "
        "Il prodotto è basato sui dati tipici del catalogo NovaStar."
    )
    st.markdown(
        "[Davide Pedretti Biagioni - 2026](https://linktr.ee/davide.pedrettibiagioni)"
    )


# ── Pagina principale: risultati ────────────────────────────────────
st.title("📐 LED Wall Calculator")
st.caption("Dimensionamento LED wall con configurazione hardware NovaStar")

# ── Sezione 1: Specifiche pannello ─────────────────────────────
st.header("🔧 Specifiche del Pannello")
col_p1, col_p2, col_p3 = st.columns(3)
with col_p1:
    st.metric("Larghezza pannello", f"{panel_width_mm} mm")
with col_p2:
    st.metric("Altezza pannello", f"{panel_height_mm} mm")
with col_p3:
    st.metric("Pixel Pitch", f"{pixel_pitch} mm")

# ── Sezione 2: Calcolo pixel per pannello ───────────────────────
st.header("📊 Pixel per Pannello")
w_px, h_px = calculate_panel_pixels(panel_width_mm, panel_height_mm, pixel_pitch)
panel_pixels_total = w_px * h_px

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Pixel in larghezza", f"{w_px} px")
with c2:
    st.metric("Pixel in altezza", f"{h_px} px")
with c3:
    st.metric("Totali per pannello", f"{panel_pixels_total:,}")
with c4:
    st.metric("Risoluzione", f"{w_px} × {h_px}")

# ── Sezione 3: Dimensionamento LED wall ─────────────────────────
st.header("🏗️ Dimensionamento LED Wall")
wall_width_mm = panels_base * panel_width_mm
wall_height_mm = panels_height * panel_height_mm
wall_width_m = wall_width_mm / 1000
wall_height_m = wall_height_mm / 1000

col_d1, col_d2, col_d3, col_d4, col_d5 = st.columns(5)
with col_d1:
    st.metric("Pannelli orizzontali", f"{panels_base}")
with col_d2:
    st.metric("Pannelli verticali", f"{panels_height}")
with col_d3:
    st.metric("Larghezza totale", f"{wall_width_m:.3f} m")
with col_d4:
    st.metric("Altezza totale", f"{wall_height_m:.3f} m")
with col_d5:
    total_pixels = w_px * h_px * panels_base * panels_height
    st.metric("Pixel totali wall", f"{total_pixels:,}")

# Dimensione in risoluzione completa
total_width_px = w_px * panels_base
total_height_px = h_px * panels_height

st.markdown("---")

# ── Sezione 4: Matrice pixel e configurazione hardware ────────────
st.header("🎛️ Configurazione Hardware NovaStar")

# Tabella riepilogativa
summary_data = {
    "Parametro": [
        "Risoluzione totale (L × A)",
        "Pixel totali LED",
        "Pannello pixel (L × A)",
        "Dimensione wall (m)",
        "Densità pixel/m²",
    ],
    "Valore": [
        f"{total_width_px} × {total_height_px}",
        f"{total_pixels:,}",
        f"{w_px} × {h_px}",
        f"{wall_width_m:.3f} × {wall_height_m:.3f}",
        f"{total_pixels / (wall_width_m * wall_height_m):,.0f}" if (wall_width_m * wall_height_m) > 0 else "N/A",
    ],
}

import pandas as pd
st.dataframe(pd.DataFrame(summary_data), width="stretch")

# Controller MCTRL raccomandati
st.subheader("🎯 Matrici NovaStar MCTRL raccomandate")

recs = get_recommended_controller(total_width_px, total_height_px)

if recs:
    for i, rc in enumerate(recs):
        with st.container():
            st.markdown(f"### {i+1}. **{rc['model']}** — {rc['type']}")
            cl1, cl2, cl3 = st.columns(3)
            with cl1:
                st.metric("Max risoluzione", f"{rc['max_resolution_width']} × {rc['max_resolution_height']}")
            with cl2:
                st.metric("Serie", "NovaStar MCTRL")
            with cl3:
                st.metric("Max pixel totali", f"{rc['total_pixels']:,}" if rc["total_pixels"] else "N/A")
            st.info(rc["description"])
            st.caption(f"🔌 {rc['ports']}  |  📌 {rc['recommended_use']}")
            st.link_button("Scheda prodotto ufficiale", rc["official_url"])
            st.divider()
else:
    st.warning(
        f"La risoluzione richiesta ({total_width_px} × {total_height_px}) è molto grande. "
        "Nessuna matrice MCTRL del catalogo ufficiale gestisce da sola questa risoluzione."
    )

# ── Sezione 5: Visualizzazione layout ─────────────────────────────
st.header("🗺️ Layout del LED Wall (rappresentazione schematica)")

# Griglia pannelli
layout_html = f"""
<div style="position:relative; width:{panels_base*100}px; height:{panels_height*60}px; border:3px solid #333; margin:auto;">
"""
for r in range(panels_height):
    for c in range(panels_base):
        label = f"P{r+1},{c+1}"
        layout_html += (
            f'<div style="position:absolute; left:{c*100}px; top:{r*60}px; '
            f'width:94px; height:54px; background:#2d7a3b; color:white; '
            f'display:flex; align-items:center; justify-content:center; '
            f'border:1px solid #fff; font-size:10px; cursor:pointer;">{label}</div>'
        )
layout_html += "</div>"
st.components.v1.html(layout_html, height=panels_height * 60 + 40)

# ── Sezione 6: Tabella dettagli pannelli ────────────────────────
st.header("📋 Dettaglio Pannello")
panel_details = []
for r in range(panels_height):
    for c in range(panels_base):
        x_start_mm = c * panel_width_mm
        y_start_mm = r * panel_height_mm
        panel_details.append({
            "Pannello": f"P{r*panels_base + c + 1}",
            "Colonna (x)": x_start_mm,
            "Riga (y)": y_start_mm,
            "Pixel X": w_px,
            "Pixel Y": h_px,
            "Area pixel": w_px * h_px,
        })

df_panels = pd.DataFrame(panel_details)
st.dataframe(df_panels, width="stretch")


# ── Footer ────────────────────────────────────────────────────────
st.divider()
st.markdown(
    "---\n"
    "*LED Wall Calculator — Dati NovaStar indicativi. Verificare sempre con il catalogo ufficiale "
    "[NovaStar](https://www.novastar.tech).*"
)
