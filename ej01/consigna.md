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

python controlador.py
python estudiante.py juan A
python estudiante.py maria B
python estudiante.py pedro A
python estado.py

## Finalizacion

python termina.py

Cada archivo es un proceso independiente. Ejecutar desde distintas terminales.
