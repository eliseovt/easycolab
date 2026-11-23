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

### 2026-11-23 · Traducir la barra de progreso en vivo (Windows y Android)

**Qué se hizo:** nueva regla que traduce al español las barras de progreso que `app.py` escribe en
chino en «Registros», por ejemplo
`DiT 去噪采样:  98%|##########| 49/50 [00:18<00:00, 0.36s/step] · 总进度 88%` →
`Muestreo DiT: 98%|##########| 49/50 [00:18<00:00, 0.36s/paso] · total 88%`.
Cubre las 8 variantes de `ACTIVE_TQDM_BARS["sampling"]`: muestreo DiT, codificación de prompt,
decodificación VAE de imagen/video/audio, empaquetado MP4 y MiniMax-H3-Image.
**Por qué:** era la única línea del registro que seguía en chino al generar una imagen.
**Archivos tocados:**
- `windows_app/i18n_es.py` (propio: `_BAR_LABELS_ZH_TO_ES`, `_BAR_TAIL_RULES_ZH_TO_ES`, `_translate_progress_bar` y la primera regla de `SERVER_REGEX_ZH_TO_ES`)
- `android_app/app/src/main/java/app/easycolab/studio/LocalizationEs.kt` (propio: lo mismo en Kotlin)

**Verificado:** las 8 variantes salen sin chino en Windows (Python) y en Android (clases Kotlin
compiladas, ejecutadas en la JVM). En inglés y chino no cambia nada. APK recompilado.
**Notas para fusionar con upstream:** solo archivos propios. Si el autor cambia el formato de esas
barras en `app.py`, ajustar las reglas.

### 2026-11-23 · Corregir el texto del botón «Generar» al cambiar la cantidad por lote

**Qué se hizo:** al elegir 1x/2x/3x/4x en «Cantidad por lote», ahora se refresca toda la vista
(`_refresh_all_state()`) en lugar de solo los botones de cantidad.
**Por qué:** fallo del autor. El botón grande seguía mostrando la cantidad anterior (p. ej.
«Generar 2x imágenes HD» con 1x seleccionado), aunque se generaba la cantidad correcta.
**Archivos tocados:**
- `windows_app/main_window.py` (modificado: 1 línea en `_set_batch_count`)

**Verificado:** con la ventana fuera de pantalla, en español, inglés y chino, con Qwen-Image-2.1 y
MiniMax-H3, el texto cambia al instante (1x → «Generar imagen», 2x → «Generar 2x imágenes HD», etc.).
**Notas para fusionar con upstream:** si el autor lo corrige por su cuenta, quédate con su versión.

### 2026-11-22 · Añadir idioma español a la app Android

**Qué se hizo:** Se añadió el español (`"es"`, `AppLanguage.ES`) como tercer idioma en la app móvil Android (`android_app/`), con cambio cíclico `ZH → ES → EN → ZH` desde la barra superior, chip `Español` en Ajustes junto a `中文` y `English`, persistencia en `SharedPreferences` (`"easycolab_prefs"`), traducción completa de llamadas `L()`, catálogo de modelos, resoluciones, plantillas, paquetes ComfyUI, descripciones de fragmentos y mensajes del servidor/puente (`ColabNativeBridge.kt` y `app.py`), respetando prefijos `[HH:MM:SS]` y emojis iniciales como `⏳` (`U+2300–U+23FF`).

**Por qué:** Permitir usar la app Android en español latinoamericano neutro con el mismo glosario que el cliente de Windows (`windows_app/i18n_es.py`), reduciendo al mínimo los conflictos al fusionar `upstream/master`.

