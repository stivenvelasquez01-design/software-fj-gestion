"""Clase Cliente con validaciones estrictas y datos encapsulados."""  # Describe el módulo
import re  # Módulo de expresiones regulares, usado para validar el correo
from entidades import Entidad  # Clase abstracta de la que hereda Cliente
from excepciones import ClienteInvalidoError  # Excepción personalizada para datos inválidos


class Cliente(Entidad):  # Cliente hereda de Entidad
    def __init__(self, identificador, nombre, correo, telefono):  # Constructor con los datos del cliente
        super().__init__(identificador)  # Inicializa la parte heredada (el id)
        # Se asigna mediante los setters para reutilizar las validaciones
        self.nombre = nombre  # Dispara el setter de nombre (valida)
        self.correo = correo  # Dispara el setter de correo (valida)
        self.telefono = telefono  # Dispara el setter de teléfono (valida)

    @property  # Getter de nombre
    def nombre(self):  # Permite leer cliente.nombre
        return self.__nombre  # Atributo privado (doble guion bajo): encapsulación fuerte

    @nombre.setter  # Setter de nombre con validación
    def nombre(self, valor):  # Se ejecuta al asignar cliente.nombre = valor
        if not isinstance(valor, str) or len(valor.strip()) < 3:  # Debe ser texto de al menos 3 caracteres
            raise ClienteInvalidoError(f"Nombre inválido: {valor!r}")  # Lanza error personalizado si no cumple
        self.__nombre = valor.strip()  # Guarda el nombre sin espacios sobrantes

    @property  # Getter de correo
    def correo(self):  # Permite leer cliente.correo
        return self.__correo  # Devuelve el atributo privado

    @correo.setter  # Setter de correo con validación
    def correo(self, valor):  # Se ejecuta al asignar cliente.correo = valor
        if not isinstance(valor, str) or not re.fullmatch(r"[\w.+-]+@[\w-]+\.[\w.]+", valor):  # Debe tener formato usuario@dominio.ext
            raise ClienteInvalidoError(f"Correo inválido: {valor!r}")  # Error si el formato no coincide
        self.__correo = valor  # Guarda el correo válido

    @property  # Getter de teléfono
    def telefono(self):  # Permite leer cliente.telefono
        return self.__telefono  # Devuelve el atributo privado

    @telefono.setter  # Setter de teléfono con validación
    def telefono(self, valor):  # Se ejecuta al asignar cliente.telefono = valor
        if not isinstance(valor, str) or not valor.isdigit() or len(valor) != 10:  # Debe ser texto numérico de 10 dígitos
            raise ClienteInvalidoError(f"Teléfono inválido (deben ser 10 dígitos): {valor!r}")  # Error si no cumple
        self.__telefono = valor  # Guarda el teléfono válido

    def describir(self):  # Implementa el método abstracto de Entidad
        return f"Cliente #{self.id}: {self.nombre} <{self.correo}>"  # Texto con id, nombre y correo
