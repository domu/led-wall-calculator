import json
import math
from pathlib import Path
from typing import Any


PANEL_ARCHIVE_PATH = Path(__file__).with_name("panel_archive.json")
_PROFILE_FIELDS = (
    "name",
    "manufacturer",
    "project",
    "width_mm",
    "height_mm",
    "pixel_pitch_mm",
    "max_absorption_w",
)


def _validate_profile(profile: Any) -> dict[str, Any]:
    if not isinstance(profile, dict):
        raise ValueError("Ogni profilo pannello deve essere un oggetto.")

    for field in ("name", "manufacturer", "project"):
        value = profile.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Il campo '{field}' è obbligatorio.")

    for field in ("width_mm", "height_mm", "pixel_pitch_mm", "max_absorption_w"):
        value = profile.get(field)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"Il campo '{field}' deve essere un numero.")
        if not math.isfinite(value) or value <= 0:
            raise ValueError(f"Il campo '{field}' deve essere maggiore di zero.")

    return {field: profile[field] for field in _PROFILE_FIELDS}


def load_panel_archive(path: Path = PANEL_ARCHIVE_PATH) -> list[dict[str, Any]]:
    """Carica e valida i profili dei pannelli dal file JSON versionato."""
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("L'archivio pannelli deve contenere una lista JSON.")
    return [_validate_profile(profile) for profile in data]


def save_panel_profile(
    profile: dict[str, Any], path: Path = PANEL_ARCHIVE_PATH
) -> list[dict[str, Any]]:
    """Aggiunge un profilo non duplicato e salva l'archivio JSON."""
    validated_profile = _validate_profile(profile)
    archive = load_panel_archive(path)

    profile_key = tuple(
        validated_profile[field].strip().casefold()
        for field in ("name", "manufacturer", "project")
    )
    for saved_profile in archive:
        saved_key = tuple(
            saved_profile[field].strip().casefold()
            for field in ("name", "manufacturer", "project")
        )
        if saved_key == profile_key:
            raise ValueError("Questo pannello è già presente nell'archivio.")

    archive.append(validated_profile)
    path.write_text(
        json.dumps(archive, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return archive


def calculate_total_max_absorption(
    panel_count: int, max_absorption_per_panel_w: float
) -> float:
    """Calcola la potenza massima teorica dell'intero wall in Watt."""
    if isinstance(panel_count, bool) or not isinstance(panel_count, int) or panel_count <= 0:
        raise ValueError("Il numero di pannelli deve essere maggiore di zero.")
    if (
        isinstance(max_absorption_per_panel_w, bool)
        or not isinstance(max_absorption_per_panel_w, (int, float))
        or not math.isfinite(max_absorption_per_panel_w)
        or max_absorption_per_panel_w <= 0
    ):
        raise ValueError("L'assorbimento massimo per pannello deve essere maggiore di zero.")
    return panel_count * max_absorption_per_panel_w