**Archivos tocados:**
- `android_app/app/src/main/java/app/easycolab/studio/LocalizationEs.kt` (nuevo: 1255 líneas; `fromCode`, ciclo `ZH → ES → EN → ZH`, diccionario `EN_TO_ES`, 63 plantillas `EN_REGEX_TO_ES`, traducciones de fragmentos y reglas chino→español `SERVER_EXACT_ZH_TO_ES` / `SERVER_REGEX_ZH_TO_ES` con fallback al inglés)
- `android_app/app/src/main/java/app/easycolab/studio/LocalizationAndModels.kt` (modificado, +21/-7 líneas: enum `ES("es")`, `isEN` como `lang != AppLanguage.ZH`, `LanguageManager.init/toggle`, `L()`, rango `U+2300..U+23FF` en `stripEmoji`, hooks en `localizeModelFileDesc`, `localizeServerText` y `ComfyPresetPackItem`)
- `android_app/app/src/main/java/app/easycolab/studio/MainActivity.kt` (modificado, +1/-0 línea: llamada temprana `LanguageManager.init(applicationContext)` en `onCreate`)
- `android_app/app/src/main/java/app/easycolab/studio/WorkspaceViews.kt` (modificado, +2/-2 líneas: etiqueta dinámica del botón de idioma mediante `nextLangButtonLabel` y `localizeServerText(vm.statusMessage)` en la barra inferior)
- `android_app/app/src/main/java/app/easycolab/studio/StudioCloudAndSettingsViews.kt` (modificado, +10/-6 líneas: selector en Ajustes con los 3 chips `中文`, `Español` y `English`)

**No se tocó:** `windows_app/`, `macos_app/`, `ios_app/`, `app.py` ni `colab_bridge.py`. Archivos locales ignorados por git creados para compilar: `android_app/local.properties`, `android_app/.signing/` y el APK en `EasyColab-Android.apk`.

**Verificado:**
- Script temporal de cobertura sobre los `.kt` de `android_app/`: `0` apariciones de `vídeo`/`Vídeo`; `239/239` llamadas literales a `L()`, `56/56` plantillas con variables y `65/65` textos del catálogo/resoluciones/modos cubiertos (`0` sin cubrir).
- Test JVM temporal compilado con JDK 17 contra las clases release compiladas: ciclo `ZH → ES → EN → ZH`, `fromCode`, `L()`, `formatDuration`, `localizeModelFileDesc`, `stripEmoji("⏳ ...")`, fallback chino→inglés y traducción en modo `ES` de las líneas reales del servidor (reintento HTTP 503 con y sin `⏳`, liberación con tasa CU/h y `[22:24:16] [RAMDisk ...]`).
- Compilación Release con JDK 17 (`C:\Program Files\Microsoft\jdk-17.0.21.102-hotspot`) vía `.\gradlew.bat assembleRelease` (`BUILD SUCCESSFUL`) y copia a `EasyColab-Android.apk` (2 827 544 bytes).

**Notas para fusionar con upstream:**
- Si el autor añade nuevas cadenas en `L(zh, en)` sin actualizar `LocalizationEs.kt`, `L()` y `localizeServerText()` hacen fallback automático al inglés y nunca muestran texto vacío ni dejan el mensaje en chino si existe regla inglesa.
- En caso de conflicto en `LocalizationAndModels.kt`, `WorkspaceViews.kt` o `StudioCloudAndSettingsViews.kt`, basta conservar el enum `ES("es")`, `isEN = lang != AppLanguage.ZH`, las llamadas puntuales a `LocalizationEs.*` y el tercer `FilterChip`.

### 2026-11-22 · Añadir idioma español al cliente de Windows

**Qué se hizo:** Se añadió el español (`"es"`) como tercer idioma seleccionable en el cliente de escritorio para Windows, con cambio cíclico `中文 → ES → EN → 中文` desde la barra superior y desde la guía inicial, persistencia en `settings.json`, traducción de la interfaz (`tr()`), etiquetas dinámicas, mensajes de `colab_bridge.py` / `app.py` y líneas del panel «Run Logs» (respetando `[HH:MM:SS]`).
**Por qué:** Permitir usar todo el cliente de Windows en español manteniendo la capacidad de fusionar cambios de `upstream/master` con el mínimo de conflictos posible.
**Archivos tocados:**
- `windows_app/i18n_es.py` (nuevo: normalización y ciclo de idioma, diccionario `EN_TO_ES`, plantillas regex `EN_REGEX_TO_ES`, reglas chino→español `SERVER_EXACT_ZH_TO_ES` y `SERVER_REGEX_ZH_TO_ES` para `colab_bridge.py` y `app.py`, y helpers de cambio en vivo)
- `windows_app/models.py` (modificado: import de `i18n_es`, `is_en()` como «no chino», `set_lang` (también carga la traducción de Qt), `tr`, `localize_shard_desc`, `localize_server_text` con conservación de `[HH:MM:SS]` y fallback en inglés, y `ModelFileItem.desc`)
- `windows_app/viewmodel.py` (modificado: carga/guardado y ciclo de `"es"`, delegación de `_translate_default_runtime_strings` y traducción de líneas en `append_console_line`, `_apply_status_response` y `_poll_colab_job`, además de `cancel_current_generation`)
- `windows_app/main_window.py` (modificado: etiqueta/tooltip de `lang_btn` mediante `lang_button_info`, palabras clave de coloración de terminal en español en `_refresh_console` y ancho fijo del botón «Mask» de 58 a 68 px)
- `windows_app/onboarding_dialog.py` (modificado: etiqueta/tooltip de `lang_btn` mediante `lang_button_info`)

