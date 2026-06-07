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

| Sector | Turnos disponibles |
| --- | --- |
| Envasado | 08:00, 08:30 |
| Empaque | 09:30 |
| Limpieza | 10:00, 10:30 |

## Archivos a desarrollar

- `controlador.py`: coordina la asignacion de turnos, administra disponibilidad y procesa solicitudes concurrentes.
- `tecnico.py`: proceso distribuido que solicita turnos y espera la asignacion correspondiente.
- `_redisconnect.py`: centraliza la configuracion y conexion a Redis.
- `termina.py`: finaliza la simulacion distribuida y libera recursos.
- `datagram_modules.py`: no se modifica; contiene estructuras auxiliares para mensajes.

## Ejecucion de prueba

```bash
python controlador.py
python tecnico.py carlos Envasado
python tecnico.py laura Empaque
python tecnico.py pedro Envasado
python tecnico.py ana Empaque
python tecnico.py oscar Almacen
```

## Finalizacion

```bash
python termina.py
```

Cada archivo es un proceso independiente. Ejecutar desde distintas terminales.

## Auditoria de cumplimiento

### Cumple

- Solicitud con nombre y especialidad: `tecnico.py` toma nombre y sector por argumentos y los envia como solicitud.
- Serializacion con `datagram_modules.py`: `controlador.py` y `tecnico.py` usan `MPDU` y `Datagrama`.
- Agenda inicial indicada: `controlador.py` carga Envasado, Empaque y Limpieza con los turnos pedidos en listas Redis.
- Agenda persistida en Redis: los turnos se guardan en claves Redis `agenda:<sector>` durante la ejecucion.
- No usar agenda local en el controlador: la agenda no se mantiene en listas o diccionarios locales del controlador.
- Eliminar el turno asignado para evitar duplicaciones: `receive_from(f"agenda:{sector}")` extrae el turno de la lista Redis.
- Respuesta para especialidad inexistente o sin turnos: el controlador distingue entre especialidad inexistente y sector existente sin disponibilidad; el tecnico muestra `Solicitud rechazada: no hay disponibilidad` cuando corresponde.
- Recursos liberados al finalizar: `termina.py` detiene el sistema con `control.stop()`, espera la finalizacion y borra la clave de control con `control.delete()`.
- Finalizacion del controlador: el controlador sale cuando `ControlSistema.is_alive()` deja de indicar sistema activo.

### Cumple parcialmente

- Asignar turno disponible si existe: para sectores existentes con turnos disponibles asigna y elimina un turno de Redis.
- Evitar asignaciones inconsistentes o superposicion invalida: el uso de `BLPOP` sobre la lista Redis evita duplicar el mismo turno, pero la verificacion previa con `cant_cola` y el `BLPOP` posterior no son una unica operacion atomica.

### No cumple

- Configuracion Redis: en `ej02/_redisconnect.py`, `username` esta vacio aunque la consigna pide completar la conexion a Redis Cloud.
