import redis     # https://redis-py.readthedocs.io/en/stable/
from _redisconnect import _dict_connect 
from contextlib import contextmanager
from typing import Dict, Any, Optional, Generator, Type
import json      # Para serialización y deserialización con JSON

class ControlSistema: # Clase para manejar el control de sistemas
    def __init__(self,host:str="localhost", port: int=6379, dr:bool=True):
        self._redis_params: Dict[str, Any] = _dict_connect
        # self._redis_params: Dict[str, Any] = {
        #     'host': host,
        #     'port': port,
        #     'decode_responses': dr
        # }

    @contextmanager
    def redis_connection(self) -> Generator[redis.Redis, Any, Any]:
        """Context manager para conexión Redis."""
        connection: redis.Redis = redis.Redis(**self._redis_params)             # https://redis.io/docs/latest/develop/clients/redis-py/connect/
        try:
            yield connection
        finally:
            connection.close()
    
    def start(self, clave: str = "sistema") -> None:
        """Activa el sistema al enviar un mensaje a la cola de control."""
        with self.redis_connection() as r:
            r.rpush(clave, "activo") 
    def stop(self, clave: str = "sistema") -> None:    
        """Desactiva el sistema al enviar un mensaje a la cola de control."""
        with self.redis_connection() as r:
            r.rpush(clave, "inactivo")
    def is_alive(self, clave: str = "sistema") -> bool:
        """Retorna True si la cola existe y el contenido es 'activo', sino False."""
        valor = False
        with self.redis_connection() as r:
            if r.exists(clave) and r.llen(clave) > 0:
                if r.lindex(clave, 0) == "activo":
                    valor = True
        return valor
    def delete(self, clave: str = "sistema") -> None:
        """Elimina la cola del sistema."""
        with self.redis_connection() as r:
            r.delete(clave)

class MPDU:      # Message Protocol Data Unit - se pasa entre procesos
    '''
    Clase MPDU (Message Protocol Data Unit) que representa una unidad de datos de protocolo de mensaje.

    Atributos:
        hdr (str): Cabecera del mensaje, utilizada por el receptor.
        sdu (str): Unidad de datos de servicio, utilizada por la aplicación.

    Métodos:
        __init__(hdr: str = "data", sdu: str = ""):
            Constructor que inicializa los atributos hdr y sdu.
        hdr:
            Propiedad para obtener o establecer la cabecera del mensaje.
        sdu:
            Propiedad para obtener o establecer los datos de servicio.
        __str__() -> str:
            Representación en cadena del objeto MPDU.
        to_json() -> str:
            Serializa el objeto MPDU a una cadena JSON.
        from_json(serialized_obj: str) -> "MPDU":
            Método estático que deserializa un objeto MPDU desde una cadena JSON.
    '''
    def __init__(self, hdr: str = "data", sdu: str = ""):
        self._hdr = hdr   # header -  para el receptor
        self._sdu = sdu   # Service Data Unit  - para la aplicación

    @property
    def hdr(self) -> str: # establecer la cabecera del mensaje.
        return self._hdr

    @hdr.setter           # obtener la cabecera del mensaje.
    def hdr(self, value: str) -> None:
        self._hdr = value

    @property             # obtener los datos de servicio.
    def sdu(self) -> str:
        return self._sdu

    @sdu.setter           # establecer los datos de servicio.
    def sdu(self, value: str) -> None:
        self._sdu = value

    def __str__(self) -> str:
        return f"(Header: <{self._hdr}>, Data: <{self._sdu}>)"

    def to_json(self) -> str:
        """Serializar el objeto MPDU a una cadena JSON."""
        return json.dumps({"hdr": self._hdr, "sdu": self._sdu})

    @staticmethod
    def from_json(serialized_obj: str) -> "MPDU":
        """Deserializar un objeto MPDU desde una cadena JSON."""
        data = json.loads(serialized_obj)
        return MPDU(hdr=data["hdr"], sdu=data["sdu"])

