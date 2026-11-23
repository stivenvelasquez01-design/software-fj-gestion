"""Simulación de 13 operaciones (válidas e inválidas) sin base de datos."""  # Describe el módulo
from cliente import Cliente  # Clase Cliente
from servicios import ReservaSala, AlquilerEquipo, Asesoria  # Los tres servicios especializados
from reserva import Reserva  # Clase Reserva
from excepciones import ErrorSoftwareFJ  # Excepción base para capturar errores del sistema
from registro import logger, RUTA_LOG  # Logger y ruta del archivo de log

clientes, servicios, reservas = [], [], []  # "Base de datos" en memoria: tres listas vacías


def operacion(num, descripcion, funcion):  # Ejecuta una operación de forma segura
    """Ejecuta una operación; cualquier error se registra y el programa continúa."""  # Describe la función
    print(f"\n[{num:02d}] {descripcion}")  # Muestra el número y la descripción de la operación
    try:  # Intenta ejecutar la operación
        resultado = funcion()  # Llama a la función recibida
        print("   OK ->", resultado)  # Muestra el resultado exitoso
        logger.info(f"Operación {num} exitosa: {descripcion}")  # Registra el éxito en el log
    except ErrorSoftwareFJ as e:  # Captura los errores controlados del sistema
        causa = f" (causa: {e.__cause__})" if e.__cause__ else ""  # Si hay error encadenado, lo muestra
        print(f"   ERROR controlado -> {e}{causa}")  # Muestra el error en pantalla
        logger.error(f"Operación {num} fallida: {descripcion} | {e}{causa}")  # Registra el error en el log
    except Exception as e:  # Captura cualquier error inesperado para no detener el programa
        print(f"   ERROR inesperado -> {e!r}")  # Muestra el error inesperado
        logger.critical(f"Operación {num} error inesperado: {e!r}")  # Lo registra como crítico


def registrar(lista, obj):  # Agrega un objeto a una lista y devuelve su descripción
    lista.append(obj)  # Guarda el objeto en la lista
    return obj.describir()  # Devuelve la descripción (polimorfismo)


def main():  # Función principal de la simulación
    logger.info("=== Inicio de la simulación ===")  # Marca el inicio en el log
    operacion(1, "Cliente válido (Ana)", lambda: registrar(clientes, Cliente(1, "Ana Pérez", "ana@correo.com", "3001234567")))  # Cliente correcto
    operacion(2, "Cliente con correo inválido", lambda: registrar(clientes, Cliente(2, "Luis Gómez", "luis-correo", "3009876543")))  # Falla: correo
    operacion(3, "Cliente con teléfono inválido", lambda: registrar(clientes, Cliente(3, "Eva Ruiz", "eva@correo.com", "123")))  # Falla: teléfono
    operacion(4, "Cliente válido (Carlos)", lambda: registrar(clientes, Cliente(4, "Carlos Díaz", "carlos@correo.com", "3112223344")))  # Cliente correcto
    operacion(5, "Sala válida", lambda: registrar(servicios, ReservaSala(1, "Sala Norte", 50000, 10)))  # Servicio correcto
    operacion(6, "Equipo con tarifa negativa", lambda: registrar(servicios, AlquilerEquipo(2, "Portátil", -100, 20000)))  # Falla: tarifa
    operacion(7, "Equipo válido", lambda: registrar(servicios, AlquilerEquipo(3, "Proyector", 15000, 30000)))  # Servicio correcto
    operacion(8, "Asesoría válida", lambda: registrar(servicios, Asesoria(4, "Asesoría Python", 80000, "Programación")))  # Servicio correcto

    def reserva_ok():  # Operación 9: reserva exitosa
        r = Reserva(1, clientes[0], servicios[0], 3)  # Ana reserva la sala 3 horas
        reservas.append(r)  # Guarda la reserva
        costo = r.procesar()  # Confirma y calcula el costo
        return f"{r.describir()} | costo ${costo}"  # Devuelve la descripción y el costo
    operacion(9, "Reserva exitosa de sala (3 h)", reserva_ok)  # Ejecuta la operación 9

    def reserva_horas_malas():  # Operación 10: duración inválida
        r = Reserva(2, clientes[0], servicios[2], 10)  # Asesoría de 10 h (el máximo es 4)
        reservas.append(r)  # Guarda la reserva
        return r.procesar()  # Falla al procesar
    operacion(10, "Reserva con duración inválida (asesoría 10 h)", reserva_horas_malas)  # Ejecuta la operación 10

    def reserva_no_disponible():  # Operación 11: servicio no disponible
        servicios[0].disponible = False  # Marca la sala como no disponible
        r = Reserva(3, clientes[1], servicios[0], 2)  # Intenta reservar la sala no disponible
        reservas.append(r)  # Guarda la reserva
        return r.procesar()  # Falla al procesar
    operacion(11, "Reserva de servicio no disponible", reserva_no_disponible)  # Ejecuta la operación 11

    def cancelar_doble():  # Operación 12: cancelar dos veces
        r = reservas[0]  # Toma la primera reserva
        r.cancelar()  # Primera cancelación: válida
        r.cancelar()  # Segunda cancelación: lanza error
    operacion(12, "Cancelar dos veces la misma reserva", cancelar_doble)  # Ejecuta la operación 12

    operacion(13, "Reserva sin cliente", lambda: Reserva(4, None, servicios[0], 2))  # Falla: cliente None

    # Demostración de métodos sobrecargados (parámetros opcionales)
    print("\n[Extra] Costo de Asesoría 2 h:",  # Encabezado de la demostración
          servicios[2].calcular_costo(2),  # Con IVA por defecto
          "| sin IVA:", servicios[2].calcular_costo(2, impuesto=0),  # Con impuesto personalizado (0)
          "| con 10% desc.:", servicios[2].calcular_costo(2, descuento=0.10))  # Con 10 % de descuento

    logger.info("=== Fin de la simulación ===")  # Marca el final en el log
    print(f"\nSimulación terminada. Revisa el log en: {RUTA_LOG}")  # Indica dónde está el log


if __name__ == "__main__":  # Solo se ejecuta si el archivo se corre directamente
    main()  # Inicia la simulación
