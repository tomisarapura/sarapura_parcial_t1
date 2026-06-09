from _redisconnect import redisconnect

r = redisconnect()

cola_solicitudes_estudiantes = "Lab_solicitudes"
cola_espera_estudiantes = "Lab_espera"
cola_termina = "Lab_termina"
cola_liberacion = "Lab_liberacion"
estaciones_libres_queue = "Lab_estaciones_libres"

r.rpush(estaciones_libres_queue, "1")
r.rpush(estaciones_libres_queue, "2")

print("[CONTROLADOR] Iniciado.")

loop_activo = True
    
while loop_activo:
    solicitud_recibida = r.blpop(cola_solicitudes_estudiantes, timeout=1)
    if solicitud_recibida:
        solicitud = solicitud_recibida[1]
        r.rpush(cola_espera_estudiantes, solicitud)
        
    cantidad_en_espera = r.llen(cola_espera_estudiantes) 
    estaciones_libres = r.llen(estaciones_libres_queue)
    asignado = False

    if cantidad_en_espera > 0 and estaciones_libres > 0:
        estudiantes_revisados = 0
        while estudiantes_revisados < cantidad_en_espera and estaciones_libres > 0:
            estudiante = r.lpop(cola_espera_estudiantes)
            
            if estudiante:
                estudiante_separado = estudiante.split(",")
                nombre = estudiante_separado[0]
                grupo = estudiante_separado[1]
                grupo_clave = f"Lab_grupo_{grupo}"
                grupo_ocupado = r.exists(grupo_clave)
                asignado = False
                
                if not grupo_ocupado:
                    estacion_disponible = r.lpop(estaciones_libres_queue) 

                    if estacion_disponible:
                        r.set(grupo_clave, "1")
                        r.set(f"Lab_estacion_ocupada_{estacion_disponible}", f"{nombre} (Grupo {grupo})")
                        r.rpush(f"Lab_respuesta_{nombre}", estacion_disponible)
                        print(f"[CONTROLADOR] {nombre} del grupo {grupo} asignado a estación {estacion_disponible}")
                        
                        asignado = True
                        estaciones_libres -= 1 
                
                if not asignado:
                    r.rpush(cola_espera_estudiantes, estudiante)
                    
            estudiantes_revisados = estudiantes_revisados + 1

    cantidad_liberaciones = r.llen(cola_liberacion)

    for i in range(cantidad_liberaciones):
        liberacion_recibida = r.lpop(cola_liberacion)
        liberacion_separado = liberacion_recibida[1].split(",")
        nombre_libera = liberacion_separado[0]
        grupo_libera = liberacion_separado[1]
        estacion_liberada = liberacion_separado[2]
        print(f"[CONTROLADOR] Estación {estacion_liberada} liberada por {nombre_libera}")
        r.rpush(estaciones_libres_queue, estacion_liberada)
        r.delete(f"Lab_grupo_{grupo_libera}")
        r.delete(f"Lab_estacion_ocupada_{estacion_liberada}")

    if r.exists(cola_termina):
        loop_activo = False

r.delete(estaciones_libres_queue)
r.delete("Lab_solicitudes")
r.delete("Lab_espera")
r.delete("Lab_liberacion")
r.delete("Lab_estaciones_libres")
claves_estaciones = r.keys("Lab_estacion_ocupada_*")
if claves_estaciones:
    r.delete(*claves_estaciones)
claves_grupos = r.keys("Lab_grupo_*")
if claves_grupos:
    r.delete(*claves_grupos)
r.delete("Lab_termina")

print("[CONTROLADOR] Finalizando.")
r.close()

print("[CONTROLADOR] Sistema detenido")