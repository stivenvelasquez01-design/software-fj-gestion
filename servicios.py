"""Servicio abstracto y tres servicios especializados (polimorfismo)."""  # Describe el módulo
from abc import abstractmethod  # Para declarar métodos abstractos
from entidades import Entidad  # Clase base de la que hereda Servicio
from excepciones import ServicioInvalidoError, CalculoInconsistenteError  # Excepciones personalizadas usadas aquí


class Servicio(Entidad):  # Clase abstracta Servicio (hereda de Entidad, que ya es abstracta)
    IVA = 0.19  # Atributo de clase: impuesto por defecto (19 %)

    def __init__(self, identificador, nombre, tarifa_hora):  # Constructor común a todos los servicios
        super().__init__(identificador)  # Inicializa el id en la clase base
        if not isinstance(nombre, str) or not nombre.strip():  # El nombre debe ser texto no vacío
            raise ServicioInvalidoError("El servicio requiere un nombre")  # Error si falta el nombre
        if not isinstance(tarifa_hora, (int, float)) or tarifa_hora <= 0:  # La tarifa debe ser un número positivo
            raise ServicioInvalidoError(f"Tarifa inválida: {tarifa_hora!r}")  # Error si la tarifa es inválida
        self.nombre = nombre.strip()  # Guarda el nombre limpio
        self._tarifa_hora = float(tarifa_hora)  # Atributo protegido: tarifa por hora como decimal
        self.disponible = True  # Por defecto el servicio está disponible

    @abstractmethod  # Cada servicio hijo debe implementarlo
    def validar_parametros(self, horas):  # Valida la duración según las reglas de cada servicio
        """Cada servicio valida la duración según sus propias reglas."""  # Polimorfismo

    @abstractmethod  # Cada servicio hijo debe implementarlo
    def costo_base(self, horas):  # Calcula el costo antes de impuestos y descuentos
        """Costo sin impuestos ni descuentos (varía por servicio)."""  # Polimorfismo

    def calcular_costo(self, horas, impuesto=None, descuento=0.0):  # Método "sobrecargado" mediante parámetros opcionales
        """Método 'sobrecargado' con parámetros opcionales:
        calcular_costo(h)                  -> base + IVA por defecto
        calcular_costo(h, impuesto=0.05)   -> impuesto personalizado
        calcular_costo(h, descuento=0.10)  -> con descuento (10 %)
        """  # Python no tiene sobrecarga real; se simula con valores por defecto
        self.validar_parametros(horas)  # Valida la duración (puede lanzar ServicioInvalidoError)
        if impuesto is None:  # Si no se indicó impuesto...
            impuesto = self.IVA  # ...se usa el IVA por defecto
        if not 0 <= descuento < 1 or impuesto < 0:  # El descuento debe estar en [0,1) y el impuesto no ser negativo
            raise CalculoInconsistenteError(f"Impuesto/descuento inválido: {impuesto}, {descuento}")  # Error de cálculo
        total = self.costo_base(horas) * (1 - descuento) * (1 + impuesto)  # Base, menos descuento, más impuesto
        if total <= 0:  # Un costo no positivo es inconsistente
            raise CalculoInconsistenteError(f"Costo no positivo: {total}")  # Error de cálculo
        return round(total, 2)  # Devuelve el total redondeado a 2 decimales


class ReservaSala(Servicio):  # Servicio especializado: reserva de salas
    def __init__(self, identificador, nombre, tarifa_hora, capacidad):  # Agrega el atributo capacidad
        super().__init__(identificador, nombre, tarifa_hora)  # Reutiliza el constructor de Servicio
        if not isinstance(capacidad, int) or capacidad <= 0:  # La capacidad debe ser un entero positivo
            raise ServicioInvalidoError(f"Capacidad inválida: {capacidad!r}")  # Error si es inválida
        self.capacidad = capacidad  # Guarda la capacidad de la sala

    def validar_parametros(self, horas):  # Sobrescribe: regla propia de las salas
        if not isinstance(horas, (int, float)) or not 1 <= horas <= 8:  # Entre 1 y 8 horas
            raise ServicioInvalidoError("Una sala se reserva entre 1 y 8 horas")  # Error si está fuera de rango

    def costo_base(self, horas):  # Sobrescribe: cálculo propio de las salas
        return self._tarifa_hora * horas  # Tarifa por hora multiplicada por las horas

    def describir(self):  # Implementa el método abstracto de Entidad
        return f"Sala '{self.nombre}' (capacidad {self.capacidad}) - ${self._tarifa_hora}/h"  # Descripción de la sala


class AlquilerEquipo(Servicio):  # Servicio especializado: alquiler de equipos
    def __init__(self, identificador, nombre, tarifa_hora, deposito):  # Agrega el atributo depósito
        super().__init__(identificador, nombre, tarifa_hora)  # Reutiliza el constructor de Servicio
        if not isinstance(deposito, (int, float)) or deposito < 0:  # El depósito debe ser un número no negativo
            raise ServicioInvalidoError(f"Depósito inválido: {deposito!r}")  # Error si es inválido
        self.deposito = deposito  # Guarda el depósito del equipo

    def validar_parametros(self, horas):  # Sobrescribe: regla propia de los equipos
        if not isinstance(horas, (int, float)) or not 1 <= horas <= 72:  # Entre 1 y 72 horas
            raise ServicioInvalidoError("Un equipo se alquila entre 1 y 72 horas")  # Error si está fuera de rango

    def costo_base(self, horas):  # Sobrescribe: cálculo propio de los equipos
        return self._tarifa_hora * horas + self.deposito  # Tarifa por horas más el depósito

    def describir(self):  # Implementa el método abstracto de Entidad
        return f"Equipo '{self.nombre}' - ${self._tarifa_hora}/h + depósito ${self.deposito}"  # Descripción del equipo


class Asesoria(Servicio):  # Servicio especializado: asesorías
    def __init__(self, identificador, nombre, tarifa_hora, especialidad):  # Agrega el atributo especialidad
        super().__init__(identificador, nombre, tarifa_hora)  # Reutiliza el constructor de Servicio
        if not isinstance(especialidad, str) or not especialidad.strip():  # La especialidad debe ser texto no vacío
            raise ServicioInvalidoError("La asesoría requiere una especialidad")  # Error si falta
        self.especialidad = especialidad  # Guarda la especialidad

    def validar_parametros(self, horas):  # Sobrescribe: regla propia de las asesorías
        if not isinstance(horas, (int, float)) or not 0.5 <= horas <= 4:  # Entre 0.5 y 4 horas
            raise ServicioInvalidoError("Una asesoría dura entre 0.5 y 4 horas")  # Error si está fuera de rango

    def costo_base(self, horas):  # Sobrescribe: cálculo propio de las asesorías
        return self._tarifa_hora * horas * 1.25  # Tarifa por horas con 25 % de recargo por especialización

    def describir(self):  # Implementa el método abstracto de Entidad
        return f"Asesoría '{self.nombre}' en {self.especialidad} - ${self._tarifa_hora}/h"  # Descripción de la asesoría
