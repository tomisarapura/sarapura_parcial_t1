from _redisconnect import redisconnect

r = redisconnect()

print("\n=== ESTADO DEL SISTEMA ===")

for i in range(1, 3):
    ocupante = r.get(f"Lab_estacion_ocupada_{i}")
    if ocupante:
        estado = f"Ocupada por {ocupante}"
    else:
        estado = "Libre"
    print(f"Estación {i}: {estado}")

lista_espera = r.lrange("Lab_espera", 0, -1)

if lista_espera:
    print("En cola de espera:")
    for solicitud in lista_espera:
        solicitud_separada = solicitud.split(",")
        nombre = solicitud_separada[0]
        grupo = solicitud_separada[1]
        print(f"[{nombre}] (Grupo {grupo})")
else:
    print("Cola de espera vacía.")