"""Clase Reserva: integra cliente, servicio, duración y estado."""
from entidades import Entidad
from cliente import Cliente
from servicios import Servicio
from excepciones import (ReservaInvalidaError, OperacionNoPermitidaError,
                         ServicioNoDisponibleError, ErrorSoftwareFJ)
from registro import logger


class Reserva(Entidad):
    PENDIENTE, CONFIRMADA, CANCELADA = "PENDIENTE", "CONFIRMADA", "CANCELADA"

    def __init__(self, identificador, cliente, servicio, horas):
        super().__init__(identificador)
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva requiere un cliente válido")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere un servicio válido")
        self.cliente, self.servicio, self.horas = cliente, servicio, horas
        self.estado = self.PENDIENTE

    def confirmar(self):
        """Confirma la reserva si el servicio está disponible y la duración es válida."""
        if self.estado != self.PENDIENTE:
            raise OperacionNoPermitidaError(f"No se puede confirmar una reserva {self.estado}")
        if not self.servicio.disponible:
            raise ServicioNoDisponibleError(f"Servicio '{self.servicio.nombre}' no disponible")
        self.servicio.validar_parametros(self.horas)
        self.estado = self.CONFIRMADA
        logger.info(f"Reserva {self.id} confirmada")

    def cancelar(self):
        if self.estado == self.CANCELADA:
            raise OperacionNoPermitidaError("La reserva ya estaba cancelada")
        self.estado = self.CANCELADA
        logger.info(f"Reserva {self.id} cancelada")

    def procesar(self):
        """Confirma y calcula el costo; demuestra try/except/else/finally y encadenamiento."""
        try:
            self.confirmar()
            costo = self.servicio.calcular_costo(self.horas)
        except ErrorSoftwareFJ as e:
            logger.error(f"Reserva {self.id} falló: {e}")
            # Encadenamiento: conserva la causa original con 'from e'
            raise ReservaInvalidaError(f"No se pudo procesar la reserva {self.id}") from e
        else:
            logger.info(f"Reserva {self.id} procesada. Costo: ${costo}")
            return costo
        finally:
            logger.info(f"Fin de procesamiento de la reserva {self.id} (estado {self.estado})")

    def describir(self):
        return (f"Reserva #{self.id}: {self.cliente.nombre} -> {self.servicio.nombre} "
                f"({self.horas} h) [{self.estado}]")
