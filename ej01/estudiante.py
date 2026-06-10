import sys
import time
import random

from _redisconnect import redisconnect

r = redisconnect()

nombre_estudiante = sys.argv[1] if len(sys.argv) > 1 else "EstudianteX"
grupo_estudiante = sys.argv[2] if len(sys.argv) > 2 else "A"

cola_solicitudes_estudiantes = "Lab_solicitudes"
cola_respuesta_estudiante = f"Lab_respuesta_{nombre_estudiante}"
cola_liberacion = "Lab_liberacion" 
cola_termina = "Lab_termina"

print(f"[{nombre_estudiante}] Esperando asignación...")

solicitud = f"{nombre_estudiante},{grupo_estudiante}"
r.rpush(cola_solicitudes_estudiantes, solicitud)

loop_activo = True

while loop_activo:
    respuesta_recibida = r.blpop(cola_respuesta_estudiante, timeout = 1)
    if respuesta_recibida:

        num_estacion = respuesta_recibida[1]

        print(f"[{nombre_estudiante}] Asignado a estación {num_estacion}. Editando...")
        time.sleep(random.randint(2, 5))                                                  #Fingimos el tiempo que usamos la estacion
        mensaje_liberacion = f"{nombre_estudiante},{grupo_estudiante},{num_estacion}"
        r.rpush(cola_liberacion, mensaje_liberacion)                                      #Cargamos en la cola de liberación la info de la estación que se termina de usar 
        print(f"[{nombre_estudiante}] Edición finalizada.")
        loop_activo = False                                                               #Corta  el loop después de usar la estación porque no tiene nada más que hacer

    if r.exists(cola_termina):
        loop_activo = False
        print(f"[{nombre_estudiante}]: Señal recibida. Terminando")

r.close()