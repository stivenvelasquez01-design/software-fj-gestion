"""Clase Cliente con validaciones estrictas y datos encapsulados."""
import re
from entidades import Entidad
from excepciones import ClienteInvalidoError


class Cliente(Entidad):
    def __init__(self, identificador, nombre, correo, telefono):
        super().__init__(identificador)
        # Se asigna mediante los setters para reutilizar las validaciones
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self):
        return self.__nombre  # atributo privado

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError(f"Nombre inválido: {valor!r}")
        self.__nombre = valor.strip()

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if not isinstance(valor, str) or not re.fullmatch(r"[\w.+-]+@[\w-]+\.[\w.]+", valor):
            raise ClienteInvalidoError(f"Correo inválido: {valor!r}")
        self.__correo = valor

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        if not isinstance(valor, str) or not valor.isdigit() or len(valor) != 10:
            raise ClienteInvalidoError(f"Teléfono inválido (deben ser 10 dígitos): {valor!r}")
        self.__telefono = valor

    def describir(self):
        return f"Cliente #{self.id}: {self.nombre} <{self.correo}>"
