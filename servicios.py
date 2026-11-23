"""Servicio abstracto y tres servicios especializados (polimorfismo)."""
from abc import abstractmethod
from entidades import Entidad
from excepciones import ServicioInvalidoError, CalculoInconsistenteError


class Servicio(Entidad):
    IVA = 0.19  # impuesto por defecto

    def __init__(self, identificador, nombre, tarifa_hora):
        super().__init__(identificador)
        if not isinstance(nombre, str) or not nombre.strip():
            raise ServicioInvalidoError("El servicio requiere un nombre")
        if not isinstance(tarifa_hora, (int, float)) or tarifa_hora <= 0:
            raise ServicioInvalidoError(f"Tarifa inválida: {tarifa_hora!r}")
        self.nombre = nombre.strip()
        self._tarifa_hora = float(tarifa_hora)
        self.disponible = True

    @abstractmethod
    def validar_parametros(self, horas):
        """Cada servicio valida la duración según sus propias reglas."""

    @abstractmethod
    def costo_base(self, horas):
        """Costo sin impuestos ni descuentos (varía por servicio)."""

    def calcular_costo(self, horas, impuesto=None, descuento=0.0):
        """Método 'sobrecargado' con parámetros opcionales:
        calcular_costo(h)                  -> base + IVA por defecto
        calcular_costo(h, impuesto=0.05)   -> impuesto personalizado
        calcular_costo(h, descuento=0.10)  -> con descuento (10 %)
        """
        self.validar_parametros(horas)
        if impuesto is None:
            impuesto = self.IVA
        if not 0 <= descuento < 1 or impuesto < 0:
            raise CalculoInconsistenteError(f"Impuesto/descuento inválido: {impuesto}, {descuento}")
        total = self.costo_base(horas) * (1 - descuento) * (1 + impuesto)
        if total <= 0:
            raise CalculoInconsistenteError(f"Costo no positivo: {total}")
        return round(total, 2)


class ReservaSala(Servicio):
    def __init__(self, identificador, nombre, tarifa_hora, capacidad):
        super().__init__(identificador, nombre, tarifa_hora)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioInvalidoError(f"Capacidad inválida: {capacidad!r}")
        self.capacidad = capacidad

    def validar_parametros(self, horas):
        if not isinstance(horas, (int, float)) or not 1 <= horas <= 8:
            raise ServicioInvalidoError("Una sala se reserva entre 1 y 8 horas")

    def costo_base(self, horas):
        return self._tarifa_hora * horas

    def describir(self):
        return f"Sala '{self.nombre}' (capacidad {self.capacidad}) - ${self._tarifa_hora}/h"


class AlquilerEquipo(Servicio):
    def __init__(self, identificador, nombre, tarifa_hora, deposito):
        super().__init__(identificador, nombre, tarifa_hora)
        if not isinstance(deposito, (int, float)) or deposito < 0:
            raise ServicioInvalidoError(f"Depósito inválido: {deposito!r}")
        self.deposito = deposito

    def validar_parametros(self, horas):
        if not isinstance(horas, (int, float)) or not 1 <= horas <= 72:
            raise ServicioInvalidoError("Un equipo se alquila entre 1 y 72 horas")

    def costo_base(self, horas):
        return self._tarifa_hora * horas + self.deposito  # incluye depósito

    def describir(self):
        return f"Equipo '{self.nombre}' - ${self._tarifa_hora}/h + depósito ${self.deposito}"


class Asesoria(Servicio):
    def __init__(self, identificador, nombre, tarifa_hora, especialidad):
        super().__init__(identificador, nombre, tarifa_hora)
        if not isinstance(especialidad, str) or not especialidad.strip():
            raise ServicioInvalidoError("La asesoría requiere una especialidad")
        self.especialidad = especialidad

    def validar_parametros(self, horas):
        if not isinstance(horas, (int, float)) or not 0.5 <= horas <= 4:
            raise ServicioInvalidoError("Una asesoría dura entre 0.5 y 4 horas")

    def costo_base(self, horas):
        return self._tarifa_hora * horas * 1.25  # recargo por especialización

    def describir(self):
        return f"Asesoría '{self.nombre}' en {self.especialidad} - ${self._tarifa_hora}/h"
