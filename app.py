import json

import pandas as pd
import streamlit as st
from app_version import APP_VERSION
from panel_archive import (
    calculate_total_max_absorption,
    load_panel_archive,
    save_panel_profile,
)
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
panel_archive = load_panel_archive()

with st.sidebar:
    st.title("⚙️ Specifiche Pannello")
    st.divider()

    profile_options = [-1, *range(len(panel_archive))]

    def format_profile_option(index: int) -> str:
        if index == -1:
            return "Inserimento manuale"
        profile = panel_archive[index]
        return f"{profile['name']} — {profile['manufacturer']} · {profile['project']}"

    selected_profile_index = st.selectbox(
        "Tipo di pannello",
        options=profile_options,
        format_func=format_profile_option,
        help="Seleziona un profilo salvato oppure inserisci le specifiche manualmente.",
    )
    selected_profile = (
        None if selected_profile_index == -1 else panel_archive[selected_profile_index]
    )
    profile_widget_key = f"profile_{selected_profile_index}"

    col1, col2 = st.columns(2)
    with col1:
        panel_width_mm = st.number_input(
            "Larghezza pannello (mm)",
            min_value=1,
            value=int(selected_profile["width_mm"]) if selected_profile else 960,
            step=10,
            help="Dimensione base del singolo pannello in millimetri",
            key=f"panel_width_{profile_widget_key}",
        )
    with col2:
        panel_height_mm = st.number_input(
            "Altezza pannello (mm)",
            min_value=1,
            value=int(selected_profile["height_mm"]) if selected_profile else 640,
            step=10,
            help="Dimensione altezza del singolo pannello in millimetri",
            key=f"panel_height_{profile_widget_key}",
        )

    pixel_pitch = st.number_input(
        "Pixel Pitch (mm)",
        min_value=0.1,
        max_value=100.0,
        value=float(selected_profile["pixel_pitch_mm"]) if selected_profile else 2.5,
        step=0.5,
        help="Distanza tra due pixel adiacenti (pixel pitch) in millimetri",
        key=f"panel_pitch_{profile_widget_key}",
    )

    max_absorption_per_panel_w = st.number_input(
        "Assorbimento massimo per pannello (W)",
        min_value=0,
        value=int(selected_profile["max_absorption_w"]) if selected_profile else 0,
        step=10,
        help="Valore massimo dichiarato dal produttore; lascia 0 se non disponibile.",
        key=f"panel_absorption_{profile_widget_key}",
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

    if selected_profile:
        st.caption(
            f"Produttore: {selected_profile['manufacturer']} · "
            f"Progetto: {selected_profile['project']}"
        )

    with st.expander("Salva un tipo di pannello nell'archivio"):
        with st.form("save_panel_profile_form"):
            profile_name = st.text_input("Nome del pannello")
            profile_manufacturer = st.text_input("Produttore")
            profile_project = st.text_input("Progetto associato")
            save_profile = st.form_submit_button("Salva tipo di pannello")

        if save_profile:
            try:
                save_panel_profile(
                    {
                        "name": profile_name,
                        "manufacturer": profile_manufacturer,
                        "project": profile_project,
                        "width_mm": panel_width_mm,
                        "height_mm": panel_height_mm,
                        "pixel_pitch_mm": pixel_pitch,
                        "max_absorption_w": max_absorption_per_panel_w,
                    }
                )
            except ValueError as error:
                st.error(str(error))
            else:
                st.session_state["saved_panel_profile_notice"] = profile_name.strip()
                st.rerun()

    if "saved_panel_profile_notice" in st.session_state:
        st.success(
            f"Profilo '{st.session_state.pop('saved_panel_profile_notice')}' salvato nell'archivio."
        )

    st.download_button(
        "Scarica archivio JSON",
        data=json.dumps(panel_archive, ensure_ascii=False, indent=2),
        file_name="panel_archive.json",
        mime="application/json",
    )
    st.caption(
        "Su Streamlit Cloud, scarica e versiona il JSON aggiornato nel repository "
        "per conservare i profili anche dopo un nuovo deploy."
    )

    st.markdown("---")
    st.caption(f"Versione applicazione: v{APP_VERSION}")
    st.markdown(
        "[Davide Pedretti Biagioni - 2026](https://linktr.ee/davide.pedrettibiagioni)"
    )


# ── Pagina principale: risultati ────────────────────────────────────
st.title("📐 LED Wall Calculator")
st.caption("Dimensionamento LED wall con configurazione hardware NovaStar")

# ── Sezione 1: Specifiche pannello ─────────────────────────────
st.header("🔧 Specifiche del Pannello")
if selected_profile:
    st.caption(
        f"{selected_profile['name']} · {selected_profile['manufacturer']} · "
        f"Progetto {selected_profile['project']}"
    )
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

st.subheader("⚡ Assorbimento elettrico massimo stimato")
panel_count = panels_base * panels_height
if max_absorption_per_panel_w > 0:
    total_max_absorption_w = calculate_total_max_absorption(
        panel_count, max_absorption_per_panel_w
    )
    power_col1, power_col2, power_col3 = st.columns(3)
    with power_col1:
        st.metric("Assorbimento per pannello", f"{max_absorption_per_panel_w:,} W")
    with power_col2:
        st.metric("Pannelli totali", f"{panel_count}")
    with power_col3:
        st.metric(
            "Assorbimento massimo totale",
            f"{total_max_absorption_w:,.0f} W",
            help=f"{total_max_absorption_w / 1000:,.2f} kW",
        )
    st.caption(
        "Stima teorica basata sull'assorbimento massimo dichiarato dei pannelli; "
        "non include controller, alimentatori o altri apparati."
    )
    st.caption(f"Potenza equivalente: {total_max_absorption_w / 1000:,.2f} kW.")
else:
    total_max_absorption_w = None
    st.info("Inserisci l'assorbimento massimo per pannello per calcolare il totale.")

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
st.caption(
    "Anteprima dei pannelli; la visualizzazione è predisposta per aggiungere "
    "in seguito i percorsi di rete e alimentazione."
)

layout_html = f"""
<div role="img" aria-label="Layout LED wall: {panels_base} pannelli in larghezza e {panels_height} in altezza"
     style="display:grid; grid-template-columns:repeat({panels_base}, minmax(0, 1fr));
            gap:4px; max-width:1000px; margin:auto; padding:8px;
            border:3px solid #333; border-radius:8px;">
"""
panel_power_label = (
    f"{max_absorption_per_panel_w:,} W"
    if max_absorption_per_panel_w > 0
    else "assorb. n.d."
)
for r in range(panels_height):
    for c in range(panels_base):
        label = f"P{r+1},{c+1}"
        layout_html += (
            '<div style="min-height:54px; aspect-ratio:5 / 3; background:#2d7a3b; '
            'color:white; display:flex; flex-direction:column; align-items:center; '
            'justify-content:center; border:1px solid #fff; border-radius:4px; '
            f'font:12px sans-serif;">{label}'
            f'<span>{panel_power_label}</span></div>'
        )
layout_html += "</div>"
st.html(layout_html)

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
            "Assorbimento massimo (W)": max_absorption_per_panel_w or None,
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
