"""Clase abstracta base para las entidades del sistema."""  # Describe el módulo
from abc import ABC, abstractmethod  # ABC permite crear clases abstractas; abstractmethod marca métodos obligatorios


class Entidad(ABC):  # Clase abstracta: no se puede instanciar directamente
    """Entidad general: toda entidad tiene un identificador y se puede describir."""  # Contrato común del sistema

    def __init__(self, identificador):  # Constructor: recibe el identificador de la entidad
        self._id = identificador  # Atributo protegido (convención _): encapsulación del id

    @property  # Convierte el método en una propiedad de solo lectura
    def id(self):  # Getter del identificador
        """Identificador de solo lectura."""  # Sin setter: no se puede modificar desde fuera
        return self._id  # Devuelve el identificador almacenado

    @abstractmethod  # Obliga a las clases hijas a implementar este método
    def describir(self):  # Método abstracto: cada entidad se describe a su manera
        """Devuelve una descripción en texto de la entidad."""  # Las subclases lo sobrescriben (polimorfismo)
