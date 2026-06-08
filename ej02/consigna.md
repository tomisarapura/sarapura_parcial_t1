# Ejercicio 02: Gestion Distribuida de Turnos Tecnicos

## Objetivo

Implementar un sistema distribuido de asignacion de turnos utilizando Redis como mecanismo de coordinacion entre procesos concurrentes.

## Contexto

El controlador debe administrar una agenda inicial de sectores. Cada tecnico solicita una especialidad y recibe un turno disponible si existe. Una vez asignado, el turno se elimina de la agenda para evitar duplicaciones o inconsistencias concurrentes.

La agenda de turnos disponibles debe mantenerse persistida en Redis durante toda la ejecucion.

No se aceptan soluciones que almacenen la agenda en estructuras locales del controlador.

La asignacion y actualizacion de turnos debe realizarse sobre datos compartidos en Redis para garantizar consistencia entre procesos concurrentes.

## Reglas del sistema

1. Cada tecnico solicita atencion indicando su especialidad y su nombre.
2. Las solicitudes y respuestas deben serializarse utilizando las estructuras definidas en `datagram_modules.py`.
3. Cada sector posee una capacidad limitada de turnos de atencion.
4. No deben producirse asignaciones inconsistentes ni superposicion invalida de turnos.
5. Los recursos deben liberarse correctamente al finalizar cada operacion.
6. El controlador debe coordinar correctamente la asignacion.
7. El controlador debe administrar la agenda inicial de sectores indicada.
8. Cada tecnico solicita una especialidad y recibe un turno disponible si existe.
9. Una vez asignado, el turno se elimina de la agenda para evitar duplicaciones o inconsistencias concurrentes.
10. La agenda de turnos disponibles debe mantenerse persistida en Redis durante toda la ejecucion.
11. La agenda no debe almacenarse en listas, diccionarios u otras estructuras locales del controlador.

## Agenda de turnos

| Sector   | Turnos disponibles |
| -------- | ------------------ |
| Envasado | 08:00, 08:30       |
| Empaque  | 09:30              |
| Limpieza | 10:00, 10:30       |

## Archivos a desarrollar

- `controlador.py`: coordina la asignacion de turnos, administra disponibilidad y procesa solicitudes concurrentes.
- `tecnico.py`: proceso distribuido que solicita turnos y espera la asignacion correspondiente.
- `_redisconnect.py`: centraliza la configuracion y conexion a Redis.
- `termina.py`: finaliza la simulacion distribuida y libera recursos.
- `datagram_modules.py`: no se modifica; contiene estructuras auxiliares para mensajes.

## Ejecucion de prueba

python controlador.py
python tecnico.py carlos Envasado
python tecnico.py laura Empaque
python tecnico.py pedro Envasado
python tecnico.py ana Empaque
python tecnico.py oscar Almacen

## Finalizacion

python termina.py

Cada archivo es un proceso independiente. Ejecutar desde distintas terminales.
