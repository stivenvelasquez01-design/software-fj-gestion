"""Excepciones personalizadas del sistema Software FJ."""  # Docstring: describe el propósito del módulo


class ErrorSoftwareFJ(Exception):  # Excepción base; hereda de Exception para poder capturarse con try/except
    """Excepción base: todas las demás heredan de ella."""  # Capturar esta clase atrapa cualquier error del sistema


class ClienteInvalidoError(ErrorSoftwareFJ):  # Error específico para datos de cliente incorrectos
    """Datos de cliente inválidos (nombre, correo, teléfono...)."""  # Se lanza desde las validaciones de Cliente


class ServicioInvalidoError(ErrorSoftwareFJ):  # Error para parámetros incorrectos de un servicio
    """Parámetros inválidos al crear o configurar un servicio."""  # Ej.: tarifa negativa o duración fuera de rango


class ServicioNoDisponibleError(ErrorSoftwareFJ):  # Error cuando el servicio no se puede reservar ahora
    """El servicio existe pero no está disponible para reservar."""  # Se lanza si servicio.disponible es False


class ReservaInvalidaError(ErrorSoftwareFJ):  # Error para reservas mal formadas o que no se pudieron procesar
    """Datos inválidos al crear una reserva (duración, cliente, servicio)."""  # También envuelve otros errores (encadenamiento)


class OperacionNoPermitidaError(ErrorSoftwareFJ):  # Error de transición de estado inválida
    """Transición de estado no permitida (ej. cancelar una reserva ya cancelada)."""  # Protege la coherencia del estado


class CalculoInconsistenteError(ErrorSoftwareFJ):  # Error cuando un cálculo da un resultado absurdo
    """El cálculo de costos produjo un valor inconsistente."""  # Ej.: descuento fuera de rango o costo no positivo
