import json
import logging
import re
import sys
import os
from pathlib import Path

logger = logging.getLogger(__name__)

# Linux & Windows Standard-Pfade
STEAM_DEFAULT_PATHS = [
    Path("C:/Program Files (x86)/Steam"),
    Path("C:/Program Files/Steam"),
    Path.home() / ".steam/steam",
    Path.home() / ".local/share/Steam",
    Path.home() / ".var/app/com.valvesoftware.Steam/.local/share/Steam",
]

GAME_EXE = Path("bin64/CrimsonDesert.exe")
LIBRARY_FOLDERS_VDF = "steamapps/libraryfolders.vdf"

def _find_steam_root() -> Path | None:
    for p in STEAM_DEFAULT_PATHS:
        if p.exists():
            return p
    if sys.platform == "win32":
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            steam = Path(f"{letter}:/Steam")
            if steam.exists(): return steam
            steam2 = Path(f"{letter}:/SteamLibrary")
            if steam2.exists(): return steam2
    return None

def _parse_library_folders(vdf_path: Path) -> list[Path]:
    paths: list[Path] = []
    try:
        text = vdf_path.read_text(encoding="utf-8")
        for match in re.finditer(r'\"path\"\\s+\"([^\"]+)\"', text):
            paths.append(Path(match.group(1).replace("\\\\", "/")))
    except Exception as e:
        logger.error(f"Error parsing VDF: {e}")
    return paths

def find_game_directories() -> list[Path]:
    candidates: list[Path] = []
    steam_root = _find_steam_root()
    if steam_root:
        vdf = steam_root / LIBRARY_FOLDERS_VDF
        if vdf.exists():
            for lib in _parse_library_folders(vdf):
                d = lib / "steamapps/common/Crimson Desert"
                if d.exists(): candidates.append(d)

        direct = steam_root / "steamapps/common/Crimson Desert"
        if direct.exists(): candidates.append(direct)

    # Dubletten entfernen
    seen = set()
    unique = []
    for c in candidates:
        key = str(c.resolve()).lower()
        if key not in seen:
            seen.add(key)
            unique.append(c)
    return unique

# --- DIESE FUNKTIONEN FEHLTEN ---

def validate_game_directory(path: Path) -> bool:
    """Prüft, ob der Pfad eine gültige Installation ist."""
    if not path: return False
    return (path / GAME_EXE).exists()

def is_steam_install(game_dir: Path) -> bool:
    return "steamapps" in str(game_dir).lower()

def is_epic_install(game_dir: Path) -> bool:
    path_lower = str(game_dir).lower()
    return "epic games" in path_lower or "epicgames" in path_lower

def is_xbox_install(game_dir: Path) -> bool:
    return "pax" in str(game_dir).lower() # Vereinfacht für Kompatibilität
