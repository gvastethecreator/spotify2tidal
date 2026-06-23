# Spotify to Tidal GUI MVP Plan

## Auditoria del proyecto

- El proyecto actual es un CLI Python pequeno, publicado como paquete `spotify_to_tidal`.
- La sincronizacion real vive en `src/spotify_to_tidal/sync.py`; no conviene reescribirla para el MVP.
- La autenticacion vive en `src/spotify_to_tidal/auth.py` y ya abre navegador para Spotify/Tidal.
- La configuracion principal es YAML (`config.yml`), con ejemplo en `example_config.yml`.
- El CLI actual cubre todas las playlists, playlist puntual con `--uri`, favoritos con `--sync-favorites`, mappings desde `sync_playlists`, y ahora seleccion multiple desde GUI via `included_playlists`.
- La salida de progreso existe como `print`/`tqdm`, asi que la GUI debe capturar consola y mostrar log.
- Riesgos del estado actual: secretos en YAML local, dependencia de browser/device auth, archivos fijos `.session.yml`/`.cache.db`, y errores que pueden terminar el proceso con `sys.exit`.

## Self grill-me

1. Que tipo de GUI conviene?
   - Respuesta: web local servida por Python stdlib. Da mejor UX que Tkinter y no agrega dependencias.

2. Hay que reemplazar el CLI?
   - Respuesta: no. El CLI queda como fuente de verdad; la GUI lo envuelve.

3. Como se evita congelar la interfaz durante una sync larga?
   - Respuesta: ejecutar el CLI como subproceso y leer stdout/stderr en background.

4. Como se hace configurable desde UI sin inventar un editor YAML?
   - Respuesta: formularios para Spotify, modo de sync, favoritos, concurrencia, rate limit, exclusiones y mappings.

5. Como se soportan los modos reales desde dia cero?
   - Respuesta: `all`, `single`, `mapped`, `favorites`, traducidos a argumentos CLI y YAML temporal.

6. Que pasa si el usuario tiene mappings guardados pero quiere sincronizar todo?
   - Respuesta: en modo `all` la GUI crea un YAML temporal sin `sync_playlists`; no destruye el config guardado.

7. Hace falta cancelacion?
   - Respuesta: si, pero minima. Boton `Stop` que termina el subproceso.

8. Hace falta una base de datos nueva?
   - Respuesta: no. Se conserva `.cache.db`.

9. Hace falta backend nuevo tipo Flask/FastAPI?
   - Respuesta: no. `http.server` alcanza para una GUI local.

10. Como se prueba sin tocar Spotify/Tidal reales?
    - Respuesta: tests unitarios para parsing de mappings, seleccion de modo y construccion de argumentos.

11. Que queda fuera del MVP?
    - Respuesta: selector visual de playlists remoto, progreso estructurado por track, empaquetado instalador, y gestion avanzada de tokens.

12. Cual es el criterio de MVP listo?
    - Respuesta: abre en navegador, carga/guarda config, ejecuta sync real, muestra log, permite detener, pasa tests y tiene verificacion visual desktop/mobile.

13. Como se eligen playlists sin copiar IDs?
    - Respuesta: boton de Spotify que abre OAuth si hace falta, carga `GET /me/playlists`, lista las playlists y guarda la seleccion como `included_playlists`.

14. Que manejo de duplicados entra ahora?
    - Respuesta: detectar nombres duplicados de playlists en la lista y permitir saltar duplicados por nombre. Los tracks duplicados dentro de una playlist ya se ignoran durante el armado final.

## Plan completo

### MVP

- Agregar entrypoint `spotify_to_tidal_gui`.
- Servir una GUI local en `127.0.0.1`.
- Cargar `config.yml` o, si no existe, `example_config.yml`.
- Guardar configuracion desde la UI.
- Conectar Spotify desde UI y cargar playlists reales.
- Seleccionar varias playlists desde una lista filtrable.
- Detectar playlists con nombre duplicado y permitir saltarlas.
- Conectar Tidal desde UI usando el flujo OAuth/device de `tidalapi`.
- Ejecutar sync en subproceso con YAML temporal.
- Mostrar log y estado (`Ready`, `Running`, `Finished`, `Error`, `Stopping`).
- Permitir detener el proceso.
- Mantener el CLI actual compatible.

### UX

- Pantalla principal de dos columnas.
- Izquierda: configuracion y modos.
- Derecha: acciones, estado y log.
- Controles visibles para credenciales, redirect URI, browser auth, favoritos, concurrencia, rate limit, exclusiones y mappings.
- Responsive basico para mobile.

### Validacion

- Tests unitarios al final de la ronda.
- `python -m spotify_to_tidal.gui --no-browser` para verificar servidor.
- Playwright para inspeccion visual desktop y mobile.
- `python -m spotify_to_tidal --help` para confirmar que el CLI sigue vivo.

### Post-MVP

- Selector de playlists leyendo Spotify/Tidal autenticados.
- Progreso estructurado por playlist y track.
- Export de reporte de canciones no encontradas.
- Empaquetado con acceso directo local.
- Guardado opcional de config fuera del repo.
