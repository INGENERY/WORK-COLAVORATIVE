# =====================================================
# SISTEMA INTEGRAL DE GESTIÓN - SOFTWARE FJ
# Programación Orientada a Objetos + Excepciones
# =====================================================

from abc import ABC, abstractmethod
import logging

# =====================================================
# CONFIGURACIÓN DEL ARCHIVO LOG
# =====================================================

logging.basicConfig(
    filename="sistema_logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# =====================================================
# EXCEPCIONES PERSONALIZADAS
# =====================================================

class ClienteError(Exception):
    pass


class ServicioError(Exception):
    pass


class ReservaError(Exception):
    pass


# =====================================================
# CLASE ABSTRACTA PERSONA
# =====================================================

class Persona(ABC):

    def __init__(self, nombre, documento):
        self.nombre = nombre
        self.documento = documento

    @abstractmethod
    def mostrar_datos(self):
        pass


# =====================================================
# CLASE CLIENTE
# =====================================================

class Cliente(Persona):

    def __init__(self, nombre, documento, correo):

        super().__init__(nombre, documento)

        # VALIDACIONES
        if nombre.strip() == "":
            raise ClienteError("El nombre no puede estar vacío")

        if len(documento) < 5:
            raise ClienteError("Documento inválido")

        if "@" not in correo:
            raise ClienteError("Correo inválido")

        self.__correo = correo

    def mostrar_datos(self):
        return f"Cliente: {self.nombre} - Documento: {self.documento}"

    def obtener_correo(self):
        return self.__correo


# =====================================================
# CLASE ABSTRACTA SERVICIO
# =====================================================

class Servicio(ABC):

    def __init__(self, nombre, tarifa):
        self.nombre = nombre
        self.tarifa = tarifa

    @abstractmethod
    def calcular_costo(self, tiempo):
        pass

    @abstractmethod
    def descripcion(self):
        pass


# =====================================================
# SERVICIO RESERVA DE SALAS
# =====================================================

class ReservaSala(Servicio):

    def calcular_costo(self, horas):

        if horas <= 0:
            raise ServicioError("Las horas deben ser mayores a 0")

        return self.tarifa * horas

    def descripcion(self):
        return f"Reserva de sala - ${self.tarifa} por hora"


# =====================================================
# SERVICIO ALQUILER EQUIPOS
# =====================================================

class AlquilerEquipo(Servicio):

    def calcular_costo(self, dias):

        if dias <= 0:
            raise ServicioError("Los días deben ser mayores a 0")

        subtotal = self.tarifa * dias
        impuesto = subtotal * 0.19

        return subtotal + impuesto

    def descripcion(self):
        return f"Alquiler de equipos - ${self.tarifa} por día"


# =====================================================
# SERVICIO ASESORÍA
# =====================================================

class Asesoria(Servicio):

    def calcular_costo(self, sesiones):

        if sesiones <= 0:
            raise ServicioError("Las sesiones deben ser mayores a 0")

        return self.tarifa * sesiones

    def descripcion(self):
        return f"Asesoría especializada - ${self.tarifa} por sesión"


# =====================================================
# CLASE RESERVA
# =====================================================

class Reserva:

    def __init__(self, cliente, servicio, duracion):

        if duracion <= 0:
            raise ReservaError("La duración debe ser mayor a cero")

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"

    def confirmar(self):

        try:
            self.estado = "Confirmada"

            logging.info(
                f"Reserva confirmada para {self.cliente.nombre}"
            )

            print("\nReserva confirmada correctamente")

        except Exception as e:

            logging.error(f"Error al confirmar reserva: {e}")

    def cancelar(self):

        try:
            self.estado = "Cancelada"

            logging.warning(
                f"Reserva cancelada para {self.cliente.nombre}"
            )

            print("\nReserva cancelada")

        except Exception as e:

            logging.error(f"Error al cancelar reserva: {e}")

    def procesar_reserva(self):

        try:

            costo = self.servicio.calcular_costo(self.duracion)

        except Exception as e:

            logging.error(f"Error procesando reserva: {e}")

            raise ReservaError(
                "No fue posible procesar la reserva"
            ) from e

        else:

            print("-----------------------------------")
            print("RESERVA PROCESADA")
            print("-----------------------------------")
            print("Cliente:", self.cliente.nombre)
            print("Documento:", self.cliente.documento)
            print("Servicio:", self.servicio.nombre)
            print("Descripción:", self.servicio.descripcion())
            print("Duración:", self.duracion)
            print("Costo total: $", costo)
            print("Estado:", self.estado)
            print("-----------------------------------")

        finally:

            logging.info(
                f"Proceso finalizado para {self.cliente.nombre}"
            )


# =====================================================
# LISTAS
# =====================================================

clientes = []
servicios = []
reservas = []

# =====================================================
# CREACIÓN DE SERVICIOS
# =====================================================

try:

    sala = ReservaSala("Sala VIP", 50000)
    equipo = AlquilerEquipo("Computador Gamer", 80000)
    asesoria = Asesoria("Asesoría TI", 120000)

    servicios.append(sala)
    servicios.append(equipo)
    servicios.append(asesoria)

    print("Servicios creados correctamente\n")

except Exception as e:

    print("Error creando servicios:", e)
    logging.error(e)


# =====================================================
# OPERACIONES DEL SISTEMA
# =====================================================

print("========== SISTEMA SOFTWARE FJ ==========\n")

# -----------------------------------------------------
# OPERACIÓN 1 - CLIENTE VÁLIDO
# -----------------------------------------------------

try:

    cliente1 = Cliente(
        "Juan Pérez",
        "12345",
        "juan@gmail.com"
    )

    clientes.append(cliente1)

    print("Cliente registrado correctamente")
    print(cliente1.mostrar_datos())

except ClienteError as e:

    print("Error:", e)
    logging.error(e)

# -----------------------------------------------------
# OPERACIÓN 2 - CLIENTE INVÁLIDO
# -----------------------------------------------------

try:

    cliente2 = Cliente(
        "",
        "111",
        "correo.com"
    )

    clientes.append(cliente2)

except ClienteError as e:

    print("\nError registrando cliente:")
    print(e)

    logging.error(e)

# -----------------------------------------------------
# OPERACIÓN 3 - RESERVA SALA
# -----------------------------------------------------

try:

    reserva1 = Reserva(cliente1, sala, 3)

    reservas.append(reserva1)

    reserva1.confirmar()

    reserva1.procesar_reserva()

except Exception as e:

    print("Error:", e)

    logging.error(e)

# -----------------------------------------------------
# OPERACIÓN 4 - RESERVA EQUIPO
# -----------------------------------------------------

try:

    reserva2 = Reserva(cliente1, equipo, 2)

    reservas.append(reserva2)

    reserva2.confirmar()

    reserva2.procesar_reserva()

except Exception as e:

    print("Error:", e)

    logging.error(e)

# -----------------------------------------------------
# OPERACIÓN 5 - RESERVA ASESORÍA
# -----------------------------------------------------

try:

    reserva3 = Reserva(cliente1, asesoria, 4)

    reservas.append(reserva3)

    reserva3.confirmar()

    reserva3.procesar_reserva()

except Exception as e:

    print("Error:", e)

    logging.error(e)

# -----------------------------------------------------
# OPERACIÓN 6 - RESERVA INVÁLIDA
# -----------------------------------------------------

try:

    reserva4 = Reserva(cliente1, sala, -2)

    reservas.append(reserva4)

except Exception as e:

    print("\nError creando reserva:")
    print(e)

    logging.error(e)

# -----------------------------------------------------
# OPERACIÓN 7 - COSTO INVÁLIDO
# -----------------------------------------------------

try:

    print("\nProbando cálculo inválido")

    sala.calcular_costo(-5)

except Exception as e:

    print("Error:", e)

    logging.error(e)

# -----------------------------------------------------
# OPERACIÓN 8 - CANCELAR RESERVA
# -----------------------------------------------------

try:

    reserva2.cancelar()

except Exception as e:

    print("Error:", e)

    logging.error(e)

# =====================================================
# FIN DEL SISTEMA
# =====================================================

print("\n========== FIN DEL SISTEMA ==========")