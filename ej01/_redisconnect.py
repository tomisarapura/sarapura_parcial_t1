import redis
# Este archivo contiene la configuración de conexión a Redis.
# Cambiar el host, el puerto, el username y el password para usar la nube de redis 
# por el indicado en tu nube de redis

_dict_connect = {
    "host" : 'redis-13510.c82.us-east-1-2.ec2.cloud.redislabs.com',             # Cambiar a -> "redis-xxxxxx" para usar la nube de redis, donde redis-xxxxxx es el nombre de tu servidor redis
    "port" : 13510,                    # Cambiar el puerto para usar la nube de redis por el indicado en tu nube de redis
    "decode_responses" : True,        
    "username" : "default",                  # Cambiar a -> "default" para usar la nube de redis
    "password" : "xDfyeDeUEpAJqAJA8fjyOKg67dTr7LT5"                   # Cambiar password para usar la nube de redis 
}

# Función para conectarse a Redis
def redisconnect(decode_value=True):
    r = redis.Redis(
            host = _dict_connect ["host"],
            port = _dict_connect ["port"],
            decode_responses = _dict_connect ["decode_responses"],
            username = _dict_connect ["username"],
            password = _dict_connect ["password"]
        )
    return r

# -------------------------------------------------------------
# Función para verificar la conexión a Redis
# -------------------------------------------------------------
def check_redis():
    try:
        r = redisconnect()
        r.ping()
        print("Conexión a Redis exitosa")
        print("✅"*60)
    except redis.ConnectionError:
        print("Error de conexión a Redis")
        print("❌"*60)
    except Exception as e:
        print(f"Error inesperado: {e}")
        print("❌"*60)
    finally:
        try:
            r.close()
            print("Conexión a Redis cerrada")
        except Exception as e:
            print(f"Error al cerrar la conexión a Redis: {e}")
# -------------------------------------------------------------

if __name__ == "__main__":
    check_redis()

