import time

from _redisconnect import redisconnect

r = redisconnect()

r.rpush("Lab_termina", "TERMINAR")
print("[termina.py] Señal de terminación enviada")

time.sleep(7)

print("[termina.py] Recursos liberados")

r.close()
