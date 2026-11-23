"""Configuración del archivo de logs (errores y eventos relevantes)."""
import logging
import os

RUTA_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "software_fj.log")
os.makedirs(os.path.dirname(RUTA_LOG), exist_ok=True)

logger = logging.getLogger("software_fj")
logger.setLevel(logging.INFO)
if not logger.handlers:  # evita duplicar handlers si se importa varias veces
    _h = logging.FileHandler(RUTA_LOG, encoding="utf-8")
    _h.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    logger.addHandler(_h)
