from datagram_modules import MPDU, Datagrama, ControlSistema

cola = "turnos"
dgram = Datagrama()
control = ControlSistema()
control.start()

print("[Controlador] Inicializando la agenda de turnos...")

sectores_validos = {"Envasado", "Empaque", "Limpieza"}

dgram.send_to("agenda:Envasado", MPDU(sdu="08:00"))
dgram.send_to("agenda:Envasado", MPDU(sdu="08:30"))
dgram.send_to("agenda:Empaque", MPDU(sdu="09:30"))
dgram.send_to("agenda:Limpieza", MPDU(sdu="10:00"))
dgram.send_to("agenda:Limpieza", MPDU(sdu="10:30"))
    
print("[CONTROLADOR] Sistema de turnos iniciado.")

loop_activo = True
while loop_activo:
    msg = dgram.receive_from(cola, timeout=1)
    if msg != None:                      
        if msg.hdr["tipo"] == "turno":
            tecnico = msg.sdu["tecnico"]
            sector = msg.sdu["sector"]
            
            sector_existe = sector in sectores_validos
            if sector_existe:
                if dgram.cant_cola(f"agenda:{sector}") > 0:
                    turno_mpdu = dgram.receive_from(f"agenda:{sector}", timeout=1)
                    turno_asignado = turno_mpdu.sdu
                    print(f"[CONTROLADOR] Turno asignado a {tecnico} para {sector} a las {turno_asignado}")
                    mensaje_respuesta = turno_asignado
                else:
                    mensaje_respuesta = "no hay disponibilidad"
                    print(f"[CONTROLADOR] Turno rechazado para {tecnico} ({sector}) - no hay disponibilidad")
            else: 
                mensaje_respuesta = "Especialidad INEXISTENTE"
                print(f"[CONTROLADOR] Turno rechazado para {tecnico} ({sector}) - Especialidad INEXISTENTE")
            respuesta = MPDU(
                hdr={"tipo": "respuesta_turno"},
                sdu={"turno": mensaje_respuesta}
            )
            dgram.send_to(f"respuesta_{tecnico}", respuesta)
    
    if not control.is_alive():
        print("[CONTROLADOR] Sistema finalizado.")
        loop_activo = False