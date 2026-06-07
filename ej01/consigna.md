# Ejercicio 01: Laboratorio Fotografico Distribuido

## Objetivo

Implementar un sistema distribuido que coordine el acceso concurrente a estaciones de edicion fotografica utilizando Redis como mecanismo de sincronizacion.

## Contexto

Distintos estudiantes solicitan utilizar estaciones de edicion. Cada estudiante pertenece a un grupo. El sistema debe permitir el uso concurrente de estaciones, respetando restricciones entre grupos.

El controlador administra las estaciones disponibles y la cola de espera.

Al finalizar la edicion, el estudiante libera el recurso.

La validacion de concurrencia entre grupos debe realizarse utilizando informacion compartida en Redis.

La solucion debe funcionar correctamente aunque los procesos se ejecuten desde terminales independientes.

Las estaciones, la cola de espera y cualquier estado compartido deben administrarse mediante Redis, no en memoria local del controlador.

## Reglas del sistema

1. Existen dos estaciones de edicion.
2. Cada estudiante solicita acceso indicando su nombre y grupo.
3. No pueden editar simultaneamente dos estudiantes del mismo grupo.
4. El controlador administra las estaciones disponibles y la cola de espera.
5. Al finalizar la edicion, el estudiante libera el recurso.
6. La validacion de concurrencia entre grupos debe realizarse usando informacion compartida en Redis.
7. Las estaciones, la cola de espera y cualquier estado compartido deben administrarse mediante Redis.
8. La solucion debe funcionar correctamente aunque los procesos se ejecuten desde terminales independientes.

## Archivos a desarrollar

- `controlador.py`: coordina el acceso a las estaciones, administra la cola de espera y valida restricciones entre grupos.
- `estudiante.py`: proceso distribuido que solicita acceso, realiza la edicion y libera el recurso.
- `estado.py`: consulta y muestra el estado actual del sistema: estaciones ocupadas, estudiantes activos y cola de espera.
- `_redisconnect.py`: centraliza la configuracion y conexion a Redis.
- `termina.py`: envia la senal de finalizacion y libera recursos para detener la simulacion.

## Ejecucion de prueba

```bash
python controlador.py
python estudiante.py juan A
python estudiante.py maria B
python estudiante.py pedro A
python estado.py
```

## Finalizacion

```bash
python termina.py
```

Cada archivo es un proceso independiente. Ejecutar desde distintas terminales.

## Auditoria de cumplimiento

### Cumple

- Dos estaciones de edicion: `controlador.py` define `NUM_ESTACIONES = 2`, limpia la cola de estaciones libres al iniciar y carga dos estaciones en Redis.
- Solicitud con nombre y grupo: `estudiante.py` recibe nombre y grupo por argumentos y envia ambos a Redis.
- No editar simultaneamente dos estudiantes del mismo grupo: `controlador.py` usa claves Redis `Lab_grupo_<grupo>` para bloquear grupos activos y las elimina cuando el estudiante libera la estacion.
- El estudiante libera el recurso al finalizar: `estudiante.py` envia la liberacion y `controlador.py` vuelve a cargar la estacion liberada en la cola de estaciones libres.
- Validacion de concurrencia entre grupos en Redis: la validacion consulta claves Redis y las actualiza al asignar o liberar estaciones.
- Controlador administra estaciones y cola de espera: usa listas Redis para solicitudes, espera y estaciones libres, y registra las estaciones ocupadas en Redis.
- Estado compartido administrado mediante Redis: la cola, las estaciones libres y las estaciones ocupadas estan en Redis.
- Funcionamiento desde terminales independientes: los procesos se comunican por Redis y el estado de estaciones ocupadas queda disponible para otros procesos.
- `termina.py` finaliza y libera recursos: envia la senal, borra explicitamente las colas y claves Redis del ejercicio, y cierra la conexion a Redis.
- `estado.py` muestra estado actual: muestra estaciones ocupadas, estaciones libres y cola de espera consultando claves Redis.

### Cumple parcialmente

No se detectan puntos de cumplimiento parcial en la auditoria actual.

### No cumple

No se detectan puntos incumplidos en la auditoria actual.
