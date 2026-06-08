from _redisconnect import redisconnect
import time

r = redisconnect()
cola_espera_estudiantes = "Lab_espera"
NUM_ESTACIONES = 2

print("\n=== ESTADO DEL SISTEMA ===")

for i in range(1, NUM_ESTACIONES + 1):
    ocupante = r.get(f"Lab_estacion_ocupada_{i}")
    if ocupante:
        print(f"Estación {i}: Ocupada por {ocupante}")
    else:
        print(f"Estación {i}: Libre")

cantidad_en_espera = r.llen(cola_espera_estudiantes)
if cantidad_en_espera == 0:
    print("Cola de espera vacía.")
else:
    print("En cola de espera:")
    lista_espera = r.lrange(cola_espera_estudiantes, 0, -1)
    for solicitud in lista_espera:
        nombre_est, grupo_est = solicitud.split(",")
        print(f"  - {nombre_est} (Grupo {grupo_est})")
