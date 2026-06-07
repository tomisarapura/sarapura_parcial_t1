import time

from _redisconnect import redisconnect

r = redisconnect()

r.rpush("Lab_termina", "TERMINAR")
print("[termina.py] Señal de terminación enviada")

time.sleep(2)

r.delete("Lab_solicitudes")
r.delete("Lab_espera")
r.delete("Lab_liberacion")
r.delete("Lab_estaciones_libres")
r.delete("Lab_estacion_ocupada_1")
r.delete("Lab_estacion_ocupada_2")
r.delete("Lab_grupo_A")
r.delete("Lab_grupo_B")
r.delete("Lab_termina")

print("[termina.py] Recursos liberados")

r.close()
