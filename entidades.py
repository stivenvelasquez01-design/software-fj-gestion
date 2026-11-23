"""Clase abstracta base para las entidades del sistema."""
from abc import ABC, abstractmethod


class Entidad(ABC):
    """Entidad general: toda entidad tiene un identificador y se puede describir."""

    def __init__(self, identificador):
        self._id = identificador  # atributo protegido (encapsulación)

    @property
    def id(self):
        """Identificador de solo lectura."""
        return self._id

    @abstractmethod
    def describir(self):
        """Devuelve una descripción en texto de la entidad."""
