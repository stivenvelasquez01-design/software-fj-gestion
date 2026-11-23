"""Clase Reserva: integra cliente, servicio, duración y estado."""  # Describe el módulo
from entidades import Entidad  # Clase base de Reserva
from cliente import Cliente  # Para verificar que el cliente sea del tipo correcto
from servicios import Servicio  # Para verificar que el servicio sea del tipo correcto
from excepciones import (ReservaInvalidaError, OperacionNoPermitidaError,
                         ServicioNoDisponibleError, ErrorSoftwareFJ)  # Excepciones personalizadas que se usan aquí
from registro import logger  # Logger para escribir eventos y errores en el archivo de log


class Reserva(Entidad):  # Reserva hereda de Entidad
    PENDIENTE, CONFIRMADA, CANCELADA = "PENDIENTE", "CONFIRMADA", "CANCELADA"  # Estados posibles de una reserva

    def __init__(self, identificador, cliente, servicio, horas):  # Constructor: cliente, servicio y duración
        super().__init__(identificador)  # Inicializa el id en la clase base
        if not isinstance(cliente, Cliente):  # El cliente debe ser un objeto Cliente
            raise ReservaInvalidaError("La reserva requiere un cliente válido")  # Error si no lo es
        if not isinstance(servicio, Servicio):  # El servicio debe ser un objeto Servicio
            raise ReservaInvalidaError("La reserva requiere un servicio válido")  # Error si no lo es
        self.cliente, self.servicio, self.horas = cliente, servicio, horas  # Guarda los datos de la reserva
        self.estado = self.PENDIENTE  # Toda reserva nace en estado PENDIENTE

    def confirmar(self):  # Pasa la reserva de PENDIENTE a CONFIRMADA
        """Confirma la reserva si el servicio está disponible y la duración es válida."""  # Describe el método
        if self.estado != self.PENDIENTE:  # Solo se confirma una reserva pendiente
            raise OperacionNoPermitidaError(f"No se puede confirmar una reserva {self.estado}")  # Error de estado
        if not self.servicio.disponible:  # Verifica la disponibilidad del servicio
            raise ServicioNoDisponibleError(f"Servicio '{self.servicio.nombre}' no disponible")  # Error si no está disponible
        self.servicio.validar_parametros(self.horas)  # Valida la duración (polimorfismo: cada servicio tiene su regla)
        self.estado = self.CONFIRMADA  # Cambia el estado
        logger.info(f"Reserva {self.id} confirmada")  # Registra el evento en el log

    def cancelar(self):  # Pasa la reserva a CANCELADA
        if self.estado == self.CANCELADA:  # No se puede cancelar dos veces
            raise OperacionNoPermitidaError("La reserva ya estaba cancelada")  # Error de estado
        self.estado = self.CANCELADA  # Cambia el estado
        logger.info(f"Reserva {self.id} cancelada")  # Registra el evento en el log

    def procesar(self):  # Confirma y calcula el costo de la reserva
        """Confirma y calcula el costo; demuestra try/except/else/finally y encadenamiento."""  # Describe el método
        try:  # Bloque donde pueden ocurrir errores
            self.confirmar()  # Intenta confirmar la reserva
            costo = self.servicio.calcular_costo(self.horas)  # Intenta calcular el costo
        except ErrorSoftwareFJ as e:  # Captura cualquier error propio del sistema
            logger.error(f"Reserva {self.id} falló: {e}")  # Registra el error en el log
            # Encadenamiento: conserva la causa original con 'from e'
            raise ReservaInvalidaError(f"No se pudo procesar la reserva {self.id}") from e  # Relanza con la causa original
        else:  # Se ejecuta solo si el try terminó sin errores
            logger.info(f"Reserva {self.id} procesada. Costo: ${costo}")  # Registra el éxito en el log
            return costo  # Devuelve el costo calculado
        finally:  # Se ejecuta siempre, haya o no error
            logger.info(f"Fin de procesamiento de la reserva {self.id} (estado {self.estado})")  # Registra el cierre

    def describir(self):  # Implementa el método abstracto de Entidad
        return (f"Reserva #{self.id}: {self.cliente.nombre} -> {self.servicio.nombre} "
                f"({self.horas} h) [{self.estado}]")  # Texto con cliente, servicio, horas y estado
