"""Simulación de 12 operaciones (válidas e inválidas) sin base de datos."""
from cliente import Cliente
from servicios import ReservaSala, AlquilerEquipo, Asesoria
from reserva import Reserva
from excepciones import ErrorSoftwareFJ
from registro import logger, RUTA_LOG

clientes, servicios, reservas = [], [], []  # "base de datos" en memoria


def operacion(num, descripcion, funcion):
    """Ejecuta una operación; cualquier error se registra y el programa continúa."""
    print(f"\n[{num:02d}] {descripcion}")
    try:
        resultado = funcion()
        print("   OK ->", resultado)
        logger.info(f"Operación {num} exitosa: {descripcion}")
    except ErrorSoftwareFJ as e:
        causa = f" (causa: {e.__cause__})" if e.__cause__ else ""
        print(f"   ERROR controlado -> {e}{causa}")
        logger.error(f"Operación {num} fallida: {descripcion} | {e}{causa}")
    except Exception as e:  # cualquier error inesperado tampoco detiene el sistema
        print(f"   ERROR inesperado -> {e!r}")
        logger.critical(f"Operación {num} error inesperado: {e!r}")


def registrar(lista, obj):
    lista.append(obj)
    return obj.describir()


def main():
    logger.info("=== Inicio de la simulación ===")
    operacion(1, "Cliente válido (Ana)", lambda: registrar(clientes, Cliente(1, "Ana Pérez", "ana@correo.com", "3001234567")))
    operacion(2, "Cliente con correo inválido", lambda: registrar(clientes, Cliente(2, "Luis Gómez", "luis-correo", "3009876543")))
    operacion(3, "Cliente con teléfono inválido", lambda: registrar(clientes, Cliente(3, "Eva Ruiz", "eva@correo.com", "123")))
    operacion(4, "Cliente válido (Carlos)", lambda: registrar(clientes, Cliente(4, "Carlos Díaz", "carlos@correo.com", "3112223344")))
    operacion(5, "Sala válida", lambda: registrar(servicios, ReservaSala(1, "Sala Norte", 50000, 10)))
    operacion(6, "Equipo con tarifa negativa", lambda: registrar(servicios, AlquilerEquipo(2, "Portátil", -100, 20000)))
    operacion(7, "Equipo válido", lambda: registrar(servicios, AlquilerEquipo(3, "Proyector", 15000, 30000)))
    operacion(8, "Asesoría válida", lambda: registrar(servicios, Asesoria(4, "Asesoría Python", 80000, "Programación")))

    def reserva_ok():
        r = Reserva(1, clientes[0], servicios[0], 3)
        reservas.append(r)
        costo = r.procesar()
        return f"{r.describir()} | costo ${costo}"
    operacion(9, "Reserva exitosa de sala (3 h)", reserva_ok)

    def reserva_horas_malas():
        r = Reserva(2, clientes[0], servicios[2], 10)  # asesoría máx 4 h
        reservas.append(r)
        return r.procesar()
    operacion(10, "Reserva con duración inválida (asesoría 10 h)", reserva_horas_malas)

    def reserva_no_disponible():
        servicios[1 - 1].disponible = False
        r = Reserva(3, clientes[1], servicios[0], 2)
        reservas.append(r)
        return r.procesar()
    operacion(11, "Reserva de servicio no disponible", reserva_no_disponible)

    def cancelar_doble():
        r = reservas[0]
        r.cancelar()
        r.cancelar()  # segunda cancelación -> error
    operacion(12, "Cancelar dos veces la misma reserva", cancelar_doble)

    operacion(13, "Reserva sin cliente", lambda: Reserva(4, None, servicios[0], 2))

    # Demostración de métodos sobrecargados (parámetros opcionales)
    print("\n[Extra] Costo de Asesoría 2 h:",
          servicios[2].calcular_costo(2),
          "| sin IVA:", servicios[2].calcular_costo(2, impuesto=0),
          "| con 10% desc.:", servicios[2].calcular_costo(2, descuento=0.10))

    logger.info("=== Fin de la simulación ===")
    print(f"\nSimulación terminada. Revisa el log en: {RUTA_LOG}")


if __name__ == "__main__":
    main()
