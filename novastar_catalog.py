novastar_products = [
    {
        "model": "MCTRL R5",
        "type": "LED Display Controller",
        "max_resolution_width": 3840,
        "max_resolution_height": 2160,
        "total_pixels": 2_600_000,
        "ports": "8 x Gigabit Ethernet; 2 x 10G optical",
        "recommended_use": "LED wall fino a 4K",
        "description": "Controller MCTRL con ingressi 6G-SDI, DVI e HDMI 1.4.",
        "official_url": "https://www.novastar.tech/product/detail.html?catid=2&id=25",
    },
    {
        "model": "MCTRL4K",
        "type": "LED Display Controller",
        "max_resolution_width": 7680,
        "max_resolution_height": 7680,
        "total_pixels": 8_800_000,
        "ports": "16 x Gigabit Ethernet; 4 x 10G optical",
        "recommended_use": "LED wall 4K e ad alta risoluzione",
        "description": "Controller MCTRL4K con ingressi DP 1.2, HDMI 2.0 e DVI.",
        "official_url": "https://www.novastar.tech/product/detail.html?catid=2&id=24",
    },
    {
        "model": "MCTRL700",
        "type": "LED Display Controller",
        "max_resolution_width": 3840,
        "max_resolution_height": 3840,
        "total_pixels": 2_300_000,
        "ports": "6 x Gigabit Ethernet",
        "recommended_use": "LED wall fino a 1920 x 1200",
        "description": "Controller MCTRL con ingressi DVI e HDMI 1.3.",
        "official_url": "https://www.novastar.tech/product/detail.html?catid=2&id=29",
    },
    {
        "model": "MCTRL600",
        "type": "LED Display Controller",
        "max_resolution_width": 3840,
        "max_resolution_height": 3840,
        "total_pixels": 2_300_000,
        "ports": "4 x Gigabit Ethernet",
        "recommended_use": "LED wall fino a 1920 x 1200",
        "description": "Controller MCTRL compatto per installazioni di piccola/media dimensione.",
        "official_url": "https://www.novastar.tech/product/detail.html?catid=2&id=28",
    },
    {
        "model": "MCTRL660",
        "type": "LED Display Controller",
        "max_resolution_width": 3840,
        "max_resolution_height": 2560,
        "total_pixels": 1_300_000,
        "ports": "4 x Gigabit Ethernet",
        "recommended_use": "LED wall fino a 1,3 milioni di pixel",
        "description": "Controller MCTRL con ingressi DVI e HDMI 1.3.",
        "official_url": "https://www.novastar.tech/product/detail.html?catid=2&id=27",
    },
    {
        "model": "MCTRL660 PRO",
        "type": "LED Display Controller",
        "max_resolution_width": 3840,
        "max_resolution_height": 2560,
        "total_pixels": 3_900_000,
        "ports": "6 x Gigabit Ethernet; 2 x 10G optical",
        "recommended_use": "LED wall fino a 3,9 milioni di pixel",
        "description": "Controller MCTRL PRO con ingressi DVI, HDMI 1.4 e 3G-SDI.",
        "official_url": "https://www.novastar.tech/product/detail.html?catid=2&id=26",
    },
    {
        "model": "MCTRL300",
        "type": "LED Display Controller",
        "max_resolution_width": 3840,
        "max_resolution_height": 2560,
        "total_pixels": 1_300_000,
        "ports": "2 x Gigabit Ethernet",
        "recommended_use": "LED wall fino a 1,3 milioni di pixel",
        "description": "Controller MCTRL compatto con ingresso DVI.",
        "official_url": "https://www.novastar.tech/product/detail.html?catid=2&id=30",
    },
]


def get_recommended_controller(total_width_px: int, total_height_px: int) -> list:
    """Restituisce i controller MCTRL del catalogo ufficiale adatti alla risoluzione."""
    if total_width_px <= 0 or total_height_px <= 0:
        raise ValueError("Le dimensioni della risoluzione devono essere maggiori di zero.")

    total_pixels = total_width_px * total_height_px
    compatible = [
        product
        for product in novastar_products
        if total_width_px <= product["max_resolution_width"]
        and total_height_px <= product["max_resolution_height"]
        and total_pixels <= product["total_pixels"]
    ]

    return sorted(compatible, key=lambda product: product["total_pixels"])


def get_required_receiving_cards(total_width_px: int, total_height_px: int,
                                 panel_width_px: int, panel_height_px: int) -> dict:
    """Mantiene il calcolo legacy delle schede riceventi, senza usarlo per la matrice MCTRL."""
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
        "recommendation": f"{max(1, cards_needed_width)} x {max(1, cards_needed_height)} schede riceventi",
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
