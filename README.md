# Software FJ - Sistema integral de gestión de clientes, servicios y reservas

Proyecto del curso Programación (213023) - UNAD, Fase 4.
Sistema orientado a objetos en Python, sin base de datos, con manejo avanzado de excepciones y registro de eventos en un archivo de logs.

## Ejecución
```bash
python3 main.py
```
Los eventos y errores se guardan en `logs/software_fj.log`.

## Estructura
- `excepciones.py`: excepciones personalizadas
- `registro.py`: configuración del log
- `entidades.py`: clase abstracta `Entidad`
- `cliente.py`: clase `Cliente` (validaciones y encapsulación)
- `servicios.py`: `Servicio` (abstracta), `ReservaSala`, `AlquilerEquipo`, `Asesoria`
- `reserva.py`: clase `Reserva` (confirmar, cancelar, procesar)
- `main.py`: simulación de 13 operaciones válidas e inválidas
