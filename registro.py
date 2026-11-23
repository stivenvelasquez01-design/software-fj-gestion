"""Configuración del archivo de logs (errores y eventos relevantes)."""  # Describe el módulo
import logging  # Módulo estándar de Python para registrar mensajes
import os  # Módulo para trabajar con rutas y carpetas del sistema

RUTA_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "software_fj.log")  # Ruta absoluta del log junto a este archivo
os.makedirs(os.path.dirname(RUTA_LOG), exist_ok=True)  # Crea la carpeta logs si no existe (sin error si ya existe)

logger = logging.getLogger("software_fj")  # Obtiene (o crea) el logger con nombre propio
logger.setLevel(logging.INFO)  # Registra mensajes desde nivel INFO hacia arriba (INFO, WARNING, ERROR, CRITICAL)
if not logger.handlers:  # Evita agregar el manejador dos veces si el módulo se importa varias veces
    _h = logging.FileHandler(RUTA_LOG, encoding="utf-8")  # Manejador que escribe en el archivo de log con codificación UTF-8
    _h.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))  # Formato: fecha y hora | nivel | mensaje
    logger.addHandler(_h)  # Conecta el manejador al logger