class Datagrama: # Manejo  de comunicación
    '''
    Clase para manejar la comunicación con Redis utilizando datagramas.

    Esta clase proporciona métodos para enviar y recibir mensajes serializados
    como JSON a través de listas en Redis. También incluye un administrador de
    contexto para manejar conexiones Redis de manera segura.

    Atributos:
        _redis_params (Dict[str, Any]): Parámetros de configuración para la conexión Redis.

    Métodos:
        redis_connection() -> Generator[redis.Redis, Any, Any]:
            Context manager para establecer y cerrar conexiones con Redis.

        send_to(clave: str, mpdu: MPDU) -> None:
            Envía un MPDU serializado como JSON a una lista en Redis.

        receive_from_multiple(claves: list[str], timeout: int = 0) -> tuple[Optional[str], Optional[MPDU]]:

        receive_from(clave: str, timeout: int = 0) -> Optional[MPDU]:

        cant_cola(cola: str) -> int:
    '''
    def __init__(self,host:str="localhost", port: int=6379, dr:bool=True):
        self._redis_params: Dict[str, Any] = _dict_connect
        # self._redis_params: Dict[str, Any] = {
        #     'host': host,
        #     'port': port,
        #     'decode_responses': dr
        # }

    @contextmanager
    def redis_connection(self) -> Generator[redis.Redis, Any, Any]:
        """Context manager para conexión Redis."""
        connection: redis.Redis = redis.Redis(**self._redis_params)             # https://redis.io/docs/latest/develop/clients/redis-py/connect/
        try:
            yield connection
        finally:
            connection.close()

    def send_to(self, clave: str, mpdu: MPDU) -> None:
        """Enviar un MPDU serializado como JSON a una lista en Redis."""
        with self.redis_connection() as r:
            r.rpush(clave, mpdu.to_json())  # Usar JSON

    def receive_from(self, clave: str,timeout:int=0) -> Optional[MPDU]:
        """
        Bloquea hasta recibir un MPDU serializado como JSON desde la lista identificada por la clave.
        Devuelve el MPDU deserializado.
        """
        with self.redis_connection() as r:
            result = r.blpop(clave,timeout)
        if result is not None:
            _, serialized_mpdu = result
            res= MPDU.from_json(serialized_mpdu)
        else:
            res = None
        return res  
    
    def receive_from_multiple(self, claves: list[str],timeout:int=0) -> tuple[Optional[str], Optional[MPDU]]:
        """
        Bloquea hasta recibir un datagrama desde cualquiera de las listas 
        proporcionadas. Devuelve la lista de origen y el MPDU deserializado.
        """
        with self.redis_connection() as r:
            result = r.blpop(claves, timeout=timeout)
        if result is not None:
            lista_origen, serialized_mpdu = result
            m_pdu = MPDU.from_json(serialized_mpdu)
            return lista_origen, m_pdu
        return None, None
    
    def cant_cola(self, cola: str) -> int:
        """
        Devuelve la cantidad de mensajes en la cola especificada.
        """
        with self.redis_connection() as r:
            return r.llen(cola)

class Mutex:     # Exclusión mutua ...
    """
    Clase Mutex para implementar un mecanismo de exclusión mutua utilizando Redis.

    Esta clase utiliza una lista en Redis como cola de tokens para implementar
    un mecanismo de exclusión mutua distribuido. Permite que solo un proceso
    acceda a una sección crítica a la vez.

    Atributos:
        _redis_params (Dict[str, Any]): Parámetros de configuración para la conexión Redis.
        _mutex (str): Clave en Redis que identifica el mutex.
        _mutexQ (str): Clave en Redis que identifica la cola de tokens del mutex.

    Métodos:
        redis_connection() -> Generator[redis.Redis, Any, Any]:
            Context manager para establecer y cerrar conexiones con Redis.

        __init__(host: str = "localhost", port: int = 6379, dr: bool = True, id: str = "Mutex"):
            Constructor que inicializa el mutex en Redis.

        __enter__() -> None:
            Método para adquirir el mutex al entrar en un bloque `with`.

        __exit__(exc_type, exc_value, traceback) -> Optional[bool]:
            Método para liberar el mutex al salir de un bloque `with`.

        remove() -> None:
            Elimina el mutex y su cola de tokens de Redis.
    """
    @contextmanager
    def redis_connection(self) -> Generator[redis.Redis, Any, Any]:
        """Context manager para conexión Redis."""
        connection: redis.Redis = redis.Redis(**self._redis_params)
        try:
            yield connection
        finally:
            connection.close()

    def __init__(self, host: str = "localhost", port: int = 6379, dr: bool = True, id: str = "Mutex"):
        """
        Inicializa el mutex en Redis.

        Si el mutex no existe, lo crea junto con su cola de tokens.

        Args:
            host (str): Dirección del servidor Redis.
            port (int): Puerto del servidor Redis.
            dr (bool): Si se deben decodificar las respuestas de Redis.
            id (str): Identificador único para el mutex.
        """
        self._redis_params: Dict[str, Any] = _dict_connect
        # self._redis_params: Dict[str, Any] = {
        #     'host': host,
        #     'port': port,
        #     'decode_responses': dr
        # }
        self._mutex = "Mutex_redis_" + id
        self._mutexQ = "Mutex_Q_" + id
        with self.redis_connection() as r:
            
            if not r.exists(self._mutex):
                r.set(self._mutex, "existo")    # Inicializa el mutex (es un string en redis)
                r.lpush(self._mutexQ, "token")  # Inicializa la cola de tokens (es una lista en redis)
            #else:
                #print(f"Mutex {self._mutex} ya existe, no se inicializa.")
                # Si el mutex ya existe, no lo inicializa nuevamente.

    def __enter__(self) -> None:
        """
        Adquiere el mutex al entrar en un bloque `with`.
        Bloquea hasta que un token esté disponible en la cola del mutex.
        """
        with self.redis_connection() as r:
            r.blpop(self._mutexQ)            # Bloqueante, elimina de la lista por izquierda

    def __exit__(self, exc_type: Optional[Type[BaseException]],
                 exc_value: Optional[BaseException],
                 traceback: Optional[BaseException]) -> Optional[bool]:
        """
        Libera el mutex al salir de un bloque `with`.

        Args:
            exc_type (Optional[Type[BaseException]]): Tipo de excepción, si ocurre.
            exc_value (Optional[BaseException]): Valor de la excepción, si ocurre.
            traceback (Optional[BaseException]): Rastreo de la excepción, si ocurre.

        Returns:
            Optional[bool]: False para no suprimir excepciones.
        """
        with self.redis_connection() as r:            
            r.lpush(self._mutexQ, "token")   # Agrega por izquierda en la lista
            
        return False

    def remove(self) -> None:
        """
        Elimina el mutex y su cola de tokens de Redis.
        """
        with self.redis_connection() as r:
            r.delete(self._mutexQ, self._mutex)


