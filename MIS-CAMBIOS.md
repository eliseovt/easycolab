# Mis cambios sobre EasyColab

Este repositorio es un fork personal de [wy51ai/easycolab](https://github.com/wy51ai/easycolab).
Aquí se registra cada cambio propio: qué se hizo, por qué y qué archivos se tocaron, para poder
seguir trayendo las mejoras del autor original sin perder el hilo.

## Cómo traer las mejoras del autor original

```powershell
git fetch upstream
git merge upstream/master
```

Si hay conflictos, este archivo indica qué archivos tocamos nosotros y con qué intención,
para resolverlos rápido.

## Reglas para minimizar conflictos con upstream

1. **Preferir archivos nuevos** antes que editar los del autor (por ejemplo, un módulo propio
   que se importa desde un único punto, en vez de reescribir funciones existentes).
2. **Si hay que editar un archivo del autor**, hacer cambios pequeños y localizados, sin
   reformatear, reordenar ni renombrar código ajeno.
3. **No tocar** los README del autor (`README.md`, `README_EN.md`); la documentación propia
   va aquí o en archivos nuevos.
4. **Un commit por cambio**, con mensaje claro, para poder revertirlo o reaplicarlo por separado.
5. **Registrar aquí cada cambio** con la plantilla de abajo.

## Estado base

| Dato | Valor |
|---|---|
| Fork creado a partir de | `fcad66f` (upstream/master, versión `1.1.0`) |
| Fecha | 2026-11-22 |
| Plataforma principal de uso | Windows 11 |

---

## Registro de cambios

<!--
Plantilla para cada cambio (el más reciente arriba):

### AAAA-MM-DD · Título corto

**Qué se hizo:**
**Por qué:**
**Archivos tocados:**
- `ruta/archivo` (nuevo | modificado: qué parte)
**Notas para fusionar con upstream:**
-->

### 2026-11-22 · Fijar google-colab-cli a 0.7.5

**Qué se hizo:** `google-colab-cli>=0.7.5` pasa a `google-colab-cli==0.7.5` en los requisitos y en
la instalación automática que hace el cliente de Windows la primera vez.
**Por qué:** desde la 0.7.6 la librería guarda la sesión de Google en el almacén de credenciales
del sistema, borra `token.json` y quitó `TOKEN_CONFIG_PATH`. Con esas versiones
`colab_bridge.py` no arranca (ver la entrada "Entorno de desarrollo").
**Archivos tocados:**
- `requirements.txt` (modificado: 1 línea)
- `windows_app/requirements-windows.txt` (modificado: 1 línea)
- `windows_app/viewmodel_services.py` (modificado: 1 línea en `_resolve_python_for_bridge`)

**No se tocó:** `macos_app/` ni `windows_app/build_windows_from_mac.py` (no se usan).
**Verificado:** con el `.venv`, `colab_bridge.py auth_status` responde. También se compiló
`dist\EasyColab\EasyColab.exe` (267 MB, incluye colab-cli 0.7.5) y su `--bridge-cli auth_status`
responde. La interfaz abre y el login con Google funciona. «Wake & Deploy» probado con L4 (G4 y A100 sin stock): asigna la VM, sube app.py, conecta y la URL pública devuelve 401 sin credenciales (web y /v1/models).
**Cómo compilar sin tocar archivos del repo** (el script del autor regenera `AppIcon.ico`):

```powershell
.\.venv\Scripts\pyinstaller.exe --noconfirm --clean --distpath dist --workpath build\pyinstaller windows_app\EasyColab.spec
```

**Notas para fusionar con upstream:** si el autor adapta `colab_bridge.py` a la 0.8 (sin
`TOKEN_CONFIG_PATH`), quedarse con su versión y quitar este fijado.

### 2026-11-22 · Entorno de desarrollo en Windows (.venv)

**Qué se hizo:** se creó `.venv` (Python 3.12, ignorado por git) con
`windows_app/requirements-windows.txt` y `pytest`.
**Por qué:** poder probar y compilar el cliente de Windows sin tocar el Python del sistema.
**Hallazgo:** `google-colab-cli` 0.7.6 y 0.8.0 guardan el token de Google en el almacén de
credenciales del sistema y borran `~/.config/colab-cli/token.json`. Además quitaron
`TOKEN_CONFIG_PATH`, así que `colab_bridge.py` ni siquiera arranca con ellas. Los requisitos
(`>=0.7.5`) instalan hoy la 0.8.0, así que **una instalación limpia del autor está rota**.
En el `.venv` se instaló `google-colab-cli==0.7.5` (ahora fijado en los requisitos).
**Pruebas (`pytest tests`):** 6 pasan y 5 fallan (`TypeError: type 'object' is not subscriptable`
y otros), y la suite se queda colgada a mitad. El resultado es idéntico con el código original del
autor: no lo causan nuestros cambios.
**Archivos tocados:** ninguno del repo (solo `.venv/`, que no se sube).

Recrear el entorno:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r windows_app\requirements-windows.txt pytest
```

### 2026-11-22 · Quitar el espejo hf-mirror.com

**Qué se hizo:** las consultas a la API de HuggingFace (buscar modelos, ver detalles y leer el
README) ya solo van a `huggingface.co`. Antes, si fallaba, se repetía en `hf-mirror.com`.
**Por qué:** `hf-mirror.com` es un espejo no oficial de terceros pensado para China, y recibía
tu token de HuggingFace. Fuera de China no aporta nada.
**Archivos tocados (solo cambia la lista de hosts en cada bucle `for host in ...`):**
- `windows_app/viewmodel_services.py` (modificado: 3 líneas)
- `app.py` (modificado: 4 líneas; corre en Colab)
- `EasyColab_Server.ipynb` (modificado: 4 líneas; la copia de `app.py` del modo manual)
- `android_app/app/src/main/java/app/easycolab/studio/StudioViewModelServices.kt` (modificado: 3 líneas)

**No se tocó:** macOS e iOS (no se usan). Tampoco la regex de `app.py` que limpia URLs
`hf-mirror.com` pegadas por el usuario, porque no hace ninguna conexión.
**Notas para fusionar con upstream:** si hay conflicto en esas líneas, acepta la versión del
autor y vuelve a aplicar el cambio con:

```bash
sed -i 's/("https:\/\/huggingface.co", "https:\/\/hf-mirror.com")/("https:\/\/huggingface.co",)/' app.py windows_app/viewmodel_services.py
sed -i 's/(\\"https:\/\/huggingface.co\\", \\"https:\/\/hf-mirror.com\\")/(\\"https:\/\/huggingface.co\\",)/' EasyColab_Server.ipynb
sed -i 's/listOf("https:\/\/huggingface.co", "https:\/\/hf-mirror.com")/listOf("https:\/\/huggingface.co")/' android_app/app/src/main/java/app/easycolab/studio/StudioViewModelServices.kt
grep -rn 'hf-mirror.com")' app.py windows_app android_app EasyColab_Server.ipynb   # no debe mostrar nada
```

### 2026-11-22 · Auditoría de seguridad inicial (sin cambios de código)

**Qué se hizo:** revisión dirigida del cliente Windows (`windows_app/`), `colab_bridge.py`,
`runtime_auth.py`, `app.py`, dependencias y workflow de CI. Se buscaron destinos de red, manejo
de tokens, código ofuscado, ejecución dinámica, descargas remotas y autoactualizaciones.
**Por qué:** confirmar que es seguro usarlo y que no envía datos al autor.

**Resultado: no se encontró código malicioso ni envío de datos al autor.**
- No hay servidores del autor, telemetría propia ni autoactualización desde su repo.
- El código del servidor (`app.py`, `runtime_auth.py`) se sube a Colab **desde tu copia local**.
- El login de Google usa `google-colab-cli`, publicado por Google (attestation de PyPI verificada).
- Los servicios públicos (gradio.live / trycloudflare) van detrás de nginx con contraseña de ≥24 caracteres.

**Riesgos detectados (pendientes de decidir):**
1. ~~El token de HuggingFace se envía también a `hf-mirror.com` (espejo de terceros) cuando
   huggingface.co falla~~ → **resuelto** en "Quitar el espejo hf-mirror.com".
5. Los `.apk`/`.zip` de GitHub Releases los compila el autor en su máquina (no hay CI para
   Android), así que no se puede verificar que coincidan con el código. Para usar tus cambios,
   hay que compilar desde este fork.
2. Contraseñas de administración, token HF y clave API se guardan en texto plano en
   `%LOCALAPPDATA%\EasyColab`; el token de Google en `~/.config/colab-cli/token.json`.
3. En la VM se descargan versiones "latest" sin fijar (cloudflared, rclone, ComfyUI, pip).
4. Con cliente OAuth propio, el refresh token de Google se copia a la VM (nodos de ComfyUI podrían leerlo).

**No revisado a fondo:** `EasyColab_Server.ipynb` (solo búsqueda de URLs) y las apps de macOS/iOS/Android.
**Archivos tocados:**
- `MIS-CAMBIOS.md` (esta entrada)

### 2026-11-22 · Crear este registro de cambios

**Qué se hizo:** se creó `MIS-CAMBIOS.md` con las reglas del fork y la plantilla de registro.
**Por qué:** llevar un historial claro de los cambios propios y facilitar las fusiones con upstream.
**Archivos tocados:**
- `MIS-CAMBIOS.md` (nuevo)

**Notas para fusionar con upstream:** archivo propio; no puede chocar con los del autor.
