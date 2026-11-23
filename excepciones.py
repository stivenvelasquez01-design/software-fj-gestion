"""Excepciones personalizadas del sistema Software FJ."""


class ErrorSoftwareFJ(Exception):
    """Excepción base: todas las demás heredan de ella."""


class ClienteInvalidoError(ErrorSoftwareFJ):
    """Datos de cliente inválidos (nombre, correo, teléfono...)."""


class ServicioInvalidoError(ErrorSoftwareFJ):
    """Parámetros inválidos al crear o configurar un servicio."""


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """El servicio existe pero no está disponible para reservar."""


class ReservaInvalidaError(ErrorSoftwareFJ):
    """Datos inválidos al crear una reserva (duración, cliente, servicio)."""


class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """Transición de estado no permitida (ej. cancelar una reserva ya cancelada)."""


class CalculoInconsistenteError(ErrorSoftwareFJ):
    """El cálculo de costos produjo un valor inconsistente."""
