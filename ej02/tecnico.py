from datagram_modules import MPDU, Datagrama, ControlSistema
import sys

nombre = sys.argv[1] if len(sys.argv) > 1 else "tecnicoX"
sector = sys.argv[2] if len(sys.argv) > 2 else "Empaque"

cola_principal = "solicitud_turnos"
cola_respuesta = f"respuesta_{nombre}"

dgram = Datagrama()
control = ControlSistema()

solicitud = MPDU(
    hdr={"tipo": "turno"},
    sdu={"tecnico": nombre, "sector": sector}
)

dgram.send_to(cola_principal, solicitud)
print(f"[{nombre}] Solicitando turno para el sector: {sector}...")

loop_activo = True
while loop_activo:
    respuesta = dgram.receive_from(cola_respuesta, timeout=1)
    if respuesta != None:
        resultado = respuesta.sdu["turno"]

        if resultado == "Especialidad INEXISTENTE" or resultado == "no hay disponibilidad":
            print(f"[{nombre}] Solicitud rechazada: {resultado}")
            print(f"[{nombre}] Finalizando proceso.")
        else:
            print(f"[{nombre}] Turno asignado: {resultado}")
        loop_activo = False
    if not control.is_alive():
        loop_activo = False