**No se tocó:** `colab_bridge.py`, `app.py`, `windows_app/EasyColab.spec`, `windows_app/assets/AppIcon.ico`, `macos_app/`, `ios_app/` ni `android_app/`.
**Verificado:**
- `py_compile` de todos los archivos nuevos y modificados: sin errores.
- Comprobación AST sobre `windows_app/*.py`: 450 llamadas literales a `tr()` (432 traducidas al español; 18 conservadas idénticas al inglés por ser siglas/términos técnicos o unidades breves como `Drive`, `Seed`, `VRAM`, `RAM`, `GGUF`, `LLM / VLM`, `API Key`, `Play`, `Mute`, `15/30/60 min`, `[Img]`, `[Vid]`) y 101 llamadas dinámicas/f-strings cubiertas por `EN_REGEX_TO_ES` y tablas del catálogo.
- Arranque con `QT_QPA_PLATFORM=offscreen` en modo `"es"`, construcción de `EasyColabMainWindow` y `ColabGuideDialog` (4 pasos), ciclo de 3 cambios de idioma (`es → zh → en → es`), conservación de `[HH:MM:SS]` en `append_console_line` y medición con `QFontMetrics`.
- `pytest tests` (con timeout de 25 s por el cuelgue preexistente en `test_keepalive_daemon_exits_promptly_when_parent_stdin_closes`; excluyéndolo: 10 pasan, 8 fallan por incompatibilidades preexistentes de rutas/permisos en Windows, 3 omitidos).
- Compilación de `dist\EasyColab\EasyColab.exe` (260,2 MB totales en `dist\EasyColab`) mediante `.\.venv\Scripts\pyinstaller.exe --noconfirm --clean --distpath dist --workpath build\pyinstaller windows_app\EasyColab.spec`: completada (`windows_app.i18n_es` incluido en el análisis y `--bridge-cli auth_status` responde `{"ok": true, "logged_in": false}`).
- Revisión posterior: el mensaje de reintento «⏳ … 算力池繁忙 …» seguía en chino porque `_LEADING_DECOR_RE`
  no quitaba el emoji ⏳ (U+23F3). Se añadió el rango U+2300–U+23FF. Comprobado con las líneas reales
  de la prueba de «Wake & Deploy», y el `.exe` se recompiló.
- Ajustes posteriores: «Tapar/Tapado» → «Ocultar/Oculto», «Unido» → «Superponer» y el orden del
  botón de idioma pasa a `中文 → ES → EN`. El botón «Mask» se amplió de 58 a 68 px porque «Ocultar»
  necesita 66 px (el «Masked» original en inglés ya se cortaba con 61 px). Medido con la fuente real
  de Windows: ningún botón de una línea queda más estrecho que su texto en la ventana ni en la guía.
- Botones y menús propios de Qt («Yes/Cancel» de los diálogos, menú de clic derecho en campos de
  texto, selector de archivos) salían en inglés. `i18n_es.apply_qt_translator()` carga el catálogo
  oficial `qtbase_es.qm` de PySide6 solo en modo español; `models.set_lang()` lo llama (1 línea).
  En chino e inglés no cambia nada.
- Ajuste de traducción en `windows_app/i18n_es.py`: «video» sin tilde, mayúsculas al estilo español, «Actualizar», «Carpeta de salida», «Reproducir / Abrir», «Plantillas», corrección de preposiciones/artículos y verificación de anchos de botones.

**Notas para fusionar con upstream:**
- Si el autor añade frases nuevas en `tr(zh, en)` sin tocar `i18n_es.py`, `tr()` hace fallback automático al inglés y nunca muestra texto vacío ni rompe la interfaz.
- Si hay conflictos en `models.py` o `viewmodel.py`, basta mantener el import `from windows_app import i18n_es` y reenganchar las llamadas puntuales a `i18n_es.*` y `localize_server_text(...)` en consola.

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
