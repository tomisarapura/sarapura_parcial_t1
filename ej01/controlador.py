from _redisconnect import redisconnect

r = redisconnect()

cola_solicitudes_estudiantes = "Lab_solicitudes"  #Por acá llegan las solicitudes de los estudiantes, en un string "nombre,grupo"
cola_espera_estudiantes = "Lab_espera"            #Acá quedan en espera hasta que se les asigne la estación
cola_estaciones_libres = "Lab_estaciones_libres"  #Acá se almacenan las estaciones disponibles
cola_liberacion = "Lab_liberacion"                #Acá se cargan las estaciones una vez liberadas
cola_termina = "Lab_termina"                      #Acá llega la señal de termina.py

r.rpush(cola_estaciones_libres, "1")
r.rpush(cola_estaciones_libres, "2")

print("[CONTROLADOR] Iniciado.")

loop_activo = True
    
while loop_activo:
    solicitud_recibida = r.blpop(cola_solicitudes_estudiantes, timeout=1)
    if solicitud_recibida:
        solicitud = solicitud_recibida[1]
        r.rpush(cola_espera_estudiantes, solicitud)
        
    cantidad_en_espera = r.llen(cola_espera_estudiantes) 
    estaciones_libres = r.llen(cola_estaciones_libres)

    if cantidad_en_espera > 0 and estaciones_libres > 0:
        estudiantes_revisados = 0
        while estudiantes_revisados < cantidad_en_espera and estaciones_libres > 0: #Si quedan estudiantes sin revisar y estaciones libres
            estudiante = r.lpop(cola_espera_estudiantes)
            
            if estudiante:
                estudiante_separado = estudiante.split(",")
                nombre = estudiante_separado[0]
                grupo = estudiante_separado[1]
                grupo_clave = f"Lab_grupo_{grupo}"
                grupo_ocupado = r.exists(grupo_clave)
                asignado = False
                
                if not grupo_ocupado:                                               #Si el grupo_clave no aparece en exists, nadie de ese grupo tiene asignado una estación
                    estacion_disponible = r.lpop(cola_estaciones_libres) 

                    if estacion_disponible:
                        r.set(grupo_clave, "1")
                        r.set(f"Lab_estacion_ocupada_{estacion_disponible}", f"{nombre} (Grupo {grupo})")
                        r.rpush(f"Lab_respuesta_{nombre}", estacion_disponible)
                        print(f"[CONTROLADOR] {nombre} del grupo {grupo} asignado a estación {estacion_disponible}")
                        
                        asignado = True
                        estaciones_libres = estaciones_libres - 1
                
                if not asignado:
                    r.rpush(cola_espera_estudiantes, estudiante)
                    
            estudiantes_revisados = estudiantes_revisados + 1

    cantidad_liberaciones = r.llen(cola_liberacion)

    for i in range(cantidad_liberaciones):
        liberacion_recibida = r.lpop(cola_liberacion)               #Recibe el string separado por comas
        liberacion_separado = liberacion_recibida.split(",")        #Lo separo en una lista para asignar
        nombre_libera = liberacion_separado[0]                      #Asigno
        grupo_libera = liberacion_separado[1]                       #Asigno
        estacion_liberada = liberacion_separado[2]                  #Asigno
        print(f"[CONTROLADOR] Estación {estacion_liberada} liberada por {nombre_libera}")
        r.rpush(cola_estaciones_libres, estacion_liberada)          #Vuelve a sumar a la estacion a la cola de estaciones libres
        r.delete(f"Lab_grupo_{grupo_libera}")                       #Elimina la clave del grupo para que no salte en r.exists
        r.delete(f"Lab_estacion_ocupada_{estacion_liberada}")       #Elimina la clave de la estación ocupada para que el estado lo marque como libre

    if r.exists(cola_termina):                                      #Si termina.py creo la clave, se cambio el estado de loop_activo y termina el bucle
        loop_activo = False


r.delete(cola_estaciones_libres)
r.delete(cola_solicitudes_estudiantes)
r.delete(cola_espera_estudiantes)
r.delete(cola_liberacion)
r.delete(cola_termina)

claves_estaciones = r.keys("Lab_estacion_ocupada_*")

if claves_estaciones:
    for clave in claves_estaciones:
        r.delete(clave)

claves_grupos = r.keys("Lab_grupo_*")

if claves_grupos:
    for clave in claves_grupos:
        r.delete(clave)
r.delete("Lab_termina")

print("[CONTROLADOR] Finalizando.")
r.close()
print("[CONTROLADOR] Sistema detenido")