novastar_products = [
    {
        "model": "M10",
        "type": "Main Control Card",
        "max_resolution_width": 3840,
        "max_resolution_height": 2160,
        "card_count": 1,
        "total_pixels": 8_294_400,
        "description": "Scheda di controllo principale, supporta risoluzioni fino a 4K",
        "ports": "HDBCS (CobraNet)",
        "recommended_use": "LED wall piccoli/medi"
    },
    {
        "model": "M3",
        "type": "Main Control Card",
        "max_resolution_width": 1920,
        "max_resolution_height": 1080,
        "card_count": 1,
        "total_pixels": 2_073_600,
        "description": "Scheda compatta per installazioni di piccole dimensioni",
        "ports": "HDBCS",
        "recommended_use": "LED wall piccoli"
    },
    {
        "model": "M6",
        "type": "Main Control Card",
        "max_resolution_width": 3840,
        "max_resolution_height": 2160,
        "card_count": 1,
        "total_pixels": 8_294_400,
        "description": "Scheda principale economica per risoluzioni fino a 4K",
        "ports": "HDBCS",
        "recommended_use": "LED wall medi"
    },
    {
        "model": "HD650",
        "type": "Video Processor",
        "max_resolution_width": 2560,
        "max_resolution_height": 1600,
        "card_count": 1,
        "total_pixels": 4_096_000,
        "description": "Video processor HDR per installazioni di medie/grandi dimensioni",
        "ports": "HDBCS, HUB75",
        "recommended_use": "LED wall medi/grandi"
    },
    {
        "model": "HD240",
        "type": "Receiving Card",
        "max_resolution_width": 1920,
        "max_resolution_height": 1080,
        "card_count": 1,
        "total_pixels": 2_073_600,
        "description": "Scheda ricevente per LED wall distribuiti",
        "ports": "HUB75, HDBCS",
        "recommended_use": "Componente ricevente dei panel"
    },
    {
        "model": "E4S",
        "type": "Main Control Card",
        "max_resolution_width": 6144,
        "max_resolution_height": 2304,
        "card_count": 4,
        "total_pixels": 56_623_104,
        "description": "Alta performance per grandi LED wall con espandibilità multi-card",
        "ports": "HDBCS, HUB75, CobraNet",
        "recommended_use": "LED wall molto grandi"
    },
    {
        "model": "G4S",
        "type": "Sending Card",
        "max_resolution_width": 3840,
        "max_resolution_height": 2160,
        "card_count": 4,
        "total_pixels": 37_748_736,
        "description": "Scheda di invio per flussi video ad alta risoluzione",
        "ports": "HDBCS, HUB75, SDI, HDMI",
        "recommended_use": "Flusso in ingresso per grandi installazioni"
    },
]


def get_recommended_controller(total_width_px: int, total_height_px: int) -> list:
    """Torna la lista dei controller NovaStar raccomandati per una data risoluzione."""
    if total_width_px <= 0 or total_height_px <= 0:
        raise ValueError("Le dimensioni della risoluzione devono essere maggiori di zero.")

    recommendations = []
    for prod in novastar_products:
        if prod["type"] == "Main Control Card":
            if (prod["max_resolution_width"] >= total_width_px and
                    prod["max_resolution_height"] >= total_height_px):
                recommendations.append(prod)
            elif (total_width_px <= 8192 and total_height_px <= 4320):
                # Se supera le capacità di una singola scheda, suggerisci M10 o E4S in modalità multi-card
                pass

    # Se nessuna scheda singola basta, suggerisci soluzioni multi-card
    if not recommendations:
        if total_width_px * total_height_px <= 56_623_104:
            for prod in novastar_products:
                if prod["model"] == "E4S":
                    recommendations.append(prod)
                    break
        else:
            recommendations.append(
                {"model": "HD650 (più riceventi HD240)",
                 "type": "Video Processor + Receiving Cards",
                 "max_resolution_width": 2560,
                 "max_resolution_height": 1600,
                 "card_count": None,
                 "total_pixels": None,
                 "description": "Soluzione modulare con scheda invio HD650 e schede riceventi HD240 distribuite sui pannelli.",
                 "ports": "HDBCS",
                 "recommended_use": "LED wall molto grandi (> 8M × 4M)"}
            )

    return recommendations


def get_required_receiving_cards(total_width_px: int, total_height_px: int,
                                 panel_width_px: int, panel_height_px: int) -> dict:
    """Calcola quante schede riceventi (es. HD240 1920×1080) servono."""
    if total_width_px <= 0 or total_height_px <= 0:
        raise ValueError("Le dimensioni della risoluzione devono essere maggiori di zero.")
    if panel_width_px <= 0 or panel_height_px <= 0:
        raise ValueError("Le dimensioni del pannello devono essere maggiori di zero.")

    cards_needed_width = total_width_px // 1920 + (1 if total_width_px % 1920 else 0)
    cards_needed_height = total_height_px // 1080 + (1 if total_height_px % 1080 else 0)
    return {
        "cards_per_row": max(1, cards_needed_width),
        "cards_per_col": max(1, cards_needed_height),
        "total_cards": max(1, cards_needed_width * cards_needed_height),
        "recommendation": f"{max(1, cards_needed_width)} × {max(1, cards_needed_height)} riceventi HD240"
    }


def calculate_panel_pixels(panel_width_mm: float, panel_height_mm: float,
                           pixel_pitch_mm: float) -> tuple[int, int]:
    """Calcola i pixel per pannello a partire dalle dimensioni e dal passo."""
    if panel_width_mm <= 0 or panel_height_mm <= 0:
        raise ValueError("Le dimensioni del pannello devono essere maggiori di zero.")
    if pixel_pitch_mm <= 0:
        raise ValueError("Il pixel pitch deve essere maggiore di zero.")

    w_px = round(panel_width_mm / pixel_pitch_mm)
    h_px = round(panel_height_mm / pixel_pitch_mm)
    return max(1, w_px), max(1, h_px)
