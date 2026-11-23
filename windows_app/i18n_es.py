"""
Spanish ("es") localization tables, regex templates, and server/bridge message
translators for the EasyColab Windows client.
"""
from __future__ import annotations

import re
from typing import Any, Callable, Dict, List, Sequence, Tuple

LANG_CYCLE: Tuple[str, ...] = ("zh", "es", "en")

_CJK_RE = re.compile(r"[\u4e00-\u9fff]")


def has_cjk(text: str) -> bool:
    return bool(_CJK_RE.search(text))
_TS_PREFIX_RE = re.compile(r"^(\[\d{2}:\d{2}:\d{2}\]\s*)(.*)$", re.DOTALL)
_LEADING_DECOR_RE = re.compile(
    r"^[\U0001F1E6-\U0001F1FF\U0001F300-\U0001FAFF\U00002300-\U000023FF\U00002600-\U000027BF\U0000FE0F\U0000200D\U000020E3\u2139\s]+"
)


def normalize_lang(lang: object) -> str:
    val = str(lang or "").strip().lower()
    if val.startswith("es"):
        return "es"
    if val.startswith("en"):
        return "en"
    return "zh"


def next_lang(lang: str) -> str:
    cur = normalize_lang(lang)
    idx = LANG_CYCLE.index(cur)
    return LANG_CYCLE[(idx + 1) % len(LANG_CYCLE)]


def lang_button_info(lang: str) -> Tuple[str, str]:
    cur = normalize_lang(lang)
    if cur == "zh":
        return ("ES", "切换界面为西班牙语 (Cambiar a español)")
    if cur == "es":
        return ("EN", "Cambiar interfaz a inglés (Switch to English)")
    return ("中文", "Switch UI to Chinese (切换为中文)")


_QT_TRANSLATOR: Any = None


def apply_qt_translator(lang: str) -> None:
    """Load Qt's own Spanish catalog (Yes/Cancel buttons, text-field context menus,
    file dialogs) while the UI is Spanish; remove it for any other language."""
    global _QT_TRANSLATOR
    try:
        from PySide6.QtCore import QCoreApplication, QLibraryInfo, QTranslator
    except Exception:
        return
    app = QCoreApplication.instance()
    if app is None:
        return
    if _QT_TRANSLATOR is not None:
        app.removeTranslator(_QT_TRANSLATOR)
        _QT_TRANSLATOR = None
    if normalize_lang(lang) != "es":
        return
    search_dirs = [QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)]
    try:
        import PySide6
        from pathlib import Path

        search_dirs.append(str(Path(PySide6.__file__).resolve().parent / "translations"))
    except Exception:
        pass
    translator = QTranslator(app)
    for folder in search_dirs:
        if folder and translator.load("qtbase_es", folder):
            app.installTranslator(translator)
            _QT_TRANSLATOR = translator
            return


# ─── English -> Spanish Static Dictionary (keys match exact tr(..., en) text) ─

EN_TO_ES: Dict[str, str] = {
    # Exact space-sensitive tags / prefixes
    "  [VRAM Ready]": "  [VRAM lista]",
    "[Gated] ": "[Con acceso] ",
    "[Img]": "[Img]",
    "[Vid]": "[Vid]",
    "[Missing]": "[Falta]",
    "Missing": "Falta",
    "[Ready]": "[Listo]",
    "─── Disconnecting & Releasing All Cloud GPU Runtimes ───": (
        "─── Desconectando y liberando todas las instancias GPU en la nube ───"
    ),
    "# PowerShell (Recommended on Windows)": "# PowerShell (recomendado en Windows)",
    # Top header & left sidebar controls
    "Dark": "Oscuro",
    "Light": "Claro",
    "Toggle Light / Dark studio theme": "Alternar tema claro / oscuro",
    "Guide": "Guía",
    "Colab Cloud Runtime": "Instancia Colab",
    "Offline": "Sin conexión",
    "Online": "En línea",
    "Google Account": "Cuenta Google",
    "Not Linked": "Sin vincular",
    "Not bound": "Sin vincular",
    "Connected": "Conectada",
    "Bind": "Vincular",
    "Refresh": "Actualizar",
    "Account": "Cuenta",
    "Switch Google Account...": "Cambiar cuenta de Google...",
    "Sign Out": "Cerrar sesión",
    "Paste OAuth code from browser": "Pega el código OAuth del navegador",
    "Submit": "Enviar",
    "Cancel": "Cancelar",
    "Wake & Deploy": "Activar GPU",
    "Deploying...": "Desplegando...",
    "Mask": "Ocultar",
    "Masked": "Oculto",
    "Privacy mask enabled": "Máscara de privacidad activa",
    "Stream/screenshot privacy mask: hide public tunnel URLs and account email": (
        "Máscara de privacidad para capturas: oculta URLs del túnel y tu correo"
    ),
    "Connect": "Conectar",
    "User: easycolab": "Usuario: easycolab",
    "Management password": "Clave admin",
    "Copy password": "Copiar",
    "Cloud GPU Not Connected": "GPU en la nube sin conectar",
    "Drive": "Drive",
    "Google Drive cloud persistence active": "Persistencia en Google Drive activa",
    "Overlay": "Superponer",
    "Split": "Separar",
    "Toggle between separate metric charts and combined overlay chart": (
        "Alternar entre gráficos separados o vista combinada"
    ),
    "GPU VRAM": "VRAM de GPU",
    "System RAM": "RAM del sistema",
    "Runtime Disk": "Disco de la instancia",
    # Card 2: CU & Idle Sleep
    "Compute Units & Auto-Sleep": "Créditos CU y reposo automático",
    "CU Balance": "Saldo CU",
    "Est. Balance": "Saldo est.",
    "Burn Rate": "Consumo",
    "Session Uptime": "Sesión",
    "Idle Auto-Release": "Liberar por inactividad",
    "15 min": "15 min",
    "30 min": "30 min",
    "60 min": "60 min",
    "Off": "No",
    "Idle auto-release is Off (remember to release runtime manually)": (
        "Auto-liberación desactivada (recuerda liberar la instancia al terminar)"
    ),
    "Release All Runtimes": "Liberar instancias",
    "Release All Colab Runtimes?": "¿Liberar todas las instancias Colab?",
    (
        "All active Colab GPU runtimes on your account will be terminated and billing will stop immediately.\n"
        "Confirm release now?"
    ): (
        "Se detendrán todas las instancias GPU de Colab activas en tu cuenta y el consumo parará al instante.\n"
        "¿Confirmas la liberación?"
    ),
    # Card 3: Open Model Center
    "Open Local Output Folder": "Abrir carpeta de salida",
    "Open Model Center": "Centro de modelos",
    "+ Add Custom HuggingFace Repo...": "+ Añadir repo de HuggingFace...",
    "HF Repo": "Repo HF",
    "Disk Weights": "Pesos en disco",
    "View Weight Shards (0)": "Ver fragmentos (0)",
    "Optional (for gated HF repos)": "Opcional (repos HF restringidos)",
    "1-Click Wake": "Activar en 1 clic",
    "Reconnect": "Reconectar",
    "Download": "Descargar",
    "Verify": "Verificar",
    "Load to VRAM": "Cargar en VRAM",
    "Reload VRAM": "Recargar VRAM",
    "Unload": "Quitar",
    "Unload All": "Quitar todo",
    "Unload current model from GPU VRAM": "Descargar modelo actual de la VRAM",
    "Canvas Status": "Estado del lienzo",
    "Stopped": "Detenido",
    "Starting...": "Iniciando...",
    "Online (Port 8188)": "En línea (puerto 8188)",
    "Launch ComfyUI": "Iniciar ComfyUI",
    "Open Canvas": "Abrir lienzo",
    "Stop": "Detener",
    # Card 4: Adaptive Params
    "Resolution & Sampling": "Resolución y muestreo",
    "Video Resolution": "Resolución de video",
    "Total Frames (4-15s)": "Fotogramas totales (4-15s)",
    "Sampling Steps": "Pasos de muestreo",
    "Aspect Ratio & Size": "Relación de aspecto y tamaño",
    "Denoising Strength": "Intensidad de redibujo",
    "Reasoning & Sampling": "Razonamiento y muestreo",
    "Enable Thinking Mode (CoT)": "Activar modo pensamiento (CoT)",
    "Reasoning Effort": "Nivel de razonamiento",
    "Low": "Bajo",
    "Med": "Medio",
    "High": "Alto",
    "XHigh": "Máx",
    "Context Window (up to 256K)": "Ventana de contexto (hasta 256K)",
    "Max Output Tokens (incl. CoT)": "Tokens máx. de salida (incl. CoT)",
    "Temperature": "Temperatura",
    "ComfyUI Persistence & Control": "Persistencia y control de ComfyUI",
    "Storage: Google Drive Auto-Symlink Persistence": (
        "Almacenamiento: persistencia automática por enlace en Google Drive"
    ),
    "Saved Nodes / Weights: 0 nodes · 0 weights": "Nodos / pesos guardados: 0 nodos · 0 pesos",
    "Canvas Queue: 0 running · 0 queued": "Cola del lienzo: 0 en curso · 0 en espera",
    "Free co-resident models VRAM before start": "Liberar VRAM de otros modelos antes de iniciar",
    "Sync Drive Now": "Sincronizar Drive",
    "Free VRAM Cache": "Liberar VRAM",
    "Seed": "Seed",
    "Random": "Aleatoria",
    "Batch Count": "Cantidad por lote",
    # Right Log Panel
    "Run Logs": "Registros",
    "Ready": "Listo",
    "Streaming": "En vivo",
    "Copy": "Copiar",
    "Clear": "Limpiar",
    "Copied all run logs to clipboard.": "Todos los registros copiados al portapapeles.",
    "VRAM": "VRAM",
    "RAM": "RAM",
    "Disk": "Disco",
    "Google Drive Auto-Symlink Persistence": "Persistencia automática por enlace en Google Drive",
    # Main Window / Workspace top bar & mode switcher
    "EasyColab — Cloud High-VRAM Multimodal AI Studio": (
        "EasyColab — Estudio multimodal en la nube de alta VRAM"
    ),
    "Open Multi-Model Cloud AI Studio": "Estudio multimodal abierto en la nube",
    "Presets": "Plantillas",
    "Output Folder": "Carpeta de salida",
    "User Guide": "Guía de uso",
    "Logs": "Registros",
    "Collapse / expand right live run log panel": "Mostrar u ocultar el panel derecho de registros",
    "Not Loaded in VRAM": "Sin cargar en VRAM",
    "VRAM Ready": "VRAM lista",
    "Active": "Activo",
    # Studio A: Video/Audio
    "Start & End Keyframe References": "Fotogramas clave de inicio y fin",
    "Upload a start frame and/or end frame (at least 1) for precise composition & camera transition": (
        "Sube un fotograma inicial o final (al menos 1) para controlar composición y transición"
    ),
    "Start Frame (Index 0)": "Fotograma inicial (índice 0)",
    "Drop or click to select start frame": "Arrastra o pulsa para elegir fotograma inicial",
    "End Frame (Optional · Index -1)": "Fotograma final (opcional · índice -1)",
    "Drop or click to select end frame": "Arrastra o pulsa para elegir fotograma final",
    "Camera & Multimodal Audio-Video Prompt": "Prompt de cámara y audio-video multimodal",
    "Describe visual subjects, camera motion, and lighting, plus synced soundscape/dialogue & background score": (
        "Describe sujetos, movimiento de cámara e iluminación, además de efectos, diálogos y música"
    ),
    "Visual & Camera Motion Prompt": "Prompt visual y movimiento de cámara",
    "Describe subject, framing, camera movement, and lighting...": (
        "Describe sujeto, encuadre, movimiento de cámara e iluminación..."
    ),
    "Soundscape & Dialogue (Optional)": "Ambiente sonoro y diálogos (opcional)",
    "e.g. Rhythmic train clatter over steel tracks, rustling leaves, soft spoken dialogue...": (
        "Ej.: traqueteo rítmico del tren sobre vías, hojas al viento, diálogo suave..."
    ),
    "Background Music Style (Optional)": "Estilo de música de fondo (opcional)",
    "e.g. Gentle nostalgic solo piano with warm acoustic guitar and ambient strings...": (
        "Ej.: piano solista suave y nostálgico con guitarra acústica y cuerdas..."
    ),
    "Generate": "Generar",
    "Generate Audio-Video (Ctrl+Enter)": "Generar audio-video (Ctrl+Enter)",
    "Generate Image (Ctrl+Enter)": "Generar imagen (Ctrl+Enter)",
    "Send & Start Deep Reasoning (Ctrl+Enter)": "Enviar e iniciar razonamiento (Ctrl+Enter)",
    # Studio B: ComfyUI
    "Cloud ComfyUI Fullscreen Node Canvas": "Lienzo de nodos ComfyUI en la nube",
    "1-click deploy ComfyUI + Manager over an encrypted Cloudflare HTTPS tunnel with desktop keepalive & auto-sleep": (
        "Despliega ComfyUI + Manager en 1 clic por túnel HTTPS Cloudflare con keepalive y reposo automático"
    ),
    "1-Click Launch Cloud ComfyUI & Open Fullscreen Canvas in Browser": (
        "Iniciar ComfyUI en la nube y abrir lienzo en el navegador"
    ),
    "Open Fullscreen Canvas in Browser": "Abrir lienzo en el navegador",
    "Copy Canvas URL": "Copiar URL del lienzo",
    "Copied ComfyUI public canvas URL to clipboard.": "URL pública de ComfyUI copiada al portapapeles.",
    "Restart ComfyUI": "Reiniciar ComfyUI",
    "Cloud ComfyUI not started": "ComfyUI en la nube no iniciado",
    "Canvas Online": "Lienzo en línea",
    "0 / 4 Packs Ready": "0 / 4 paquetes listos",
    "Preset I2V & First/Last-Frame Workflow Packs (1-Click Models + Guided Templates)": (
        "Paquetes predefinidos I2V y fotograma inicial/final (modelos + plantillas en 1 clic)"
    ),
    "Zero manual setup: 1-click high-speed download of official weights + ready-to-run guided workflow templates": (
        "Sin ajustes manuales: descarga rápida de pesos oficiales y plantillas listas para usar"
    ),
    "1. Click '1-Click Install Models & Workflows' below": (
        "1. Pulsa 'Instalar modelos y flujos' abajo"
    ),
    "2. Open 'Workflows' sidebar in ComfyUI & pick a template": (
        "2. Abre 'Workflows' en ComfyUI y elige una plantilla"
    ),
    "3. Upload 1-2 images & click 'Run' to generate": (
        "3. Sube 1 o 2 imágenes y pulsa 'Run' para generar"
    ),
    "1-Click Install Models & Workflows": "Instalar modelos y flujos",
    "Open in Canvas": "Abrir en el lienzo",
    "Rewrite Templates": "Reescribir plantillas",
    "Google Drive Auto-Symlink & Cross-Runtime Persistence": (
        "Enlace automático a Google Drive y persistencia entre sesiones"
    ),
    "Sync to Drive Now": "Sincronizar con Drive",
    "Cloud path: /content/drive/MyDrive/EasyColab_ComfyUI (auto-reused across fresh GPU runtimes)": (
        "Ruta en la nube: /content/drive/MyDrive/EasyColab_ComfyUI (se reutiliza entre instancias)"
    ),
    "models/* Weight Library": "models/* · biblioteca de pesos",
    "0 files": "0 archivos",
    "custom_nodes Extensions": "custom_nodes · extensiones",
    "0 nodes": "0 nodos",
    "workflows Saved Templates": "workflows · plantillas guardadas",
    "0 templates": "0 plantillas",
    "8-Thread High-Speed Weight Downloader to ComfyUI Drive": (
        "Descargador rápido de pesos en 8 hilos para ComfyUI Drive"
    ),
    "Paste a direct Hugging Face / Civitai URL, or enter an HF Repo ID + filename to pull directly into ComfyUI": (
        "Pega una URL directa de HuggingFace / Civitai o un Repo ID + archivo para bajarlo a ComfyUI"
    ),
    "Target Folder": "Carpeta de destino",
    "Direct URL https://... or HF Repo ID e.g. Kijai/WanVideo_comfy": (
        "URL directa https://... o Repo ID de HF, ej. Kijai/WanVideo_comfy"
    ),
    "Optional: subpath in repo or target filename (e.g. Wan2_2-I2V-14B.safetensors)": (
        "Opcional: subruta del repo o nombre final (ej. Wan2_2-I2V-14B.safetensors)"
    ),
    "8-Thread Download": "Descargar (8 hilos)",
    "No new outputs in cloud output/ folder": "Sin salidas nuevas en output/ de la nube",
    "Pull": "Bajar",
    # Studio C: Qwen LLM/VLM & API Gateway
    "Vision Input Images": "Imágenes de entrada para visión",
    "Drop 1-2 images for composition analysis, OCR extraction, or reverse-engineering T2I/T2V prompts": (
        "Suelta 1 o 2 imágenes para analizar composición, extraer OCR o deducir prompts T2I/T2V"
    ),
    "Input Image 1": "Imagen de entrada 1",
    "Drop or click to select image": "Arrastra o pulsa para elegir imagen",
    "Comparison Image 2 (Optional)": "Imagen comparativa 2 (opcional)",
    "Drop or click to select second image": "Arrastra o pulsa para elegir segunda imagen",
    "Prompt & Instruction Input": "Entrada de prompt e instrucciones",
    "Supports up to 256K context, deep chain-of-thought reasoning, architecture design & storyboards (Ctrl+Enter)": (
        "Soporta hasta 256K de contexto, razonamiento profundo, arquitectura y guiones (Ctrl+Enter)"
    ),
    "Enter your question, coding spec, or visual analysis prompt...": (
        "Escribe tu pregunta, especificación de código o análisis visual..."
    ),
    "API Gateway Setup": "Configurar pasarela API",
    "Clear Chat": "Limpiar chat",
    "Conversation & Deep Reasoning Transcript": "Conversación y razonamiento detallado",
    "Live streaming of chain-of-thought (Thinking Process) and final response": (
        "Transmisión en vivo del proceso de pensamiento y respuesta final"
    ),
    "No conversation yet. Enter a prompt or drop an image and press Ctrl+Enter to start reasoning.": (
        "Sin conversación aún. Escribe un prompt o suelta una imagen y pulsa Ctrl+Enter."
    ),
    "You": "Tú",
    "With Image": "Con imagen",
    "Copy Reply": "Copiar respuesta",
    "Copied model reply to clipboard.": "Respuesta del modelo copiada al portapapeles.",
    "Thinking & generating reply...": "Pensando y generando respuesta...",
    "Total API Requests: 0": "Peticiones API totales: 0",
    "API Gateway Authentication & Status": "Autenticación y estado de la pasarela API",
    "Keep API Key authentication enabled while the public tunnel is live to protect your Colab Compute Units (CU)": (
        "Mantén activa la autenticación por API Key mientras el túnel esté público para proteger tus CU"
    ),
    "Require API Key Auth (validates Bearer & x-api-key)": (
        "Exigir API Key (valida Bearer y x-api-key)"
    ),
    "API Key": "API Key",
    "Sync to Cloud": "Sincronizar",
    "Regenerate": "Regenerar",
    "Copy Key": "Copiar clave",
    "Copied API Key to clipboard.": "API Key copiada al portapapeles.",
    "API Key synced to cloud Colab gateway.": "API Key sincronizada con la pasarela de Colab.",
    "Generated a new random API Key.": "Se generó una nueva API Key aleatoria.",
    "OpenAI-Compatible Protocol": "Protocolo compatible con OpenAI",
    "Compatible with OpenAI SDK, Cursor, Cherry Studio, Chatbox & standard tools": (
        "Compatible con OpenAI SDK, Cursor, Cherry Studio, Chatbox y herramientas estándar"
    ),
    "Chat URL": "URL de chat",
    "Model ID": "ID de modelo",
    "Supports SSE streaming, reasoning_content CoT, image_url vision inputs & Function Calling; also serves /v1/images/generations when an image model is loaded.": (
        "Soporta streaming SSE, reasoning_content CoT, visión con image_url y Function Calling; también expone /v1/images/generations al cargar un modelo de imagen."
    ),
    "Copy Python SDK": "Copiar SDK Python",
    "Copied OpenAI Python snippet.": "Código Python de OpenAI copiado.",
    "Copy curl": "Copiar curl",
    "Copied OpenAI curl command.": "Comando curl de OpenAI copiado.",
    "Anthropic Messages Protocol": "Protocolo Anthropic Messages",
    "Native /v1/messages endpoint for Anthropic SDK & Claude Code CLI": (
        "Endpoint nativo /v1/messages para Anthropic SDK y Claude Code CLI"
    ),
    "Auth Header": "Cabecera",
    "x-api-key or Authorization: Bearer": "x-api-key o Authorization: Bearer",
    "Full Anthropic SSE streaming (thinking_delta, text_delta, tool_use blocks) plus /v1/messages/count_tokens.": (
        "Streaming SSE completo de Anthropic (thinking_delta, text_delta, tool_use) y /v1/messages/count_tokens."
    ),
    "Copy PowerShell Env": "Copiar env PowerShell",
    "Copied Windows PowerShell Claude Code env.": "Variables PowerShell para Claude Code copiadas.",
    "Copy Bash Env": "Copiar env Bash",
    "Copied Bash ANTHROPIC_BASE_URL env.": "Variables Bash ANTHROPIC_BASE_URL copiadas.",
    "Copy Anthropic curl": "Copiar curl Anthropic",
    "Copied Anthropic /v1/messages curl command.": "Comando curl de Anthropic /v1/messages copiado.",
    # API snippet prompt examples
    "Design a high-concurrency API gateway architecture": (
        "Diseña una arquitectura de pasarela API de alta concurrencia"
    ),
    "Explain quantum entanglement in three sentences": (
        "Explica el entrelazamiento cuántico en tres frases"
    ),
    "Explain the core advantages of Rust ownership": (
        "Explica las ventajas clave del sistema de ownership de Rust"
    ),
    # Studio D: Image
    "Instruction Edit / Img2Img Reference Images": "Imágenes de referencia para edición / Img2Img",
    "Upload source image(s) and enter natural-language edit instructions (Qwen-Image-2.1 supports dual-image fusion)": (
        "Sube las imágenes fuente y escribe instrucciones en lenguaje natural (Qwen-Image-2.1 admite fusión doble)"
    ),
    "Primary Reference 1 (Required)": "Referencia principal 1 (obligatoria)",
    "Drop or click to upload primary image": "Arrastra o pulsa para subir imagen principal",
    "Fusion Reference 2 (Optional)": "Referencia de fusión 2 (opcional)",
    "Drop or click to upload second fusion image": "Arrastra o pulsa para subir segunda imagen",
    "Image & Typography Generation Prompt": "Prompt de generación de imagen y tipografía",
    "Supports complex scene composition, commercial photography & accurate Chinese/English poster typography": (
        "Admite composición compleja, fotografía comercial y tipografía precisa en carteles"
    ),
    "Positive Prompt": "Prompt positivo",
    "Describe subject, lighting, camera lens, or quoted poster text to render...": (
        "Describe sujeto, iluminación, lente o texto entre comillas para el cartel..."
    ),
    "Negative Prompt (Optional — exclude artifacts or unwanted elements)": (
        "Prompt negativo (opcional — excluye artefactos o elementos no deseados)"
    ),
    "e.g. blurry, low quality, watermark, deformed hands...": (
        "Ej.: blurry, low quality, watermark, deformed hands..."
    ),
    # Media gallery & preview widget
    "Local Media Library": "Biblioteca local",
    "Auto-saved to Videos/EasyColab": "Guardado automático en Videos/EasyColab",
    "No local outputs yet": "Aún no hay archivos locales",
    "ComfyUI Cloud Outputs": "Salidas de ComfyUI en la nube",
    "1-click pull to local library & preview": "Descarga en 1 clic a tu PC y vista previa",
    "Output Preview Stage": "Vista previa de salida",
    "Generated audio-videos & HD images are automatically saved and played here\nSupports real-time 24 FPS video + 32 kHz stereo audio preview": (
        "Los videos con audio e imágenes HD generados se guardan y reproducen aquí\nSoporta vista previa en tiempo real de video a 24 FPS y audio estéreo de 32 kHz"
    ),
    "QtMultimedia is unavailable here. Click 'Replay / Open' below to play in default media player.": (
        "QtMultimedia no está disponible aquí. Pulsa 'Reproducir / Abrir' para reproducir con tu app predeterminada."
    ),
    "Drag & drop or click to select image": "Arrastra y suelta o pulsa para elegir imagen",
    "Image Files (*.png *.jpg *.jpeg *.webp *.bmp)": "Imágenes (*.png *.jpg *.jpeg *.webp *.bmp)",
    "Play": "Play",
    "Pause": "Pausa",
    "Mute": "Mute",
    "Muted": "Mudo",
    "No local media selected": "Sin archivo local seleccionado",
    "Replay / Open": "Reproducir / Abrir",
    "Replay": "Repetir",
    "Open in Viewer": "Abrir en el visor",
    "Show in Finder": "Ver en Finder",
    "Show in Explorer": "Ver en el Explorador",
    "Show in File Manager": "Ver en el gestor de archivos",
    # Custom HuggingFace Repo Dialog
    "Add Custom HuggingFace Repository": "Añadir repositorio de HuggingFace",
    "Pick from live HuggingFace trending models below or enter any Repo ID. For gated/private repos, enter your HF Token and accept the license on HuggingFace.": (
        "Elige un modelo en tendencia de HuggingFace o escribe un Repo ID. Para repos restringidos o privados, introduce tu HF Token y acepta la licencia."
    ),
    "Live HuggingFace Trending & Search (with Params & Colab Fit)": (
        "Tendencias y búsqueda en HuggingFace (parámetros y ajuste en Colab)"
    ),
    "Trending All": "Tendencias",
    "GGUF": "GGUF",
    "LLM / VLM": "LLM / VLM",
    "Image / Video": "Imagen / video",
    "Search HuggingFace models (e.g. Qwen3 GGUF / DeepSeek 9B), press Enter...": (
        "Busca modelos de HuggingFace (ej. Qwen3 GGUF / DeepSeek 9B) y pulsa Enter..."
    ),
    "Search HF": "Buscar HF",
    "1. HuggingFace Repo ID or URL": "1. Repo ID o URL de HuggingFace",
    "Inspect Model Details & Shards": "Ver detalles y fragmentos",
    "Click a trending card above or enter any Owner/Repo": (
        "Pulsa una tarjeta superior o escribe cualquier usuario/repo"
    ),
    "2. Filename / Wildcard Filter (Include Pattern, Optional)": (
        "2. Filtro de archivo o comodín (Include Pattern, opcional)"
    ),
    "Blank = auto-select; or *Q4_K_M*.gguf, *IQ2_XS*.gguf, *.safetensors": (
        "Vacío = autoselección; o *Q4_K_M*.gguf, *IQ2_XS*.gguf, *.safetensors"
    ),
    "3. Display Name (Optional)": "3. Nombre visible (opcional)",
    "Blank = repo short name": "Vacío = nombre corto del repo",
    "4. Task Modality": "4. Modalidad de tarea",
    "Auto-detect": "Autodetectar",
    "Chat / Vision / API": "Chat / visión / API",
    "Image Generation": "Generación de imagen",
    "Video + Audio": "Video + audio",
    "5. HuggingFace Token (Required for Gated/Private Repos)": (
        "5. HuggingFace Token (obligatorio en repos privados o restringidos)"
    ),
    "Get HF Token": "Obtener HF Token",
    "Open Repo & Accept License": "Abrir repo y aceptar licencia",
    "Inspecting HuggingFace model metadata, parameters & shards...": (
        "Consultando metadatos, parámetros y fragmentos en HuggingFace Hub..."
    ),
    "Open on HuggingFace": "Abrir en HuggingFace",
    "Close": "Cerrar",
    "Failed to load model details. Check Repo ID or HF Token.": (
        "No se pudieron cargar los detalles. Revisa el Repo ID o el HF Token."
    ),
    "N/A": "N/D",
    "Params": "Parámetros",
    "Arch/Context": "Arq. / contexto",
    "Repo Size": "Tamaño del repo",
    "No top-level .gguf/.safetensors shards listed.": (
        "No hay fragmentos .gguf/.safetensors en el nivel superior."
    ),
    "Select File": "Elegir archivo",
    "No README excerpt available.": "Sin resumen de README disponible.",
    "No models found; try another keyword, click Refresh, or enter Repo ID below": (
        "Sin resultados; prueba otra palabra, pulsa Actualizar o escribe el Repo ID abajo"
    ),
    "Details": "Info",
    "View model parameters, shards & README details": (
        "Ver parámetros, fragmentos y resumen README del modelo"
    ),
    "Fetching models, parameter counts & Colab VRAM fit from HuggingFace Hub...": (
        "Obteniendo modelos, parámetros y ajuste de VRAM desde HuggingFace Hub..."
    ),
    "Add to Model Center": "Añadir al centro de modelos",
    "Add & Download Weights Now": "Añadir y descargar pesos",
    "Remove Custom Model": "Eliminar modelo personalizado",
    # Onboarding Dialog
    "EasyColab Quick Start Guide": "Guía rápida de EasyColab",
    "EasyColab Guide": "Guía de EasyColab",
    "3-minute beginner walkthrough": "Inicio guiado en 3 minutos",
    "Connect 96GB Cloud GPU": "Conectar GPU de 96GB",
    "Wake a G4 runtime headless in 1 click, or run the notebook in browser": (
        "Activa una instancia G4 en 1 clic sin navegador o ejecuta el notebook"
    ),
    "Tip: After binding your Google account once, just click 'Wake & Deploy' next time.": (
        "Consejo: tras vincular tu cuenta de Google una vez, la próxima pulsa 'Activar GPU'."
    ),
    "Download & Load Models": "Descargar y cargar",
    "Google Drive weight persistence + G4 176GB RAM hot-cache & multi-model co-residency": (
        "Pesos persistentes en Google Drive + caché RAM de 176GB en G4 y multimodelo"
    ),
    "Tip: Co-reside Qwen3.8 LLM gateway alongside image/video models in VRAM with zero switching.": (
        "Consejo: mantén la pasarela Qwen3.8 en VRAM junto con modelos de imagen/video."
    ),
    "Explore 4 Studio Modes": "Los 4 modos",
    "Audio-video generation, ComfyUI guided workflows, 100 tok/s LLM gateway & 2K image editing": (
        "Audio-video, flujos guiados en ComfyUI, pasarela LLM a 100 tok/s y edición 2K"
    ),
    "Tip: Click any card button above to jump directly to that studio workspace.": (
        "Consejo: pulsa cualquier botón superior para ir directo a ese estudio."
    ),
    "Media Saving & CU Tips": "Guardar y ahorrar CU",
    "Outputs auto-download to local Videos folder + 30-min idle auto-shutdown": (
        "Descarga automática a tu carpeta Videos + apagado tras 30 min inactivo"
    ),
    "Tip: Click 'Release All Runtimes' at bottom-left when finished so CU burn drops to zero immediately.": (
        "Consejo: pulsa 'Liberar instancias' abajo a la izquierda al acabar para cortar el gasto CU."
    ),
    "Environment Status": "Estado del entorno",
    "Google Account: Not bound": "Cuenta de Google: sin vincular",
    "Cloud GPU: Not connected": "GPU en la nube: sin conectar",
    "Previous": "Anterior",
    "Next": "Siguiente",
    "Start Creating": "Empezar a crear",
    "1. Bind Google Account (One-time setup)": "1. Vincula tu cuenta de Google (solo la primera vez)",
    "Click 'Bind' in the left sidebar to complete official OAuth login. Credentials stay locally in ~/.config/colab-cli/token.json and sync live CU balance.": (
        "Pulsa 'Vincular' en la barra izquierda para iniciar sesión con OAuth oficial. Tus credenciales se guardan en ~/.config/colab-cli/token.json y sincronizan tu saldo CU."
    ),
    "Bind Google Account Now": "Vincular cuenta de Google",
    "Google account connected": "Cuenta de Google conectada",
    "2. Select G4 & Click 'Wake & Deploy' (Headless)": "2. Elige G4 y pulsa 'Activar GPU' (sin navegador)",
    "Automatically allocates an NVIDIA RTX PRO 6000 Blackwell (96GB VRAM + 176GB RAM), deploys the multi-model server, and connects via encrypted tunnel without opening a browser.": (
        "Asigna automáticamente una NVIDIA RTX PRO 6000 Blackwell (96GB VRAM + 176GB RAM), despliega el servidor multimodelo y conecta por túnel cifrado sin abrir navegador."
    ),
    "Wake G4 & Deploy Now": "Activar G4 y desplegar",
    "Alternative: Run Notebook Manually in Google Colab Browser": (
        "Alternativa: ejecutar el notebook manualmente en Google Colab"
    ),
    "If using Colab Free tier or preferring browser notebooks, upload EasyColab_Server.ipynb, run it, and paste the https://xxxx.gradio.live URL into the left sidebar.": (
        "Si usas el plan gratuito de Colab o prefieres el navegador, sube EasyColab_Server.ipynb, ejecútalo y pega la URL https://xxxx.gradio.live en la barra izquierda."
    ),
    "Export / Reveal .ipynb Notebook": "Exportar / Mostrar .ipynb",
    "Open Google Colab Web": "Abrir Google Colab en la web",
    "1. Click 'Download Weights': Persist Once in Google Drive": (
        "1. Pulsa 'Descargar': guarda una vez en Google Drive"
    ),
    "Built-in 8-thread concurrent downloader. With Google Drive authorized, model weights & ComfyUI nodes persist across sessions for instant reuse.": (
        "Descargador integrado de 8 hilos. Con Google Drive autorizado, pesos y nodos ComfyUI se conservan entre sesiones para reutilizarlos al instante."
    ),
    "2. Click 'Load to VRAM': 96GB VRAM + 176GB RAM Hot Cache": (
        "2. Pulsa 'Cargar en VRAM': 96GB VRAM + caché rápida en 176GB RAM"
    ),
    "G4 runtimes support multi-model VRAM co-residency (e.g. Qwen3.8 API gateway + image/video models), with 176GB DDR5 RAM hot-caching for MiniMax-H3.": (
        "Las instancias G4 permiten varios modelos residentes a la vez en VRAM (ej. pasarela Qwen3.8 + imagen/video), con caché en 176GB DDR5 para MiniMax-H3."
    ),
    "3. Live Telemetry Splines & Real-Time Run Logs": "3. Gráficos de telemetría y registros en tiempo real",
    "Left sidebar plots smooth GPU VRAM / System RAM / Disk curves (combined or split view with hover tooltips) while the right terminal streams live cloud logs.": (
        "La barra izquierda grafica VRAM, RAM y disco en tiempo real mientras el panel derecho muestra los registros en vivo de la nube."
    ),
    "MiniMax-H3 · 4–15s Cinematic Native Audio-Video": (
        "MiniMax-H3 · Audio-video cinematográfico nativo de 4–15s"
    ),
    "Generates 24 FPS HD video synced with 32 kHz stereo ambient SFX, dialogue & music, supporting Text-to-Video+Audio and First/Last-Frame transitions.": (
        "Genera video HD a 24 FPS con sonido ambiente estéreo a 32 kHz, diálogos y música, admitiendo texto a video + audio y transición por fotogramas clave."
    ),
    "Switch to MiniMax-H3 Video Studio": "Ir al estudio de video MiniMax-H3",
    "ComfyUI Node Studio · 4 Guided Ready-to-Run Workflow Packs": (
        "Estudio de nodos ComfyUI · 4 paquetes listos para usar"
    ),
    "Built-in Wan2.2, MiniMax-H3 Turbo, LTX-2.3 & HunyuanVideo 1.5 workflow packs — install weights in 1 click and create in fullscreen browser canvas.": (
        "Paquetes integrados Wan2.2, MiniMax-H3 Turbo, LTX-2.3 y HunyuanVideo 1.5: instala pesos en 1 clic y crea en el lienzo del navegador."
    ),
    "Switch to ComfyUI Node Studio": "Ir al estudio de ComfyUI",
    "Qwen3.8-27B (GGUF 100 tok/s) · Vision Chat & Claude/OpenAI Gateway": (
        "Qwen3.8-27B (GGUF 100 tok/s) · Chat visual y pasarela Claude/OpenAI"
    ),
    "Up to 256K context, deep chain-of-thought & vision prompt analysis, plus dual OpenAI (/v1) & Anthropic (/v1/messages) public API endpoints.": (
        "Hasta 256K de contexto, razonamiento profundo, análisis visual de prompts y endpoints públicos OpenAI (/v1) y Anthropic (/v1/messages)."
    ),
    "Switch to Qwen3.8-GGUF Chat & Gateway": "Ir al chat y API de Qwen3.8-GGUF",
    "Qwen-Image-2.1 / Z-Image-Turbo · 2K Posters & Instruction Editing": (
        "Qwen-Image-2.1 / Z-Image-Turbo · Carteles 2K y edición por instrucciones"
    ),
    "Accurate bilingual poster typography, dual-image natural language fusion editing, and 8-step turbo photorealistic generation.": (
        "Tipografía precisa en carteles, edición por instrucciones con fusión de dos imágenes y generación fotorrealista turbo en 8 pasos."
    ),
    "Switch to Qwen-Image-2.1 Image Studio": "Ir al estudio de imagen Qwen-Image-2.1",
    "1. Auto-Download to Local PC + Cloud Backup": "1. Descarga automática a tu PC + copia en la nube",
    "2. 30-Min Idle Auto-Sleep + 'Release All Runtimes' to Save CU": (
        "2. Reposo en 30 min + 'Liberar instancias' para ahorrar CU"
    ),
    "Built-in idle watchdog (auto-terminates runtime after 30 min idle by default). Click the red 'Release All Runtimes' button when done to stop CU billing immediately.": (
        "Vigilancia por inactividad integrada (cierra la instancia tras 30 min sin uso por defecto). Pulsa el botón rojo 'Liberar instancias' al terminar para detener el cobro al instante."
    ),
    "3. Privacy Masking Toggle & Free Encrypted Cloudflare Tunnel": (
        "3. Máscara de privacidad y túnel cifrado Cloudflare gratuito"
    ),
    "Before screen-recording or sharing screenshots, click 'Mask' next to the server URL to hide *.gradio.live / *.trycloudflare.com domains and your email.": (
        "Antes de grabar pantalla o compartir capturas, pulsa 'Ocultar' junto a la URL del servidor para ocultar dominios *.gradio.live / *.trycloudflare.com y tu correo."
    ),
    # ViewModel & ViewModelServices status / errors
    "Ready: Bind your Google account and wake a G4 runtime, or paste an existing tunnel URL.": (
        "Listo: vincula tu cuenta de Google y activa una instancia G4, o pega la URL de un túnel."
    ),
    "Please enter a https://xxxx.gradio.live server URL or click 'Wake & Deploy'.": (
        "Introduce una URL https://xxxx.gradio.live o pulsa 'Activar GPU'."
    ),
    "Cloud tunnel expired or runtime terminated. Please wake & deploy again.": (
        "El túnel expiró o la instancia se cerró. Vuelve a pulsar 'Activar GPU'."
    ),
    "Please connect or wake a Colab cloud runtime first.": (
        "Conecta o activa primero una instancia de Colab."
    ),
    "Please click 'Download Weights' to fetch model shards first.": (
        "Pulsa primero 'Descargar' para bajar los fragmentos del modelo."
    ),
    "Unloading model from GPU VRAM & freeing cache...": (
        "Descargando modelo de la VRAM y liberando caché..."
    ),
    "Cleared local VRAM residency record.": "Registro local de residencia en VRAM borrado.",
    "Please enter a prompt or message first.": "Escribe primero un prompt o mensaje.",
    "First/Last-Frame Video mode requires at least a start or end reference frame.": (
        "El modo fotograma inicial/final requiere al menos una imagen de inicio o fin."
    ),
    "Instruction Edit / Img2Img mode requires at least one reference image.": (
        "El modo de edición / Img2Img requiere al menos una imagen de referencia."
    ),
    "Not connected to Colab server. Please wake or connect a runtime first.": (
        "Sin conexión al servidor de Colab. Activa o conecta una instancia primero."
    ),
    "Failed to submit job": "Error al enviar la tarea",
    "Cloud inference process interrupted (possible OOM or runtime release). Please wake the runtime again.": (
        "La inferencia en la nube se interrumpió (posible falta de VRAM o cierre de instancia). Actívala de nuevo."
    ),
    "Polling cloud job failed repeatedly. Please check your network connection.": (
        "Falló repetidamente la consulta de estado en la nube. Revisa tu conexión."
    ),
    "Network connection timed out repeatedly. Stopped polling.": (
        "La conexión agotó el tiempo repetidamente. Consulta detenida."
    ),
    "Cloud inference failed": "Falló la inferencia en la nube",
    "Stop signal sent. Interrupting active cloud GPU sampling job...": (
        "Señal de parada enviada. Interrumpiendo la tarea activa en la GPU..."
    ),
    "Console cleared. Listening for live cloud logs...": (
        "Registros limpiados. Esperando registros en vivo de la nube..."
    ),
    "Built-in EasyColab_Server.ipynb file not found.": (
        "No se encontró el archivo integrado EasyColab_Server.ipynb."
    ),
    "First-run setup: initializing local Colab bridge components (~15-30s)...": (
        "Primer inicio: preparando componentes locales de conexión con Colab (~15-30s)..."
    ),
    "Empty response": "Respuesta vacía",
    "Cloud runtime released; local state reset.": (
        "Instancia en la nube liberada; estado local reiniciado."
    ),
    "Generating Google OAuth authorization URL...": (
        "Generando enlace de autorización Google OAuth..."
    ),
    "Select the Google account in your browser and paste the authorization code below.": (
        "Elige la cuenta de Google en tu navegador y pega abajo el código de autorización."
    ),
    "Opened Google sign-in in browser. Authorize and paste the code below.": (
        "Se abrió el acceso de Google en tu navegador. Autoriza y pega el código abajo."
    ),
    "Failed to generate OAuth URL": "No se pudo generar la URL de OAuth",
    "Please paste the Google authorization code from your browser first.": (
        "Pega primero el código de autorización de Google desde tu navegador."
    ),
    "Verifying authorization code & syncing Google Colab account...": (
        "Verificando código de autorización y sincronizando cuenta de Google Colab..."
    ),
    "Switched Google account. Click 'Wake & Deploy' to launch a new runtime.": (
        "Cuenta de Google cambiada. Pulsa 'Activar GPU' para iniciar una nueva instancia."
    ),
    "Invalid or expired authorization code": "Código de autorización inválido o caducado",
    "Signed out of Google account.": "Sesión de Google cerrada.",
    "Please click 'Bind' to sign in with your Google account first.": (
        "Pulsa primero 'Vincular' para iniciar sesión con tu cuenta de Google."
    ),
    "Syncing Google Drive & terminating all active Colab GPU runtimes...": (
        "Sincronizando Google Drive y cerrando todas las instancias GPU activas..."
    ),
    "All cloud runtimes released.": "Todas las instancias en la nube liberadas.",
    "Please enter a valid HuggingFace Repo ID (format: owner/repo, e.g. unsloth/Qwen3.8-27B-GGUF)": (
        "Introduce un Repo ID de HuggingFace válido (formato: autor/repo, ej. unsloth/Qwen3.8-27B-GGUF)"
    ),
    "Deploying ComfyUI node canvas & Cloudflare HTTPS tunnel on cloud...": (
        "Desplegando lienzo ComfyUI y túnel HTTPS Cloudflare en la nube..."
    ),
    "Syncing workflows to Google Drive and stopping ComfyUI...": (
        "Sincronizando flujos a Google Drive y deteniendo ComfyUI..."
    ),
    "Syncing ComfyUI custom nodes, models & workflows to Google Drive...": (
        "Sincronizando nodos, modelos y flujos de ComfyUI con Google Drive..."
    ),
    "Please enter a direct model URL or Hugging Face Repo ID first.": (
        "Introduce primero una URL directa del modelo o un Repo ID de HuggingFace."
    ),
    "Installing preset workflow pack & generating guided node templates on cloud...": (
        "Instalando paquete de flujos y generando plantillas guiadas en la nube..."
    ),
    "Cloud server version is outdated. Click 'Wake & Deploy' on the left to hot-update the server.": (
        "La versión del servidor en la nube es antigua. Pulsa 'Activar GPU' a la izquierda para actualizarlo."
    ),
    # Models catalog, resolutions, ComfyUI preset packs, shard descriptions & HF sizing
    "Native BF16 · 134 GB": "BF16 nativo · 134 GB",
    "Full-modality native BF16 generation of HD video with synced 32kHz stereo SFX, dialogue & music": (
        "Generación BF16 nativa multimodal de video HD con efectos estéreo 32kHz, diálogos y música"
    ),
    "Text to Video+Audio": "Texto a video + audio",
    "Describe visuals and sound to generate video with synced stereo audio": (
        "Describe escena y sonido para generar video con audio estéreo sincronizado"
    ),
    "First/Last Frame to Video": "Fotograma inicial/final a video",
    "Upload start/end reference frames for precise composition & camera transitions": (
        "Sube fotogramas de inicio/fin para controlar con precisión la composición y cámara"
    ),
    "ComfyUI Node Studio": "Estudio de nodos ComfyUI",
    "Node Workflows · Drive Symlink": "Flujos por nodos · enlace a Drive",
    "One-click cloud ComfyUI + Manager fullscreen node canvas with auto Google Drive symlink persistence for nodes, models & workflows": (
        "Lienzo ComfyUI + Manager en la nube en 1 clic con persistencia automática en Google Drive para nodos, modelos y flujos"
    ),
    "Fullscreen Node Canvas": "Lienzo de nodos completo",
    "Deploy & open fullscreen node canvas in browser with G4 keepalive, telemetry & auto-sleep": (
        "Despliega y abre el lienzo en navegador con keepalive G4, telemetría y reposo automático"
    ),
    "Fast Weight DL & Output Pull": "Descarga rápida y sincronización de salidas",
    "8-thread high-speed model download to Drive and 1-click output media sync to local PC": (
        "Descarga de modelos en 8 hilos a Drive y sincronización de salidas a tu PC en 1 clic"
    ),
    "Native BF16 · 51.8 GB": "BF16 nativo · 51.8 GB",
    "Top open-source multimodal LLM in full native BF16 precision with up to 256K context (high-VRAM GPU)": (
        "LLM multimodal abierto líder en BF16 nativo con hasta 256K de contexto (requiere GPU de alta VRAM)"
    ),
    "Deep Reasoning Chat": "Chat de razonamiento profundo",
    "Long chain-of-thought reasoning, architecture design, logic & storyboard writing": (
        "Razonamiento largo en cadena, diseño de arquitectura, lógica y guiones visuales"
    ),
    "Vision Understanding": "Comprensión visual",
    "Drop images for scene analysis, OCR, or reverse-engineering image/video prompts": (
        "Suelta imágenes para analizar escenas, OCR o deducir prompts de imagen y video"
    ),
    "API Protocol Gateway": "Pasarela de protocolo API",
    "Dual-protocol public gateway supporting OpenAI (/v1) & Anthropic (/v1/messages)": (
        "Pasarela pública dual compatible con OpenAI (/v1) y Anthropic (/v1/messages)"
    ),
    "UD-Q4_K_M + MTP · 18.7 GB": "UD-Q4_K_M + MTP · 18.7 GB",
    "Unsloth dynamic 4-bit quantization + native MTP speculative decoding (~100 tok/s), up to 256K context & vision": (
        "Cuantización dinámica 4-bit Unsloth + decodificación especulativa MTP (~100 tok/s), hasta 256K y visión"
    ),
    "Ultra-fast UD-Q4_K_M + MTP speculative decoding for CoT reasoning, coding & long-context analysis": (
        "Decodificación ultrarrápida UD-Q4_K_M + MTP para razonamiento CoT, código y contexto largo"
    ),
    "Built-in mmproj-F16 vision projector for image analysis, OCR & prompt reverse-engineering": (
        "Proyector visual mmproj-F16 integrado para análisis de imagen, OCR y extracción de prompts"
    ),
    "T2I & Image Edit · 30.9 GB": "T2I y edición · 30.9 GB",
    "Flagship Qwen text-to-image generation and natural-language multi-image editing model": (
        "Modelo insignia de Qwen para texto a imagen y edición multi-imagen en lenguaje natural"
    ),
    "HD Text to Image": "Texto a imagen HD",
    "HD Text-to-Image": "Texto a imagen HD",
    "Complex composition, accurate bilingual typography & studio-grade photography/illustration": (
        "Composición compleja, tipografía precisa e ilustración o fotografía de estudio"
    ),
    "Multi-Image Instruction Edit": "Edición por instrucción multi-imagen",
    "Upload 1-2 reference images to edit regions, swap backgrounds, or fuse subjects via natural language": (
        "Sube 1 o 2 imágenes para editar zonas, cambiar fondos o fusionar sujetos con lenguaje natural"
    ),
    "8-Step Turbo T2I · 30.6 GB": "T2I turbo 8 pasos · 30.6 GB",
    "Popular 8-step distilled photorealistic & bilingual poster image generation model": (
        "Modelo popular destilado de 8 pasos para fotografía realista y carteles con texto"
    ),
    "8-Step Turbo T2I": "Texto a imagen turbo en 8 pasos",
    "Commercial-grade portraits & bilingual poster typography in just 8 sampling steps": (
        "Retratos comerciales y tipografía en carteles en solo 8 pasos de muestreo"
    ),
    "Image-to-Image Restyle": "Redibujo imagen a imagen",
    "Upload a reference image and adjust denoising strength to restyle while preserving composition": (
        "Sube una imagen de referencia y ajusta la intensidad para reestilizar conservando la composición"
    ),
    "Custom HuggingFace image generation pipeline": "Pipeline personalizado de imagen de HuggingFace",
    "Upload a reference image and adjust denoising strength to restyle": (
        "Sube una imagen de referencia y ajusta la intensidad para reestilizar"
    ),
    "Custom HuggingFace model chat, CoT reasoning & coding": (
        "Chat, razonamiento CoT y código con modelo personalizado de HuggingFace"
    ),
    "Drop images for scene analysis, OCR, or prompt reverse-engineering": (
        "Suelta imágenes para análisis de escena, OCR o extracción de prompts"
    ),
    "Public dual-protocol gateway compatible with OpenAI (/v1) & Anthropic (/v1/messages)": (
        "Pasarela pública dual compatible con OpenAI (/v1) y Anthropic (/v1/messages)"
    ),
    # Video & Image resolutions
    "832 × 480 (16:9 Landscape · Recommended)": "832 × 480 (16:9 horizontal · recomendado)",
    "480 × 832 (9:16 Vertical Short)": "480 × 832 (9:16 vertical corto)",
    "1280 × 720 (16:9 720P HD)": "1280 × 720 (16:9 720P HD)",
    "720 × 1280 (9:16 720P Vertical)": "720 × 1280 (9:16 720P vertical)",
    "640 × 640 (1:1 Square)": "640 × 640 (1:1 cuadrado)",
    "1024 × 1024 (1:1 Square HD · Recommended)": "1024 × 1024 (1:1 cuadrado HD · recomendado)",
    "1344 × 768 (16:9 Cinematic Wide)": "1344 × 768 (16:9 panorámico de cine)",
    "768 × 1344 (9:16 Vertical Poster)": "768 × 1344 (9:16 cartel vertical)",
    "1536 × 1024 (3:2 DSLR Photo)": "1536 × 1024 (3:2 foto DSLR)",
    # Preset template titles & LLM/VLM preset prompts
    "[Anime] Makoto Shinkai · Cherry Blossom Railway Crossing": (
        "[Anime] Estilo Makoto Shinkai · Paso a nivel entre cerezos"
    ),
    "[Anime] ufotable Sakuga · Blue Lightning Sword Duel": (
        "[Anime] Estilo ufotable · Duelo de espadas con relámpago azul"
    ),
    "[Realistic] Icelandic Waterfall FPV Drone Dive": (
        "[Realista] Dron FPV en picado sobre cascada de Islandia"
    ),
    "[Image] Cyberpunk Shanghai Neon Poster (Typography)": (
        "[Imagen] Cartel neón ciberpunk de Shanghái (tipografía)"
    ),
    "[Image] Medium Format Film Afternoon Tokyo Cafe": (
        "[Imagen] Café de Tokio de tarde en película de formato medio"
    ),
    "[Reasoning] Write 3 Makoto Shinkai Anime Storyboard Prompts": (
        "[Razonamiento] Crear 3 prompts de storyboard anime estilo Makoto Shinkai"
    ),
    "[Vision] Analyze Composition & Reverse-Engineer T2I/T2V Prompt": (
        "[Visión] Analizar composición y deducir prompt T2I/T2V"
    ),
    (
        "Please design 3 vivid Makoto Shinkai-style anime short film storyboards. For each shot include: "
        "1) Visual & Camera prompt; 2) Soundscape description; 3) Background Music description."
    ): (
        "Diseña 3 storyboards detallados para un corto de animación al estilo Makoto Shinkai. "
        "Para cada plano incluye: 1) prompt Visual & Camera (en inglés); 2) descripción de Soundscape; "
        "3) descripción de Background Music."
    ),
    (
        "Carefully examine the subject, lighting, color grading, camera framing, and artistic style of this image. "
        "Provide a brief breakdown first, then reverse-engineer a detailed English T2I / T2V generation prompt."
    ): (
        "Analiza con detalle el sujeto, la iluminación, el color, el encuadre y el estilo artístico de esta imagen. "
        "Ofrece primero un breve desglose en español y después deduce un prompt detallado en inglés para T2I / T2V."
    ),
    # ComfyUI preset packs
    "Wan2.2 14B · Image-to-Video + First/Last Frame Dual Workflows": (
        "Wan2.2 14B · Imagen a video + flujos duales inicio/fin"
    ),
    "Beginner Pick · 4-Step Fast": "Recomendado · rápido en 4 pasos",
    "Includes Single-Image I2V & First/Last-Frame Smooth Transition workflows (~25s on G4, pure built-in nodes, zero missing-node errors)": (
        "Incluye flujos I2V de imagen única y transición suave inicio/fin (~25s en G4, solo nodos integrados, cero errores)"
    ),
    "MiniMax-H3 Turbo · Audio-Video I2V + First/Last Frame Workflows": (
        "MiniMax-H3 Turbo · I2V audio-video + flujos inicio/fin"
    ),
    "Synced Stereo Audio · 8-Step": "Audio estéreo sincronizado · 8 pasos",
    "Includes Single-Image & First/Last-Frame Audio-Video workflows generating HD motion with synced ambient SFX, music & dialogue": (
        "Incluye flujos audio-video de imagen única y doble fotograma con video HD y SFX, música y diálogo sincronizados"
    ),
    "LTX-2.3 (22B) · Cinematic First/Last-Frame Camera Control + Audio": (
        "LTX-2.3 (22B) · Control de cámara cinematográfico inicio/fin + audio"
    ),
    "Cinematic Camera · Only 2 Weights": "Cámara de cine · solo 2 pesos",
    "Optimized for dramatic camera motion between keyframes (e.g., aerial crane dive to low-angle close-up with synced soundtrack)": (
        "Optimizado para movimientos amplios de cámara entre fotogramas clave con banda sonora sincronizada"
    ),
    "HunyuanVideo 1.5 · Single-Image Direct 1080P Super-Res Workflow": (
        "HunyuanVideo 1.5 · Flujo directo 1080P super-resolución desde 1 imagen"
    ),
    "720P + 1080P Dual Output": "Doble salida 720P + 1080P",
    "Latent super-resolution pipeline enabled by default — upload 1 image to render both 720P base and crisp 1920×1080 HD video": (
        "Pipeline de super-resolución latente activo por defecto: sube 1 imagen para generar base 720P y HD 1920×1080"
    ),
    # Shard descriptions & HF sizing
    "3D Video VAE BF16 (9.7 GB)": "VAE de video 3D BF16 (9.7 GB)",
    "32kHz Stereo Audio VAE BF16 (0.6 GB)": "VAE de audio estéreo 32kHz BF16 (0.6 GB)",
    "Unsloth UD-Q4_K_M Main Weights (16.5 GB)": "Pesos principales Unsloth UD-Q4_K_M (16.5 GB)",
    "Multimodal Vision Projector (0.93 GB)": "Proyector visual multimodal (0.93 GB)",
    "Unsloth MTP Speculative Head (1.31 GB)": "Cabeza especulativa Unsloth MTP (1.31 GB)",
    "Image VAE": "VAE de imagen",
    "VRAM TBD": "VRAM por determ.",
    "Size TBD": "Tamaño por determ.",
    "T4 15G Ready": "Apto T4 15G",
    "L4 24G Ready": "Apto L4 24G",
    "A100 40G": "A100 40G",
    "A100 80G": "A100 80G",
    ">80G VRAM": ">80G VRAM",
    "Set a management password before deploying": "Configura una clave admin antes de desplegar",
}


def _plural(n_str: str, singular: str, plural: str) -> str:
    return singular if n_str == "1" else plural


# ─── English -> Spanish Regex Rules for f-string tr(..., en) calls ───────────

EN_REGEX_TO_ES: List[Tuple[re.Pattern[str], Any]] = [
    # main_window.py
    (
        re.compile(r"^Applied preset template: (.+)$", re.DOTALL),
        r"Plantilla aplicada: \1",
    ),
    (
        re.compile(r"^(\d+) frames · ~([\d.]+)s$"),
        lambda m: f"{m.group(1)} fotogramas · ~{m.group(2)}s",
    ),
    (
        re.compile(r"^(\d+) steps$"),
        lambda m: f"{m.group(1)} {_plural(m.group(1), 'paso', 'pasos')}",
    ),
    (
        re.compile(
            r"^(.+?) · VRAM ([\d.]+)/(\d+)G · RAM ([\d.]+)/(\d+)G · Disk Free (\d+)/(\d+)G$"
        ),
        r"\1 · VRAM \2/\3G · RAM \4/\5G · Disco libre \6/\7G",
    ),
    (
        re.compile(r"^Co-Resident in VRAM \((\d+)\)$"),
        r"En VRAM (\1)",
    ),
    (
        re.compile(r"^View Weight Shards \((\d+)\)$"),
        r"Ver fragmentos (\1)",
    ),
    (
        re.compile(r"^Release All Runtimes \((\d+) Active\)$"),
        lambda m: f"Liberar instancias ({m.group(1)} {_plural(m.group(1), 'activa', 'activas')})",
    ),
    (
        re.compile(r"^(\d+) Co-Resident$"),
        r"\1 residentes",
    ),
    (
        re.compile(r"^(\d+) Models Co-Resident$"),
        lambda m: f"{m.group(1)} {_plural(m.group(1), 'modelo residente', 'modelos residentes')}",
    ),
    (
        re.compile(r"^(\d+) lines$"),
        lambda m: f"{m.group(1)} {_plural(m.group(1), 'línea', 'líneas')}",
    ),
    (
        re.compile(r"^Inferring on Cloud\.\.\. (\d+)% · Elapsed (.+)$"),
        r"Infiriendo en la nube... \1% · Transcurrido \2",
    ),
    (
        re.compile(r"^RAM Disk Free ([\d.]+)/(\d+)G$"),
        r"RAMDisk libre \1/\2G",
    ),
    (
        re.compile(r"^Drive Free ([\d.]+)G$"),
        r"Drive libre \1G",
    ),
    (
        re.compile(r"^Auto-release in (\d+)m (\d+)s if idle$"),
        r"Auto-liberación en \1m \2s si está inactivo",
    ),
    (
        re.compile(r"^Auto-release after (\d+) min of inactivity once connected$"),
        r"Se liberará tras \1 min de inactividad al conectarse",
    ),
    (
        re.compile(r"^Ready (\d+)/(\d+) \(([\d.]+) GB\)$"),
        r"Listo \1/\2 (\3 GB)",
    ),
    (
        re.compile(r"^(\d+)/(\d+) shards$"),
        r"\1/\2 fragmentos",
    ),
    (
        re.compile(r"^Loaded KV is (\d+)K — click 'Reload VRAM' to apply (\d+)K$"),
        r"KV cargado a \1K — pulsa 'Recargar VRAM' para aplicar \2K",
    ),
    (
        re.compile(r"^Generate (\d+)x Audio-Video Clips \(Ctrl\+Enter\)$"),
        r"Generar \1x clips audio-video (Ctrl+Enter)",
    ),
    (
        re.compile(r"^Generate (\d+)x HD Images \(Ctrl\+Enter\)$"),
        r"Generar \1x imágenes HD (Ctrl+Enter)",
    ),
    (
        re.compile(r"^Thinking Process \((\d+) chars\)$"),
        r"Proceso de pensamiento (\1 caracteres)",
    ),
    (
        re.compile(r"^Storage: (.+)$", re.DOTALL),
        lambda m: f"Almacenamiento: {localize_server_text_es(m.group(1))}",
    ),
    (
        re.compile(r"^Saved Nodes / Weights: (\d+) nodes · (\d+) weights$"),
        lambda m: (
            f"Nodos / pesos guardados: {m.group(1)} {_plural(m.group(1), 'nodo', 'nodos')} · "
            f"{m.group(2)} {_plural(m.group(2), 'peso', 'pesos')}"
        ),
    ),
    (
        re.compile(r"^Canvas Queue: (\d+) running · (\d+) queued$"),
        r"Cola del lienzo: \1 en curso · \2 en espera",
    ),
    # onboarding_dialog.py
    (
        re.compile(
            r"^All generated MP4 audio-videos and PNG HD images automatically download to (.+?) on your computer, safe even after cloud shutdown\.$",
            re.DOTALL,
        ),
        r"Todos los videos MP4 con audio e imágenes PNG HD se descargan automáticamente a \1 en tu equipo, a salvo aunque apagues la nube.",
    ),
    (
        re.compile(r"^Google Account: (.+)$", re.DOTALL),
        lambda m: f"Cuenta de Google: {translate_en_to_es(m.group(1))}",
    ),
    (
        re.compile(r"^Cloud GPU: (.+)$", re.DOTALL),
        lambda m: f"GPU en la nube: {localize_server_text_es(m.group(1))}",
    ),
    # viewmodel.py
    (
        re.compile(r"^Located notebook file: (.+)$", re.DOTALL),
        r"Notebook localizado: \1",
    ),
    (
        re.compile(r"^Starting 8-thread cloud download for (.+?) weights\.\.\.$"),
        r"Iniciando descarga en la nube (8 hilos) de pesos de \1...",
    ),
    (
        re.compile(r"^Loading (.+?) into cloud GPU VRAM\.\.\.$"),
        r"Cargando \1 en la VRAM de la GPU en la nube...",
    ),
    (
        re.compile(r"^Submitting (.+?) inference job to cloud\.\.\.$"),
        r"Enviando tarea de inferencia de \1 a la nube...",
    ),
    (
        re.compile(r"^EasyColab (.+?) Studio is ready\.$"),
        r"Estudio EasyColab para \1 listo.",
    ),
    (
        re.compile(r"^Local media auto-save folder: (.+)$", re.DOTALL),
        r"Carpeta de guardado automático local: \1",
    ),
    (
        re.compile(r"^Please click 'Load to VRAM' in the Model Center to load (.+?) first\.$"),
        r"Pulsa primero 'Cargar en VRAM' en el centro de modelos para cargar \1.",
    ),
    (
        re.compile(r"^Weight download request error: (.+)$", re.DOTALL),
        r"Error al solicitar descarga de pesos: \1",
    ),
    (
        re.compile(r"^Load to VRAM request error: (.+)$", re.DOTALL),
        r"Error al solicitar carga en VRAM: \1",
    ),
    (
        re.compile(r"^Failed to submit inference job: (.+)$", re.DOTALL),
        r"Error al enviar la tarea de inferencia: \1",
    ),
    (
        re.compile(r"^Connected to cloud (.+)!$"),
        r"¡Conectado a \1 en la nube!",
    ),
    (
        re.compile(r"^Batch generation complete \((\d+) items\) and auto-saved locally!$"),
        lambda m: (
            f"¡Lote completado ({m.group(1)} {_plural(m.group(1), 'elemento', 'elementos')}) y guardado en tu equipo!"
        ),
    ),
    (
        re.compile(r"^Cannot reach cloud tunnel: (.+)$", re.DOTALL),
        r"No se puede conectar al túnel en la nube: \1",
    ),
    (
        re.compile(r"^Cloud server error \(HTTP (\d+)\)\.$"),
        r"Error del servidor en la nube (HTTP \1).",
    ),
    # viewmodel_services.py
    (
        re.compile(r"^Waking Google Colab (.+?) runtime & deploying multi-model server\.\.\.$"),
        r"Activando instancia Google Colab \1 y desplegando servidor multimodelo...",
    ),
    (
        re.compile(
            r"^Added custom model '(.+?)' \((.+?)\)\. Connect to Colab to download weights to Google Drive\.$",
            re.DOTALL,
        ),
        r"Modelo personalizado '\1' (\2) añadido. Conéctate a Colab para bajar los pesos a Google Drive.",
    ),
    (
        re.compile(r"^8-thread downloading weights to ComfyUI/models/(.+?)\.\.\.$"),
        r"Descargando pesos en 8 hilos a ComfyUI/models/\1...",
    ),
    (
        re.compile(r"^Pulling output media (.+?) from cloud ComfyUI\.\.\.$"),
        r"Descargando archivo \1 desde ComfyUI en la nube...",
    ),
    (
        re.compile(r"^Server script app\.py not found \((.+?)\)$", re.DOTALL),
        r"No se encontró el script del servidor app.py (\1)",
    ),
    (
        re.compile(r"^─── Starting Headless Wake for Colab (.+?) Runtime ───$"),
        r"─── Iniciando activación sin navegador de Colab \1 ───",
    ),
    (
        re.compile(r"^Resolving HuggingFace repo (.+?) & syncing to cloud Model Center\.\.\.$"),
        r"Resolviendo repo HuggingFace \1 y sincronizando con el centro de modelos...",
    ),
    (
        re.compile(r"^Failed to get OAuth URL: (.+)$", re.DOTALL),
        r"Error al obtener URL de OAuth: \1",
    ),
    (
        re.compile(
            r"^Google account bound \((.+?)\)! Ready to wake (.+?) runtime in 1 click\.$",
            re.DOTALL,
        ),
        r"¡Cuenta de Google vinculada (\1)! Listo para activar \2 en 1 clic.",
    ),
    (
        re.compile(r"^Account binding failed: (.+)$", re.DOTALL),
        r"Error al vincular cuenta: \1",
    ),
    (
        re.compile(r"^Error starting ComfyUI: (.+)$", re.DOTALL),
        r"Error al iniciar ComfyUI: \1",
    ),
    (
        re.compile(r"^Saved locally: (.+)$", re.DOTALL),
        r"Guardado en local: \1",
    ),
    (
        re.compile(r"^Cloud (.+?) runtime is online! Syncing model status\.\.\.$"),
        r"¡Instancia \1 en la nube activa! Sincronizando estado de modelos...",
    ),
    (
        re.compile(r"^Tunnel URL acquired: (.+)$", re.DOTALL),
        r"URL del túnel obtenida: \1",
    ),
    (
        re.compile(r"^Wake failed: (.+)$", re.DOTALL),
        lambda m: f"Error al activar instancia: {localize_server_text_es(m.group(1))}",
    ),
    (
        re.compile(r"^Wake process error: (.+)$", re.DOTALL),
        r"Error en el proceso de activación: \1",
    ),
    (
        re.compile(r"^Error stopping ComfyUI: (.+)$", re.DOTALL),
        r"Error al detener ComfyUI: \1",
    ),
    (
        re.compile(r"^Error freeing VRAM: (.+)$", re.DOTALL),
        r"Error al liberar VRAM: \1",
    ),
    (
        re.compile(r"^Error syncing to Google Drive: (.+)$", re.DOTALL),
        r"Error al sincronizar con Google Drive: \1",
    ),
    (
        re.compile(r"^Error downloading ComfyUI weight: (.+)$", re.DOTALL),
        r"Error al descargar peso de ComfyUI: \1",
    ),
    (
        re.compile(r"^Error installing preset workflow pack: (.+)$", re.DOTALL),
        r"Error al instalar paquete de flujos: \1",
    ),
    (
        re.compile(r"^Failed to pull output media \(HTTP (\d+)\)$"),
        r"Error al bajar archivo de salida (HTTP \1)",
    ),
    (
        re.compile(r"^Error pulling output media: (.+)$", re.DOTALL),
        r"Error al bajar archivo de salida: \1",
    ),
    # widgets.py
    (
        re.compile(r"^Select Image — (.+)$", re.DOTALL),
        r"Elegir imagen — \1",
    ),
    (
        re.compile(r"^Elapsed (.+)$"),
        r"Duración \1",
    ),
    # workspace_mixin.py
    (
        re.compile(r"^Weights (\d+)/(\d+) · ~([\d.]+) GB  \|  $"),
        r"Pesos \1/\2 · ~\3 GB  |  ",
    ),
    (
        re.compile(r"^  \|  Tunnel: (.+)$", re.DOTALL),
        r"  |  Túnel: \1",
    ),
    (
        re.compile(r"^(\d+) / (\d+) Packs Ready$"),
        r"\1 / \2 paquetes listos",
    ),
    (
        re.compile(r"^(\d+) files$"),
        lambda m: f"{m.group(1)} {_plural(m.group(1), 'archivo', 'archivos')}",
    ),
    (
        re.compile(r"^(\d+) nodes$"),
        lambda m: f"{m.group(1)} {_plural(m.group(1), 'nodo', 'nodos')}",
    ),
    (
        re.compile(r"^(\d+) templates$"),
        lambda m: f"{m.group(1)} {_plural(m.group(1), 'plantilla', 'plantillas')}",
    ),
    (
        re.compile(r"^Total API Requests: (\d+)$"),
        r"Peticiones API totales: \1",
    ),
    (
        re.compile(r"^Model Details — (.+)$", re.DOTALL),
        r"Detalles del modelo — \1",
    ),
    (
        re.compile(r"^Installing \((\d+)%\)\.\.\.$"),
        r"Instalando (\1%)...",
    ),
    (
        re.compile(r"^Tip: Click 'Load to VRAM' on the left to load (.+?) first$"),
        r"Consejo: pulsa 'Cargar en VRAM' a la izquierda para cargar \1 primero",
    ),
    (
        re.compile(r"^Copied (.+?) to clipboard\.$", re.DOTALL),
        r"\1 copiado al portapapeles.",
    ),
    (
        re.compile(r"^Rendering \((\d+) running / (\d+) queued\)$"),
        r"Renderizando (\1 en curso / \2 en espera)",
    ),
    (
        re.compile(r"^Multi-model co-residency active: external APIs can call (.+?) anytime$"),
        r"Multimodelo en VRAM activo: las APIs externas pueden llamar a \1 en cualquier momento",
    ),
    (
        re.compile(r"^(.+?) API Gateway Ready$"),
        r"Pasarela API \1 lista",
    ),
    # models.py custom model / shard descriptions
    (
        re.compile(r"^Custom ([A-Za-z0-9_+-]+) · ([\d.]+) GB$"),
        r"\1 personalizado · \2 GB",
    ),
    (
        re.compile(r"^Custom HF · ([A-Za-z0-9_+-]+)$"),
        r"HF personalizado · \1",
    ),
    (
        re.compile(r"^Custom HuggingFace repo (.+)$", re.DOTALL),
        r"Repo HuggingFace personalizado \1",
    ),
    (
        re.compile(r"^DiT A/V Backbone BF16 (.+)$"),
        r"Troncal DiT A/V BF16 \1",
    ),
    (
        re.compile(r"^Multimodal Encoder BF16 (.+)$"),
        r"Codificador multimodal BF16 \1",
    ),
    (
        re.compile(r"^Weight Shard (.+)$"),
        r"Fragmento de pesos \1",
    ),
    (
        re.compile(r"^Text Encoder (.+)$"),
        r"Codificador de texto \1",
    ),
    # viewmodel_services.py HF sizing labels
    (
        re.compile(r"^Custom Pipeline \((.+?)\)$"),
        r"Pipeline no integrado (\1)",
    ),
    (
        re.compile(r"^Fit: T4 15G \((.+?)\)$"),
        r"Apto: T4 15G (\1)",
    ),
    (
        re.compile(r"^Fit: L4 24G \((.+?)\)$"),
        r"Apto: L4 24G (\1)",
    ),
    (
        re.compile(r"^Fit: A100 40G \((.+?)\)$"),
        r"Apto: A100 40G (\1)",
    ),
    (
        re.compile(r"^Needs A100 80G \((.+?)\)$"),
        r"Requiere A100 80G (\1)",
    ),
    (
        re.compile(r"^A100 80G \+ Offload \((.+?)\)$"),
        r"A100 80G + Offload (\1)",
    ),
    (
        re.compile(r"^Too Large \((.+?) · Try GGUF\)$"),
        r"Demasiado grande (\1 · prueba GGUF)",
    ),
]


def translate_en_to_es(en: str) -> str:
    if not en:
        return en
    if en in EN_TO_ES:
        return EN_TO_ES[en]
    for pattern, repl in EN_REGEX_TO_ES:
        if pattern.fullmatch(en):
            return pattern.sub(repl, en)  # type: ignore[arg-type]
    return en


# ─── Shard Descriptions (Chinese / English -> Spanish) ────────────────────────

SHARD_DESC_EXACT_ES: Dict[str, str] = {
    "3D 视频 VAE BF16 (9.7 GB)": "VAE de video 3D BF16 (9.7 GB)",
    "32kHz 立体声 VAE BF16 (0.6 GB)": "VAE de audio estéreo 32kHz BF16 (0.6 GB)",
    "Unsloth UD-Q4_K_M 主模型 (16.5 GB)": "Pesos principales Unsloth UD-Q4_K_M (16.5 GB)",
    "多模态视觉投影器 (0.93 GB)": "Proyector visual multimodal (0.93 GB)",
    "Unsloth MTP 多词元投机解码头 (1.31 GB)": "Cabeza especulativa Unsloth MTP (1.31 GB)",
    "图像 VAE": "VAE de imagen",
    "3D Video VAE BF16 (9.7 GB)": "VAE de video 3D BF16 (9.7 GB)",
    "32kHz Stereo Audio VAE BF16 (0.6 GB)": "VAE de audio estéreo 32kHz BF16 (0.6 GB)",
    "Unsloth UD-Q4_K_M Main Weights (16.5 GB)": "Pesos principales Unsloth UD-Q4_K_M (16.5 GB)",
    "Multimodal Vision Projector (0.93 GB)": "Proyector visual multimodal (0.93 GB)",
    "Unsloth MTP Speculative Head (1.31 GB)": "Cabeza especulativa Unsloth MTP (1.31 GB)",
    "Image VAE": "VAE de imagen",
}

SHARD_DESC_PREFIXES_ES: List[Tuple[str, str]] = [
    ("DiT 音视频主干 BF16 ", "Troncal DiT A/V BF16 "),
    ("多模态编码器 BF16 ", "Codificador multimodal BF16 "),
    ("权重分片 ", "Fragmento de pesos "),
    ("编码器 ", "Codificador de texto "),
    ("DiT A/V Backbone BF16 ", "Troncal DiT A/V BF16 "),
    ("Multimodal Encoder BF16 ", "Codificador multimodal BF16 "),
    ("Weight Shard ", "Fragmento de pesos "),
    ("Text Encoder ", "Codificador de texto "),
]


def translate_shard_desc_es(desc: str) -> str:
    if not desc:
        return desc
    if desc in SHARD_DESC_EXACT_ES:
        return SHARD_DESC_EXACT_ES[desc]
    for src_p, dst_p in SHARD_DESC_PREFIXES_ES:
        if desc.startswith(src_p):
            return dst_p + desc[len(src_p) :]
    return desc


# ─── Server / colab_bridge.py / Run Logs (Chinese -> Spanish) ─────────────────

SERVER_EXACT_ZH_TO_ES: Dict[str, str] = {
    "尚未连接云端 GPU": "GPU en la nube sin conectar",
    "云端 ComfyUI 尚未启动": "ComfyUI en la nube no iniciado",
    "Google Drive 自动软链持久化": "Persistencia automática por enlace en Google Drive",
    "Google Drive 实时软链挂载": "Enlace directo en vivo de Google Drive montado",
    "Google Drive 云盘自动持久化": "Persistencia automática en la nube con Google Drive",
    "实例本地高速存储": "Almacenamiento local rápido de la instancia",
    "尚未启动（支持一键拉起 ComfyUI + Google Drive 自动软链持久化）": (
        "No iniciado (ComfyUI en 1 clic + persistencia automática en Google Drive)"
    ),
    "ComfyUI 已停止（节点、模型与工作流已持久化保存至 Google Drive）": (
        "ComfyUI detenido (nodos, modelos y flujos guardados en Google Drive)"
    ),
    "正在初始化 ComfyUI 环境与 Google Drive 持久化目录...": (
        "Inicializando entorno ComfyUI y carpetas persistentes de Google Drive..."
    ),
    "正在释放现有常驻模型显存，为 ComfyUI 腾出完整 96GB 空间...": (
        "Liberando modelos residentes de la VRAM para dejar los 96GB libres a ComfyUI..."
    ),
    "正在从 Google Drive 恢复历史持久化的 ComfyUI 节点、模型与工作流...": (
        "Restaurando nodos personalizados, modelos y flujos de ComfyUI desde Google Drive..."
    ),
    "正在克隆官方最新 ComfyUI 核心引擎...": "Clonando el motor oficial más reciente de ComfyUI...",
    "正在安装 ComfyUI 核心依赖（保留当前 G4 Blackwell CUDA PyTorch）...": (
        "Instalando dependencias de ComfyUI (conservando CUDA PyTorch actual)..."
    ),
    "正在恢复已持久化的自定义节点并配置 ComfyUI-Manager...": (
        "Restaurando nodos personalizados y configurando ComfyUI-Manager..."
    ),
    "正在检查并安装已保存自定义节点的 Python 依赖包...": (
        "Comprobando e instalando paquetes Python de los nodos personalizados..."
    ),
    "正在拉起 ComfyUI 节点推理引擎 (端口 8188)...": "Iniciando motor de nodos ComfyUI (puerto 8188)...",
    "正在拉起 ComfyUI 节点推理引擎 (本地后端)...": "Iniciando motor de nodos ComfyUI (backend local)...",
    "ComfyUI 内核已就绪，正在建立 Cloudflare 高速全屏画布隧道...": (
        "Núcleo de ComfyUI listo; abriendo túnel Cloudflare para el lienzo..."
    ),
    "正在先从 Google Drive 检查已持久化的历史模型权重...": (
        "Comprobando pesos de modelos ya guardados en Google Drive..."
    ),
    "正在将配齐的模型与中文工作流持久化同步至 Google Drive...": (
        "Sincronizando modelos instalados y flujos con Google Drive..."
    ),
    "正在预装并校验 llama.cpp CUDA 高速推理引擎...": (
        "Preinstalando y verificando el motor de inferencia CUDA llama.cpp..."
    ),
    "正在映射 MiniMax-H3 BF16 多模态编码器权重 (14 分片)...": (
        "Mapeando pesos del codificador multimodal MiniMax-H3 BF16 (14 fragmentos)..."
    ),
    "正在映射 MiniMax-H3 BF16 33B DiT 主干权重 (13 分片)...": (
        "Mapeando pesos de la troncal DiT 33B MiniMax-H3 BF16 (13 fragmentos)..."
    ),
    "正在映射 3D 视频 VAE 与 32kHz 立体声 VAE 权重...": (
        "Mapeando pesos de VAE de video 3D y VAE de audio estéreo 32kHz..."
    ),
    "正在构建 MiniMax-H3 BF16 原生 GPU 计算图与 Processor...": (
        "Construyendo grafo GPU nativo BF16 y Processor de MiniMax-H3..."
    ),
    "正在映射 Qwen-Image-2.1 权重并构建 GPU 管线...": (
        "Mapeando pesos de Qwen-Image-2.1 y construyendo pipeline GPU..."
    ),
    "正在映射 Z-Image-Turbo 权重并构建 8 步极速生图管线...": (
        "Mapeando pesos de Z-Image-Turbo y construyendo pipeline turbo de 8 pasos..."
    ),
    "正在预热 Qwen3.8-27B-UD-Q4_K_M.gguf 与 mmproj 视觉权重...": (
        "Precalentando Qwen3.8-27B-UD-Q4_K_M.gguf y pesos visuales mmproj..."
    ),
    "正在自动补齐 Unsloth MTP 投机解码加速头 (1.31 GB)...": (
        "Descargando cabeza especulativa Unsloth MTP (1.31 GB)..."
    ),
    "正在检查账号下已有的 Colab 实例...": "Comprobando instancias Colab existentes en tu cuenta...",
    "旧实例已失效或正在销毁，正在自动清理并重新分配新实例...": (
        "La instancia anterior expiró; limpiando y asignando una nueva..."
    ),
    "容器仍在初始化，继续尝试连接内核...": (
        "El contenedor sigue inicializándose; reintentando conexión al kernel..."
    ),
    "正在上传最新多模型开源服务端代码 (app.py)...": (
        "Subiendo código del servidor multimodelo (app.py)..."
    ),
    "正在云端配置 Google Drive 持久化、多模型引擎并启动隧道 (约需 40~90 秒)...": (
        "Configurando persistencia Google Drive, motores y túnel (~40-90s)..."
    ),
    "尚未授权登录 Google 账号，请先点击「绑定账号」": (
        "Cuenta de Google sin autorizar. Pulsa primero 'Vincular'."
    ),
    "尚未登录 Google Colab CLI": "Sesión no iniciada en Google Colab CLI",
    "已释放全部云端实例": "Todas las instancias en la nube liberadas",
    "已释放全部云端实例。": "Todas las instancias en la nube liberadas.",
    # colab_bridge.py & app.py boot/runtime messages
    "检测到账号下残留未释放实例占用并发名额，正在自动清理后重试...": (
        "Se detectaron instancias residuales ocupando cuota; limpiando y reintentando..."
    ),
    "正在克隆 DiffSynth-Studio...": "Clonando DiffSynth-Studio...",
    "已通过自定义 OAuth 自动挂载 Google Drive (/content/drive/MyDrive)！": (
        "¡Google Drive montado automáticamente mediante OAuth personalizado (/content/drive/MyDrive)!"
    ),
    "─── 实时下载/采样进度流 ───": "─── Progreso de descarga/muestreo en vivo ───",
    "等待检查模型状态...": "Esperando comprobación del estado de modelos...",
    "缺失依赖自动安装完成。": "Dependencias faltantes instaladas correctamente.",
    "正在安装 Qwen3.8 GatedDeltaNet 原生 Triton 算子 (fla-core + flash-linear-attention)...": (
        "Instalando operadores Triton nativos Qwen3.8 GatedDeltaNet (fla-core + flash-linear-attention)..."
    ),
    "[MiniMax-H3-Image] 检测到当前 diffusers 版本不含 MiniMaxH3ImageModularPipeline，正在升级 diffusers>=0.43.0 ...": (
        "[MiniMax-H3-Image] La versión de diffusers no incluye MiniMaxH3ImageModularPipeline; actualizando diffusers>=0.43.0..."
    ),
    "[MiniMax-H3-Image] diffusers>=0.43.0 热升级校验通过！": (
        "[MiniMax-H3-Image] ¡Actualización a diffusers>=0.43.0 verificada!"
    ),
    "[MiniMax-H3-Image] 检测到高分辨率解码显存峰值，自动开启 VAE Tiling 并清理瞬态缓存重试...": (
        "[MiniMax-H3-Image] Pico de VRAM al decodificar alta resolución; activando VAE Tiling y reintentando..."
    ),
    "[GGUF 引擎] 检测到尚未缓存 MTP 投机解码权重，正在 8 路并发极速补齐...": (
        "[Motor GGUF] Pesos MTP sin caché; descargando en 8 hilos..."
    ),
    "[PromptCache] 命中 Qwen3-VL 32B 多模态编码缓存，0ms 瞬时跳过文本编码阶段！": (
        "[PromptCache] ¡Acierto en caché multimodal Qwen3-VL 32B; codificación de texto omitida en 0ms!"
    ),
    "整帧 VAE 解码显存触顶，正在清理缓存并自动切换为 Tiled 分块安全解码...": (
        "VRAM al límite en decodificación VAE completa; cambiando a decodificación por bloques Tiled..."
    ),
    "超长序列注意力显存触顶，正在自动释放闲置子模块并启用梯度检查点安全重试...": (
        "VRAM al límite en secuencia larga; liberando submódulos y reintentando con checkpointing..."
    ),
    "[ComfyUI] 服务与公网隧道已停止，GPU 显存已回收。": (
        "[ComfyUI] Servicio y túnel detenidos; VRAM de la GPU recuperada."
    ),
    "[ComfyUI] 正在从 Google Drive 同步已保存的节点、模型与工作流...": (
        "[ComfyUI] Sincronizando nodos, modelos y flujos guardados desde Google Drive..."
    ),
    "[ComfyUI] 正在克隆官方最新 ComfyUI 仓库...": (
        "[ComfyUI] Clonando el repositorio oficial más reciente de ComfyUI..."
    ),
    "[ComfyUI 云盘同步] 正在通过高速通道将自定义节点、模型与工作流同步至 Google Drive...": (
        "[ComfyUI Sync Drive] Sincronizando nodos, modelos y flujos con Google Drive..."
    ),
    "[ComfyUI 预置包] 权重与工作流已就绪，正在自动拉起 ComfyUI 全屏画布...": (
        "[Paquete ComfyUI] Pesos y flujos listos; iniciando lienzo ComfyUI..."
    ),
    "[任务控制] 已收到停止指令，正在中断当前 GPU 推理并清空进度缓存...": (
        "[Control de tareas] Señal de parada recibida; interrumpiendo inferencia GPU y limpiando caché..."
    ),
    "已手动停止当前推理任务": "Tarea de inferencia detenida manualmente",
    "已被新提交任务接替中断": "Interrumpida por una nueva tarea enviada",
    "任务已提交至 Colab 队列...": "Tarea enviada a la cola de Colab...",
    "尚未有任何模型加载至 GPU 显存！请先在左侧点击「下载权重」与「加载到显存」。": (
        "¡No hay ningún modelo cargado en VRAM! Pulsa 'Descargar' y 'Cargar en VRAM' a la izquierda."
    ),
    "当前指定模型未驻留显存，无需卸载。": "El modelo indicado no está en VRAM; no hace falta quitarlo.",
    "已终止推理并从显存卸载该模型": "Inferencia detenida y modelo descargado de la VRAM",
    "已释放 ComfyUI 驻留模型与显存缓存（画布保持在线）": (
        "Modelos de ComfyUI y caché VRAM liberados (el lienzo sigue activo)"
    ),
    "首尾帧模式下请至少提供首帧或尾帧图片": (
        "El modo fotograma inicial/final requiere al menos una imagen de inicio o fin"
    ),
    "图像编辑/重绘模式下请至少拖入一张输入图片": (
        "El modo de edición / redibujo requiere al menos una imagen de entrada"
    ),
    "正在同步 MiniMax-H3-Image 模块化配置与 Diffusers>=0.43 运行时...": (
        "Sincronizando configuración modular de MiniMax-H3-Image y entorno Diffusers>=0.43..."
    ),
    "正在自动升级 diffusers>=0.43.0 以支持 MiniMax-H3-Image 模块化管线...": (
        "Actualizando diffusers>=0.43.0 para soportar el pipeline modular de MiniMax-H3-Image..."
    ),
    "正在构建 MiniMax-H3-Image 本地零拷贝组装目录与共享编码器映射...": (
        "Construyendo carpeta local sin copia de MiniMax-H3-Image y mapa de codificador compartido..."
    ),
    "正在加载 MiniMax-H3-Image 调度器与多模态 Processor...": (
        "Cargando planificador y Processor multimodal de MiniMax-H3-Image..."
    ),
    "正在分层装载 32B 视觉文本编码器 (1/3)...": (
        "Cargando por capas el codificador visual-texto 32B (1/3)..."
    ),
    "正在分层装载 33B 图像 DiT 主干 (2/3)...": (
        "Cargando por capas la troncal DiT de imagen 33B (2/3)..."
    ),
    "正在装载 4K 16MP 图像 VAE 并开启分块解码保护 (3/3)...": (
        "Cargando VAE de imagen 4K 16MP con protección de decodificación por bloques (3/3)..."
    ),
    "正在将 32B 文本编码器装载至系统内存热备池（后续解析新提示词仅需 ~5 秒）...": (
        "Cargando codificador de texto 32B en caché RAM (~5s al cambiar de prompt)..."
    ),
    "正在准备潜空间与多模态编码...": "Preparando espacio latente y codificación multimodal...",
    "正在合成 32kHz 立体声音轨与 MP4 视频...": "Sintetizando pista estéreo 32kHz y video MP4...",
    "Qwen3.8-27B / Qwen3.8-27B-GGUF 尚未加载至 Colab GPU 显存，请先在 Mac 客户端点击「加载到显存」。": (
        "Qwen3.8-27B / Qwen3.8-27B-GGUF aún no está en VRAM. Pulsa 'Cargar en VRAM' en el cliente."
    ),
    "请先在客户端加载 MiniMax-H3-Image、Qwen-Image-2.1 或 Z-Image-Turbo 至显存。": (
        "Carga primero MiniMax-H3-Image, Qwen-Image-2.1 o Z-Image-Turbo en la VRAM desde el cliente."
    ),
    "已自动切换至内置专属引擎「MiniMax-H3-Image (33B · 4K)」（仅下载 Diffusers 必需 27 个分片，并自动零拷贝共享 MiniMax-H3 的 66.7GB 编码器权重）！": (
        "¡Cambiado al motor integrado 'MiniMax-H3-Image (33B · 4K)' (solo baja los 27 fragmentos de Diffusers y comparte sin copia los 66.7GB del codificador de MiniMax-H3)!"
    ),
}


def _translate_gguf_fit(fit_desc: str) -> str:
    if fit_desc == "MoE 异构驻留 (Attention GPU + Experts CPU)":
        return "Residencia híbrida MoE (Attention GPU + Experts CPU)"
    if fit_desc == "全量 GPU 驻留":
        return "100% en GPU"
    m = re.fullmatch(r"混合驻留 \((\d+)/65 层 GPU\)", fit_desc)
    if m:
        return f"Residencia mixta ({m.group(1)}/65 capas GPU)"
    return fit_desc


def _translate_mode_label(lbl: str) -> str:
    out = lbl.replace("内存热备", "caché RAM").replace("双主干", "doble troncal")
    out = out.replace("BF16 原生", "BF16 nativo").replace("8步极速 BF16", "BF16 turbo 8 pasos")
    out = out.replace("全量 GPU", "100% GPU")
    return out


def _translate_pack_title(title: str) -> str:
    zh_to_es = {
        "万相 Wan2.2 14B · 图生视频 + 首尾帧双工作流": "Wan2.2 14B · Imagen a video + flujos duales inicio/fin",
        "MiniMax-H3 Turbo · 图生有声视频 + 首尾帧双工作流": "MiniMax-H3 Turbo · I2V audio-video + flujos inicio/fin",
        "LTX-2.3 (22B) · 首尾帧电影级运镜有声工作流": "LTX-2.3 (22B) · Control de cámara cinematográfico inicio/fin + audio",
        "混元 HunyuanVideo 1.5 · 单图直出 1080P 超分工作流": "HunyuanVideo 1.5 · Flujo directo 1080P super-resolución desde 1 imagen",
    }
    return zh_to_es.get(title, title)


def _translate_stage_label(lbl: str) -> str:
    mapping = {
        "高清图像 VAE 解码": "decodificación VAE de imagen HD",
        "3D 视频 VAE 解码": "decodificación VAE de video 3D",
        "3D 视频与音频 VAE 解码": "decodificación VAE de video 3D y audio",
        "多模态提示词编码": "codificación multimodal de prompt",
        "32kHz 立体声解码": "decodificación estéreo 32kHz",
    }
    return mapping.get(lbl, lbl)


# Live text progress bars that app.py writes into ACTIVE_TQDM_BARS["sampling"], e.g.
# "DiT 去噪采样:  98%|##########| 49/50 [00:18<00:00, 0.36s/step] · 总进度 88%".
_BAR_LABELS_ZH_TO_ES = {
    "DiT 去噪采样": "Muestreo DiT",
    "提示词编码": "Codificación de prompt",
    "音视频封装": "Empaquetado MP4",
    "MiniMax-H3-Image 采样": "Muestreo MiniMax-H3-Image",
    "高清图像 VAE 解码": "Decodificación VAE de imagen HD",
    "3D 视频 VAE 解码": "Decodificación VAE de video 3D",
    "3D 视频与音频 VAE 解码": "Decodificación VAE de video 3D y audio",
    "32kHz 立体声解码": "Decodificación estéreo 32kHz",
}

_BAR_TAIL_RULES_ZH_TO_ES: List[Tuple[re.Pattern[str], str]] = [
    (re.compile(r"^(\d+/\d+) \[(\S+)<(\S+), ([\d.]+)s/step\] · 总进度 (\d+)%$"), r"\1 [\2<\3, \4s/paso] · total \5%"),
    (re.compile(r"^(\d+/\d+) \[正在执行第 (\d+/\d+) 步\.\.\.\]$"), r"\1 [ejecutando paso \2...]"),
    (
        re.compile(r"^DiT 采样已完成 \((\d+/\d+)，耗时 (\S+)\) -> 正在解码输出\.\.\.$"),
        r"muestreo DiT completado (\1, \2) -> decodificando la salida...",
    ),
    (re.compile(r"^正在解析画面、运镜与声音提示词\.\.\.$"), "analizando prompts de imagen, cámara y sonido..."),
    (re.compile(r"^正在将潜空间张量解码为高清像素\.\.\.$"), "decodificando el espacio latente a píxeles HD..."),
    (re.compile(r"^正在解码双声道环境音与配乐波形\.\.\.$"), "decodificando ambiente y música en estéreo..."),
    (re.compile(r"^正在编码 H\.264 视频与 32kHz 立体声 MP4\.\.\.$"), "codificando MP4 con video H.264 y audio estéreo 32kHz..."),
    (re.compile(r"^(\d+) 步 PDD 蒸馏推理中 \((.+?)\)\.\.\.$"), r"inferencia destilada PDD en \1 pasos (\2)..."),
]


def _translate_progress_bar(m: "re.Match[str]") -> str:
    label = _BAR_LABELS_ZH_TO_ES.get(m.group(1).strip(), m.group(1))
    tail = m.group(4)
    for pattern, repl in _BAR_TAIL_RULES_ZH_TO_ES:
        if pattern.search(tail):
            tail = pattern.sub(repl, tail)
            break
    return f"{label}: {m.group(2)}%|{m.group(3)}| {tail}"


SERVER_REGEX_ZH_TO_ES: List[Tuple[re.Pattern[str], Any]] = [
    # app.py live progress bars ("<label>: NN%|####------| <detail>")
    (re.compile(r"^([^:|]*[一-鿿][^:|]*):\s*(\d+)%\|([^|]*)\|\s*(.*)$"), _translate_progress_bar),
    # colab_bridge.py wake & stop messages
    (
        re.compile(r"^尚未授权登录 Google 账号，请先点击「\s*绑定账号」$"),
        "Cuenta de Google sin autorizar. Pulsa primero 'Vincular'.",
    ),
    (
        re.compile(r"^🛑?\s*已彻底释放全部云端实例！当前计费速率:\s*([\d.]+)\s*CU/小时$"),
        r"¡Todas las instancias en la nube liberadas! Tasa de consumo actual: \1 CU/h",
    ),
    (
        re.compile(
            r"^Google Colab 当前区域 (.+?) 算力池繁忙 \((.+?)\)，(\d+) 秒后进行第 (\d+)/(\d+) 次申请\.\.\.$"
        ),
        r"Pool de \1 ocupado en esta región de Google Colab (\2); reintento \4/\5 en \3s...",
    ),
    (
        re.compile(
            r"^Google Colab 云端当前时段 (.+?) 算力池库存不足 \((.+?)\)，连续 (\d+) 次申请均未分到机器"
            r"（属于 Colab 官方高配机型时段性缺货，非本地客户端故障）。建议稍等几分钟再试，或在左侧临时切换为 A100 / L4 实例。$"
        ),
        r"Sin stock disponible para \1 en Google Colab ahora (\2) tras \3 intentos "
        r"(falta temporal de capacidad en Colab, no es un fallo del cliente). Espera unos minutos o cambia temporalmente a A100 / L4.",
    ),
    (
        re.compile(
            r"^Google Colab 拒绝分配 (.+?) \(HTTP 412\)：当前账号并发实例数已达上限，或该时段高配机型触发临时配额限制。"
            r"请确认未在其他浏览器标签页占用实例，稍后重试或临时切换为 A100 / L4。$"
        ),
        r"Google Colab rechazó asignar \1 (HTTP 412): límite de instancias concurrentes o cuota temporal alcanzada. "
        r"Verifica que no tengas otra instancia abierta en el navegador, reintenta luego o cambia a A100 / L4.",
    ),
    (
        re.compile(
            r"^Google Colab 后端拒绝分配 (.+?) \(HTTP 400\)：当前账号订阅等级可能暂不支持该机型或可用计算单元不足，"
            r"建议切换为 A100 / L4 / T4 实例。$"
        ),
        r"Google Colab rechazó asignar \1 (HTTP 400): es posible que tu suscripción no admita esta GPU o falten CU. Prueba con A100 / L4 / T4.",
    ),
    (
        re.compile(r"^检测到云端(?:已在后台|已)完成 (.+?) 实例分配，直接接管！$"),
        r"¡Instancia \1 asignada en segundo plano detectada en la nube; tomando control!",
    ),
    (
        re.compile(r"^正在向 Google Colab 申请分配 (.+?) 实例\.\.\.$"),
        r"Solicitando instancia \1 a Google Colab...",
    ),
    (
        re.compile(r"^成功分配 (.+?) 云端虚拟机！正在等待容器内核就绪\.\.\.$"),
        r"¡VM en la nube \1 asignada! Esperando a que el kernel arranque...",
    ),
    (
        re.compile(r"^正在检查已有实例 \[(.+?)\] \((.+?)\) 连通性\.\.\.$"),
        r"Comprobando conectividad de la instancia existente [\1] (\2)...",
    ),
    (
        re.compile(r"^旧实例 \((.+?)\) 已失效或正在销毁，准备清理\.\.\.$"),
        r"La instancia anterior (\1) expiró o se está cerrando; preparando limpieza...",
    ),
    (
        re.compile(
            r"^当前已占用实例 \[(.+?)\]，正在彻底释放并等待配额就绪以切换为 \[(.+?)\]\.\.\.$"
        ),
        lambda m: (
            f"Instancia actual [{'instancia anterior' if m.group(1) == '旧实例' else m.group(1)}] en uso; "
            f"liberando y esperando cuota para cambiar a [{m.group(2)}]..."
        ),
    ),
    (
        re.compile(r"^当前已分配实例型号为 \[(.+?)\]，正在释放并切换为您选择的 \[(.+?)\]\.\.\.$"),
        r"Instancia asignada actual [\1]; liberando y cambiando a [\2]...",
    ),
    (
        re.compile(r"^启动超时，日志尾部:\s*(.*)$", re.DOTALL),
        r"Tiempo de arranque agotado. Últimos registros: \1",
    ),
    # Existing models.py server regex rules translated directly to Spanish
    (
        re.compile(r"^已无缝接管在线 ComfyUI 画布（(.+?)）$"),
        lambda m: f"Reconectado al lienzo activo de ComfyUI ({localize_server_text_es(m.group(1))})",
    ),
    (
        re.compile(r"^ComfyUI 进程已退出 \(code=([^)]+)\)，可点击重新启动$"),
        r"El proceso de ComfyUI terminó (code=\1). Pulsa para reiniciar.",
    ),
    (
        re.compile(r"^正在建立 (.+?) 目录软链 \(models / workflows / output\)\.\.\.$"),
        lambda m: f"Enlazando directorios de {localize_server_text_es(m.group(1))} (models / workflows / output)...",
    ),
    (
        re.compile(r"^正在 8 线程极速下载 (.+?) 至 (.+?)\.\.\.$"),
        r"Descargando en 8 hilos \1 a \2...",
    ),
    (
        re.compile(r"^正在下载 (.+?) 至 (.+?)\.\.\.$"),
        r"Descargando \1 a \2...",
    ),
    (
        re.compile(r"^正在准备配齐「(.+?)」（共 (\d+) 个官方权重）\.\.\.$"),
        lambda m: f'Preparando paquete "{_translate_pack_title(m.group(1))}" ({m.group(2)} pesos oficiales)...',
    ),
    (
        re.compile(r"^正在生成「(.+?)」全中文三步傻瓜注释工作流\.\.\.$"),
        lambda m: f'Generando plantillas guiadas para "{_translate_pack_title(m.group(1))}"...',
    ),
    (
        re.compile(r"^正在为 (.+?) 启动 8 路并发 HTTP Range 极速下载通道\.\.\.$"),
        r"Iniciando descarga HTTP Range en 8 hilos para \1...",
    ),
    (
        re.compile(r"^\[(\d+/\d+)\] (.+?) 已就绪 \((.+?)\)，跳过下载$"),
        r"[\1] \2 listo (\3), omitido",
    ),
    (
        re.compile(r"^\[(\d+/\d+)\] 正在 8 线程并发下载 (.+?) \((.+?)\)\.\.\.$"),
        lambda m: f"[{m.group(1)}] Descargando en 8 hilos {m.group(2)} ({translate_shard_desc_es(m.group(3))})...",
    ),
    (
        re.compile(r"^正在获取 (.+?) 的分词器与 Processor 配置文件\.\.\.$"),
        r"Obteniendo tokenizador y configuración de Processor para \1...",
    ),
    (
        re.compile(r"^正在评估显存余量并装载 (.+?) 至 GPU\.\.\.$"),
        r"Evaluando VRAM libre y cargando \1 en GPU...",
    ),
    (
        re.compile(r"^\[显存常驻加速\] 正在将子模块 (.+?) 预热锁入 GPU 显存\.\.\.$"),
        r"[Caché VRAM] Precalentando y fijando submódulo \1 en VRAM...",
    ),
    # app.py RAMDisk, deps, acceleration, cache, Drive, ComfyUI & job logs
    (
        re.compile(r"^\[RAMDisk 内存盘加速已开启\] /dev/shm 可用空间 ([\d.]+) GB \(2\.4GB/s 零延迟读写\)$"),
        r"[RAMDisk activado] /dev/shm libre: \1 GB (lectura/escritura rápida 2.4GB/s)",
    ),
    (
        re.compile(r"^正在自动安装缺失的运行期依赖:\s*(.+?)\s*\.\.\.$"),
        r"Instalando dependencias faltantes en tiempo de ejecución: \1...",
    ),
    (
        re.compile(r"^检测到 torchaudio 动态库异常 \((.+?)\)，正在自动对齐 PyTorch \((.+?)\) ABI\.\.\.$", re.DOTALL),
        r"Detectada incompatibilidad en torchaudio (\1); alineando ABI con PyTorch (\2)...",
    ),
    (
        re.compile(r"^torchaudio 已自动修复对齐至 (.+?)！$"),
        r"¡torchaudio reparado y alineado a \1!",
    ),
    (
        re.compile(r"^\[加速引擎\] Triton causal_conv1d 注册跳过:\s*(.+)$", re.DOTALL),
        r"[Motor acelerado] Registro Triton causal_conv1d omitido: \1",
    ),
    (
        re.compile(r"^\[加速引擎\] accelerate hook 拆除跳过:\s*(.+)$", re.DOTALL),
        r"[Motor acelerado] Retirada de hook accelerate omitida: \1",
    ),
    (
        re.compile(r"^\[加速引擎\] 算子融合未完成 \((.+)\)$", re.DOTALL),
        r"[Motor acelerado] Fusión de operadores no completada (\1)",
    ),
    (
        re.compile(
            r"^\[加速引擎\] 全 64 层融合算子 \+ CUDAGraph 静态图引擎已就绪 \(CUDAGraph 静态加速 (\d+) tokens / 动态最大上下文 (\d+) tokens\)！$"
        ),
        r"[Motor acelerado] 64 capas fusionadas + CUDAGraph listos (estático \1 tokens / contexto máx. \2 tokens)",
    ),
    (
        re.compile(r"^\[加速引擎\] CUDAGraph 未捕获，融合算子仍保留 \((.+)\)$", re.DOTALL),
        r"[Motor acelerado] CUDAGraph no capturado; se conservan operadores fusionados (\1)",
    ),
    (
        re.compile(r"^\[自定义模型\] 读取 (.+?) 跳过:\s*(.+)$", re.DOTALL),
        r"[Modelo personalizado] Lectura de \1 omitida: \2",
    ),
    (
        re.compile(r"^\[自定义模型\] 写入 (.+?) 跳过:\s*(.+)$", re.DOTALL),
        r"[Modelo personalizado] Escritura de \1 omitida: \2",
    ),
    (
        re.compile(r"^\[自定义模型\] (.+)$", re.DOTALL),
        lambda m: f"[Modelo personalizado] {localize_server_text_es(m.group(1))}",
    ),
    (
        re.compile(r"^\[显存管理\] (.+)$", re.DOTALL),
        lambda m: f"[Gestión VRAM] {localize_server_text_es(m.group(1))}",
    ),
    (
        re.compile(r"^\[ComfyUI 云盘持久化\] (.+)$", re.DOTALL),
        lambda m: f"[ComfyUI Drive] {localize_server_text_es(m.group(1))}",
    ),
    (
        re.compile(r"^\[Google Drive 同步完成\] (.+?) -> (.+)$"),
        r"[Sync Google Drive completado] \1 -> \2",
    ),
    (
        re.compile(r"^\[Google Drive 同步失败\] (.+?):\s*(.+)$", re.DOTALL),
        r"[Error al sincronizar Google Drive] \1: \2",
    ),
    (
        re.compile(r"^\[Google Drive 同步异常\] (.+?):\s*(.+)$", re.DOTALL),
        r"[Excepción al sincronizar Google Drive] \1: \2",
    ),
    (
        re.compile(r"^\[后台云盘同步完成\] (.+?) 已持久化保存至 Google Drive$"),
        r"[Sync en segundo plano listo] \1 guardado en Google Drive",
    ),
    (
        re.compile(r"^\[后台云盘同步跳过\] (.+?):\s*(.+)$", re.DOTALL),
        r"[Sync en segundo plano omitido] \1: \2",
    ),
    (
        re.compile(r"^多线程分片直连回退至标准 HF 下载 \((.+)\)\.\.\.$", re.DOTALL),
        r"Descarga directa multihilo recurriendo a descarga estándar de HF (\1)...",
    ),
    (
        re.compile(r"^\[自动省额度看门狗\] 已连续闲置 (\d+) 分钟，正在自动释放 Colab 虚拟机\.\.\.$"),
        r"[Vigilancia CU] \1 min sin actividad; liberando instancia Colab automáticamente...",
    ),
    (
        re.compile(
            r"^Google Drive 剩余空间 \(([\d.]+) GB\) 小于 (.+?) 待下载增量 \(([\d.]+) GB\)，自动改用实例本地高速 NVMe 磁盘 \((.+?)\) 存储！$"
        ),
        r"Espacio libre en Google Drive (\1 GB) menor que la descarga pendiente de \2 (\3 GB); usando disco NVMe local (\4).",
    ),
    (
        re.compile(
            r"^\[MiniMax-H3-Image\] 已启用官方 ComponentsManager 自动显存/内存热备轮换 \(VRAM ([\d.]+)GB / 可用 RAM ([\d.]+)GB\)$"
        ),
        r"[MiniMax-H3-Image] Rotación automática VRAM/RAM con ComponentsManager activada (VRAM \1GB / RAM libre \2GB)",
    ),
    (
        re.compile(r"^正在将 (.+?) \(([\d.]+) GB\) 高速预热至 /dev/shm 内存盘\.\.\.$"),
        r"Precargando \1 (\2 GB) en RAMDisk /dev/shm...",
    ),
    (
        re.compile(r"^(.+?) 内存盘预热完成 \((\d+) MB/s\)$"),
        r"\1 precargado en RAMDisk (\2 MB/s)",
    ),
    (
        re.compile(r"^内存盘预热跳过 \((.+)\)，直接读取原路径$"),
        r"Precarga en RAMDisk omitida (\1); leyendo desde ruta original",
    ),
    (
        re.compile(r"^\[NVMe 高速缓存\] 正在将 (.+?) \((\d+) 个分片 / ([\d.]+) GB\) 从云盘顺序预热至本地 NVMe SSD\.\.\.$"),
        r"[Caché NVMe] Copiando \1 (\2 fragmentos / \3 GB) desde Drive al SSD NVMe local...",
    ),
    (
        re.compile(r"^\[NVMe 高速缓存\] (.+?) 本地 SSD 预热完成 \((\d+) MB/s\)$"),
        r"[Caché NVMe] Precarga en SSD local de \1 completada (\2 MB/s)",
    ),
    (
        re.compile(r"^本地 NVMe 预热跳过 \((.+)\)，继续读取原路径$"),
        r"Precarga en NVMe local omitida (\1); leyendo desde ruta original",
    ),
    (
        re.compile(r"^\[GGUF 引擎\] GitHub Releases 查询跳过，使用稳定镜像版本 ([^\s]+) \((.+)\)$", re.DOTALL),
        r"[Motor GGUF] Consulta a GitHub Releases omitida; usando versión estable \1 (\2)",
    ),
    (
        re.compile(r"^\[GGUF 引擎\] 正在下载官方预编译 llama\.cpp CUDA 12 推理后端:\s*(.+?)\s*\.\.\.$"),
        r"[Motor GGUF] Descargando binario CUDA 12 de llama.cpp: \1...",
    ),
    (
        re.compile(r"^\[GGUF 引擎\] 正在下载配套 CUDA 12 Runtime 动态库 \((.+?)\)\.\.\.$"),
        r"[Motor GGUF] Descargando librerías CUDA 12 Runtime (\1)...",
    ),
    (
        re.compile(r"^\[GGUF 引擎\] llama-server CUDA 引擎校验通过 \((.+)\)$"),
        r"[Motor GGUF] Motor CUDA llama-server verificado (\1)",
    ),
    (
        re.compile(
            r"^\[GGUF 引擎\] 正在启动 (.+?) 服务 \(上下文 (\d+K)=(\d+), KV=([^,]+), GPU采样, ([^,]+), port=(\d+)\)\.\.\.$"
        ),
        lambda m: (
            f"[Motor GGUF] Iniciando {m.group(1).replace(' + MTP 多词元投机解码', ' + decodificación MTP')} "
            f"(contexto {m.group(2)}={m.group(3)}, KV={m.group(4)}, muestreo GPU, "
            f"{_translate_gguf_fit(m.group(5))}, puerto={m.group(6)})..."
        ),
    ),
    (
        re.compile(
            r"^正在将 (.+?) 装载至 GPU \((\d+K) 上下文 · KV ([^·]+?) · (.+?)\)\.\.\.$"
        ),
        lambda m: (
            f"Cargando {m.group(1).replace(' + MTP 多词元投机解码', ' + decodificación MTP')} en GPU "
            f"(contexto {m.group(2)} · KV {m.group(3).strip()} · {_translate_gguf_fit(m.group(4))})..."
        ),
    ),
    (
        re.compile(r"^\[GGUF 引擎\] (.+?) 已就绪 \((.+)\)$"),
        lambda m: f"[Motor GGUF] {m.group(1)} listo ({_translate_mode_label(m.group(2))})",
    ),
    (
        re.compile(r"^\[GGUF 引擎\] 当前配置 \((.+?)\) 显存触顶，自动降级重试\.\.\.$"),
        r"[Motor GGUF] VRAM al límite con (\1); reintentando con perfil reducido...",
    ),
    (
        re.compile(r"^\[GGUF 引擎\] MTP 投机权重获取跳过，将以标准模式启动:\s*(.+)$", re.DOTALL),
        r"[Motor GGUF] Descarga de pesos MTP omitida; iniciando en modo estándar: \1",
    ),
    (
        re.compile(
            r"^\[G4 大内存热备\] 检测到充裕系统内存 \(([\d.]+)/([\d.]+) GB\)，已启用 32B 文本编码器 \+ 33B DiT 双主干 DDR5 内存常驻热备（阶段切换仅需 ~5 秒）！$"
        ),
        r"[Caché RAM G4] Memoria amplia (\1/\2 GB); activada caché DDR5 para codificador 32B + DiT 33B (cambio en ~5s).",
    ),
    (
        re.compile(
            r"^正在将 MiniMax-H3 预装载至 (\d+)GB 高速系统内存热备池（首次载入后换提示词仅需 ~5 秒）\.\.\.$"
        ),
        r"Precargando MiniMax-H3 en caché RAM de \1GB (tras la carga inicial, cambiar de prompt tarda ~5s)...",
    ),
    (
        re.compile(
            r"^\[混合内存热备\] 系统可用内存 ([\d.]+)/([\d.]+) GB，已将 32B 文本编码器锁入系统内存热备（换提示词 ~5 秒极速换入），DiT 走本地高速存储！$"
        ),
        r"[Caché RAM híbrida] RAM disponible \1/\2 GB; codificador 32B fijado en RAM (~5s al cambiar prompt) y DiT en disco rápido.",
    ),
    (
        re.compile(r"^检测到分词器或 transformers 组件缺失 \((.+)\)，正在自动升级 transformers 及分词器依赖\.\.\.$", re.DOTALL),
        r"Falta tokenizador o componente de transformers (\1); actualizando dependencias...",
    ),
    (
        re.compile(
            r"^\[PromptEmbedder\] 多模态提示词解析完成，总耗时 ([\d.]+)s（已写入缓存，同提示词换种子后续 0ms）$"
        ),
        r"[PromptEmbedder] Codificación multimodal completada en \1s (guardada en caché; 0ms al cambiar de Seed)",
    ),
    (
        re.compile(r"^\[PromptEmbedder\] 多模态提示词解析完成，总耗时 ([\d.]+)s$"),
        r"[PromptEmbedder] Codificación multimodal completada en \1s",
    ),
    (
        re.compile(r"^Prompt 缓存挂载跳过:\s*(.+)$", re.DOTALL),
        r"Montaje de caché de prompts omitido: \1",
    ),
    (
        re.compile(r"^\[极速显存换入\] 子模块 (.+?) 已整块载入 GPU 显存，耗时 ([\d.]+)s$"),
        r"[Carga rápida VRAM] Submódulo \1 cargado en GPU en \2s",
    ),
    (
        re.compile(r"^\[大显存常驻已激活\] 管线子模块已预热至显存 \(当前总驻留 ([\d.]+) GB / ([\d.]+) GB\)$"),
        r"[Residencia VRAM activa] Submódulos precargados en VRAM (\1 GB / \2 GB en uso)",
    ),
    # Model catalog / download / load / unload
    (
        re.compile(r"^无法获取仓库 (.+?) 详情，请检查名称或填写 HF Token$"),
        r"No se pudieron obtener detalles de \1; revisa el nombre o tu HF Token",
    ),
    (
        re.compile(
            r"^已成功导入自定义模型「(.+?)」\((.+?) · 共 (\d+) 个文件 / 约 ([\d.]+) GB\)，可立即下载权重并加载到显存！$"
        ),
        r"Modelo personalizado '\1' importado (\2 · \3 archivos / ~\4 GB). ¡Ya puedes descargar los pesos y cargarlo en VRAM!",
    ),
    (
        re.compile(r"^已从模型中心移除自定义模型「(.+?)」$"),
        r"Modelo personalizado '\1' eliminado del centro de modelos",
    ),
    (
        re.compile(
            r"^(.+?) 全部 (\d+)/(\d+) 个权重文件已就绪（共 ([\d.]+) GB），现在可点击「加载到显存」！$"
        ),
        r"¡Todos los pesos de \1 listos (\2/\3 · \4 GB)! Ya puedes pulsar 'Cargar en VRAM'.",
    ),
    (
        re.compile(r"^下载 (.+?) 权重出错:\s*(.+)$", re.DOTALL),
        r"Error al descargar pesos de \1: \2",
    ),
    (
        re.compile(r"^正在通过 ComponentsManager 装载 MiniMax-H3-Image 至 (\d+)GB 内存热备池与 GPU\.\.\.$"),
        r"Cargando MiniMax-H3-Image con ComponentsManager en caché RAM de \1GB y GPU...",
    ),
    (
        re.compile(
            r"^正在将 (.+?) 高速缓存至本地 SSD \((\d+)/(\d+)\)，消除后续换入延迟\.\.\.$"
        ),
        r"Cacheando \1 en SSD local (\2/\3) para evitar esperas posteriores...",
    ),
    (
        re.compile(r"^正在使用 Diffusers 装载自定义图像模型 (.+?)\.\.\.$"),
        r"Cargando modelo de imagen personalizado \1 con Diffusers...",
    ),
    (
        re.compile(r"^正在装载 (.+?) Transformers 原生权重 \(上下文上限 (\d+K)\)\.\.\.$"),
        r"Cargando pesos nativos Transformers de \1 (contexto máx. \2)...",
    ),
    (
        re.compile(r"^正在预热 (.+?) GGUF 权重并启动 llama\.cpp CUDA 引擎\.\.\.$"),
        r"Precalentando pesos GGUF de \1 e iniciando motor CUDA llama.cpp...",
    ),
    (
        re.compile(r"^加载 (.+?) 至显存失败:\s*(.+)$", re.DOTALL),
        r"Error al cargar \1 en VRAM: \2",
    ),
    (
        re.compile(
            r"^已从显存卸载 (.+?)，当前可用显存 ([\d.]+) GB （(.+?)）$"
        ),
        lambda m: (
            f"{m.group(1)} descargado de la VRAM; VRAM libre: {m.group(2)} GB "
            f"({re.sub(r'显存中仍保留 (\d+) 个常驻模型', lambda rm: f'queda 1 modelo en VRAM' if rm.group(1) == '1' else f'quedan {rm.group(1)} modelos en VRAM', m.group(3)).replace('显存已完全清空', 'VRAM completamente libre')})"
        ),
    ),
    (
        re.compile(
            r"^(.+?) 已装载至显存 \(([^，]+)，约 ([\d.]+)GB，耗时 ([\d.]+)s\)(?: \| 当前共 (\d+) 个模型同时常驻显存，切换 0 等待)?！(（因显存上限已自动腾退 [^）]+）)?(.*)$",
            re.DOTALL,
        ),
        lambda m: (
            f"¡{m.group(1)} cargado en VRAM ({_translate_mode_label(m.group(2))}, ~{m.group(3)}GB, {m.group(4)}s)"
            + (f" | {m.group(5)} modelos residentes a la vez (cambio instantáneo)" if m.group(5) else "")
            + (
                re.sub(
                    r"（因显存上限已自动腾退 ([^）]+)）",
                    r" (se liberó \1 por límite de VRAM)",
                    m.group(6),
                )
                if m.group(6)
                else ""
            )
            + (m.group(7) or "")
        ),
    ),
    # ComfyUI server logs & status messages
    (
        re.compile(r"^\[ComfyUI\] 生成默认占位参考图提示:\s*(.+)$", re.DOTALL),
        r"[ComfyUI] Aviso al generar imagen de referencia inicial: \1",
    ),
    (
        re.compile(r"^\[ComfyUI\] 写入 EasyColab 默认工作流引导扩展提示:\s*(.+)$", re.DOTALL),
        r"[ComfyUI] Aviso al escribir extensión guía de flujos: \1",
    ),
    (
        re.compile(r"^\[ComfyUI 工作流生成\] (.+?) 模板处理异常:\s*(.+)$", re.DOTALL),
        r"[Generador ComfyUI] Excepción en plantilla \1: \2",
    ),
    (
        re.compile(r"^\[ComfyUI\] 已自动接管实例上正在运行的 ComfyUI 服务:\s*(.+)$"),
        r"[ComfyUI] Conectado al servicio ComfyUI ya activo en la instancia: \1",
    ),
    (
        re.compile(r"^\[ComfyUI\] 正在为已持久化的自定义节点自动恢复 (\d+) 项 Python 依赖\.\.\.$"),
        r"[ComfyUI] Restaurando \1 dependencias Python de nodos personalizados...",
    ),
    (
        re.compile(r"^\[ComfyUI\] 正在预装核心插件 (.+?)\.\.\.$"),
        r"[ComfyUI] Preinstalando extensión clave \1...",
    ),
    (
        re.compile(r"^\[ComfyUI\] 画布公网隧道已开通:\s*(.+)$"),
        r"[ComfyUI] Túnel público del lienzo abierto: \1",
    ),
    (
        re.compile(r"^\[ComfyUI 极速下载\] (.+?) -> (.+?) -> (.+)$"),
        r"[ComfyUI descarga rápida] \1 -> \2 -> \3",
    ),
    (
        re.compile(r"^\[ComfyUI 直链下载\] (.+?) -> (.+)$"),
        r"[ComfyUI descarga directa] \1 -> \2",
    ),
    (
        re.compile(r"^\[ComfyUI 预置包\] \((\d+/\d+)\) 已存在跳过:\s*(.+)$"),
        r"[Paquete ComfyUI] (\1) Ya existe, omitido: \2",
    ),
    (
        re.compile(r"^\[ComfyUI 预置包\] \((\d+/\d+)\) 开始 8 线程下载 (.+?) -> (.+)$"),
        r"[Paquete ComfyUI] (\1) Iniciando descarga en 8 hilos \2 -> \3",
    ),
    (
        re.compile(r"^\[ComfyUI 预置包\] (.+)$", re.DOTALL),
        lambda m: f"[Paquete ComfyUI] {localize_server_text_es(m.group(1))}",
    ),
    (
        re.compile(r"^已持久化至 (.+?)（节点 (\d+) 个 · 权重 (\d+) 个 · 工作流 (\d+) 个）$"),
        lambda m: (
            f"Guardado en {localize_server_text_es(m.group(1))} "
            f"({m.group(2)} nodos · {m.group(3)} pesos · {m.group(4)} flujos)"
        ),
    ),
    (
        re.compile(r"^ComfyUI 已就绪（(.+?) · 节点 (\d+) 个 · 权重 (\d+) 个）$"),
        lambda m: f"ComfyUI listo ({localize_server_text_es(m.group(1))} · {m.group(2)} nodos · {m.group(3)} pesos)",
    ),
    (
        re.compile(r"^ComfyUI 启动出错:\s*(.+)$", re.DOTALL),
        r"Error al iniciar ComfyUI: \1",
    ),
    (
        re.compile(
            r"^权重 (.+?) \(([\d.]+) GB\) 已下载至 models/(.+?) 并持久化到 (.+?)（在画布按 R 键即可刷新选用）$"
        ),
        lambda m: (
            f"Peso {m.group(1)} ({m.group(2)} GB) descargado en models/{m.group(3)} y guardado en "
            f"{localize_server_text_es(m.group(4))} (pulsa R en el lienzo para actualizar)"
        ),
    ),
    (
        re.compile(r"^\[(\d+/\d+)\] 正在 8 线程极速下载 (.+?) \(约 ([\d.]+) GB\)\.\.\.$"),
        r"[\1] Descargando en 8 hilos \2 (~\3 GB)...",
    ),
    (
        re.compile(r"^「(.+?)」已全部配齐！打开画布左侧「工作流」点击 (.+?) 即可直接传图运行$"),
        lambda m: f"¡'{_translate_pack_title(m.group(1))}' listo! Abre 'Workflows' a la izquierda del lienzo y elige {m.group(2)} para ejecutarlo.",
    ),
    (
        re.compile(r"^「(.+?)」已配齐且画布已启动！在左侧「工作流」打开中文模板即可直接出片$"),
        lambda m: f"¡'{_translate_pack_title(m.group(1))}' instalado y lienzo iniciado! Abre una plantilla en 'Workflows' a la izquierda para empezar.",
    ),
    # Generation / inference / job logs
    (
        re.compile(r"^(.+?): 子阶段已完成，正在继续后续合成封装\.\.\.$"),
        lambda m: f"{_translate_stage_label(m.group(1))}: subetapa completada; empaquetando resultado...",
    ),
    (
        re.compile(r"^(\[[^\]]+\]\s*)?(.+?) 正在编码多模态上下文并启动推理\.\.\.$"),
        r"\1\2 codificando contexto multimodal e iniciando inferencia...",
    ),
    (
        re.compile(r"^(.+?) 正在深度思考 \((.+)\)\.\.\.$"),
        r"\1 pensando en profundidad (\2)...",
    ),
    (
        re.compile(r"^(.+?) 正在流式输出回复 \((.+)\)\.\.\.$"),
        r"\1 transmitiendo respuesta (\2)...",
    ),
    (
        re.compile(r"^(.+?) 推理完成！耗时 ([\d.]+s)(.*)$"),
        lambda m: (
            f"¡Inferencia de {m.group(1)} completada! Duración {m.group(2)}"
            + m.group(3).replace(" · 共 ", " · ").replace(" tokens", " tokens")
        ),
    ),
    (
        re.compile(r"^\[(.+?)\] 推理完成 \| (\d+) tokens \| ([\d.]+) tok/s \| 耗时 ([\d.]+s)$"),
        r"[\1] Inferencia completada | \2 tokens | \3 tok/s | Duración \4",
    ),
    (
        re.compile(r"^(\[[^\]]+\]\s*)?(.+?) 正在使用多模态编码器解析提示词 \((\d+)%\)\.\.\.$"),
        r"\1\2 codificando prompt con el codificador multimodal (\3%)...",
    ),
    (
        re.compile(r"^(\[[^\]]+\]\s*)?DiT 采样已完成，正在执行(.+?) \((\d+)%\)\.\.\.$"),
        lambda m: f"{m.group(1) or ''}Muestreo DiT completado; ejecutando {_translate_stage_label(m.group(2))} ({m.group(3)}%)...",
    ),
    (
        re.compile(r"^(\[[^\]]+\]\s*)?视频帧解码完成，正在执行 32kHz 立体声音轨解码 \((\d+)%\)\.\.\.$"),
        r"\1Fotogramas decodificados; decodificando pista de audio estéreo 32kHz (\2%)...",
    ),
    (
        re.compile(r"^(\[[^\]]+\]\s*)?(.+?) 正在执行去噪采样第 (\d+)/(\d+) 步 \((\d+)%\)\.\.\.$"),
        r"\1\2 ejecutando paso de muestreo \3/\4 (\5%)...",
    ),
    (
        re.compile(
            r"^(\[[^\]]+\]\s*)?(.+?) 正在采样 (\d+)/(\d+) 步 \(总进度 (\d+)% · ([\d.]+s)/步 · 采样剩余约 (\d+s)\)\.\.\.$"
        ),
        r"\1\2 muestreando paso \3/\4 (total \5% · \6/paso · ~\7 restantes)...",
    ),
    (
        re.compile(r"^(\[[^\]]+\]\s*)?DiT 采样已完成 \((\d+/\d+)\)，正在进入(.+?) \((\d+)%\)\.\.\.$"),
        lambda m: f"{m.group(1) or ''}Muestreo DiT completado ({m.group(2)}); iniciando {_translate_stage_label(m.group(3))} ({m.group(4)}%)...",
    ),
    (
        re.compile(r"^\[(.+?)\] DiT 采样 (\d+/\d+) 步完成 \(([\d.]+s)\)，开始执行(.+?)\.\.\.$"),
        lambda m: f"[{m.group(1)}] Muestreo DiT {m.group(2)} pasos listo ({m.group(3)}); iniciando {_translate_stage_label(m.group(4))}...",
    ),
    (
        re.compile(r"^(.+?) 尚未加载到 GPU 显存！请先在左侧点击「加载到显存」（显存充裕时可与现有模型同时常驻）。$"),
        r"¡\1 aún no está en VRAM! Pulsa 'Cargar en VRAM' a la izquierda (si hay VRAM libre, convive con los modelos activos).",
    ),
    (
        re.compile(r"^(.+?) 尚未加载至 GPU 显存！请先在左侧点击「加载到显存」。$"),
        r"¡\1 aún no está en VRAM! Pulsa primero 'Cargar en VRAM' a la izquierda.",
    ),
    (
        re.compile(
            r"^(.+?) 尚未加载到显存（当前已常驻：(.+?)）。请点击左侧「加载到显存」，显存充裕时可同时常驻无需卸载现有模型。$"
        ),
        r"\1 no está en VRAM (activos: \2). Pulsa 'Cargar en VRAM' a la izquierda; si hay espacio, conviven sin quitarlos.",
    ),
    (
        re.compile(r"^正在准备 (.+?) 推理管线(?: \(共 (\d+) 项\))?\.\.\.$"),
        lambda m: (
            f"Preparando pipeline de inferencia de {m.group(1)}"
            + (f" ({m.group(2)} elementos)" if m.group(2) else "")
            + "..."
        ),
    ),
    (
        re.compile(r"^(\[[^\]]+\]\s*)?正在等待上一任务释放 GPU 显存锁\.\.\.$"),
        r"\1Esperando a que la tarea anterior libere el bloqueo de GPU...",
    ),
    (
        re.compile(r"^(\[[^\]]+\]\s*)?(.+?) 正在初始化潜空间并准备 (\d+) 步推理 \(Seed: (\d+)\)\.\.\.$"),
        r"\1\2 inicializando espacio latente y preparando \3 pasos (Seed: \4)...",
    ),
    (
        re.compile(r"^(\[[^\]]+\]\s*)?VAE 解码完成，正在合成 32kHz 立体声音轨并封装 MP4 \((\d+)%\)\.\.\.$"),
        r"\1Decodificación VAE lista; mezclando pista estéreo 32kHz y empaquetando MP4 (\2%)...",
    ),
    (
        re.compile(r"^(\[[^\]]+\]\s*)?正在写入无损 PNG 图像文件 \((\d+)%\)\.\.\.$"),
        r"\1Guardando archivo de imagen PNG sin pérdida (\2%)...",
    ),
    (
        re.compile(r"^(\[[^\]]+\]\s*)?正在执行 MiniMax-H3-Image (\d+) 步 PDD 蒸馏原生超清采样 \(([^)]+)\)\.\.\.$"),
        r"\1Ejecutando muestreo HD destilado PDD de \2 pasos en MiniMax-H3-Image (\3)...",
    ),
    (
        re.compile(r"^第 (\d+/\d+) 项已完成 \(([\d.]+s)\)，已同步回传 Mac！继续生成第 (\d+) 项\.\.\.$"),
        r"Elemento \1 completado (\2) y enviado al equipo. Generando el elemento \3...",
    ),
    (
        re.compile(r"^批量生成 (\d+) 项全部完成！总耗时 ([\d.]+s) \(平均 ([\d.]+s)/项\)$"),
        r"¡Lote de \1 elementos completado! Total \2 (promedio \3/elemento)",
    ),
    (
        re.compile(r"^生成完成！耗时 ([\d.]+s) \(Seed: (\d+)\)$"),
        r"¡Generación completada! Duración \1 (Seed: \2)",
    ),
    (
        re.compile(r"^\[(.+?)\] (图像|视频)生成完成 \| 耗时 ([\d.]+s) \| Seed: (\d+) \| 已保存:\s*(.+)$"),
        lambda m: (
            f"[{m.group(1)}] {'Imagen generada' if m.group(2) == '图像' else 'Video generado'} | "
            f"Duración {m.group(3)} | Seed: {m.group(4)} | Guardado: {m.group(5)}"
        ),
    ),
    (
        re.compile(r"^生成出错:\s*(.+)$", re.DOTALL),
        r"Error al generar: \1",
    ),
    (
        re.compile(r"^\[任务控制\] 任务 (.+?) 已中断并释放 GPU 显存锁\.$"),
        r"[Control de tareas] Tarea \1 interrumpida; bloqueo de VRAM liberado.",
    ),
    (
        re.compile(r"^任务已提交至 Colab 队列 \(共 (\d+) 项\)\.\.\.$"),
        r"Tarea enviada a la cola de Colab (\1 elementos)...",
    ),
    (
        re.compile(r"^\[上下文配置\] 目标最大上下文长度已设为 (\d+K) \((\d+) tokens\)$"),
        r"[Contexto] Longitud máxima de contexto ajustada a \1 (\2 tokens)",
    ),
    (
        re.compile(r"^\[(OpenAI|Anthropic) API\] 流式完成 \| (\d+) tokens \| ([\d.]+) tok/s$"),
        r"[\1 API] Stream completado | \2 tokens | \3 tok/s",
    ),
]


def localize_server_text_es(text: str) -> str:
    """Translate server / bridge status strings & console log lines into Spanish."""
    if not text:
        return text
    m_ts = _TS_PREFIX_RE.match(text)
    ts_prefix = m_ts.group(1) if m_ts else ""
    body = m_ts.group(2) if m_ts else text
    stripped = _LEADING_DECOR_RE.sub("", body.strip())
    if not stripped:
        return text

    if stripped in SERVER_EXACT_ZH_TO_ES:
        return ts_prefix + SERVER_EXACT_ZH_TO_ES[stripped]
    for pattern, repl in SERVER_REGEX_ZH_TO_ES:
        if pattern.search(stripped):
            return ts_prefix + pattern.sub(repl, stripped)  # type: ignore[arg-type]

    out = stripped
    for src_p, dst_p in SHARD_DESC_PREFIXES_ES:
        if src_p in out:
            out = out.replace(src_p, dst_p)
    for src_exact, dst_exact in SHARD_DESC_EXACT_ES.items():
        if src_exact in out:
            out = out.replace(src_exact, dst_exact)

    if out == stripped and not _CJK_RE.search(stripped):
        out = translate_en_to_es(stripped)
    return ts_prefix + out


# ─── Live Language-Switch Helpers for ViewModel ──────────────────────────────


def swap_runtime_text(
    val: str,
    pairs: List[Tuple[str, str]],
    current_lang: str,
    localize_fn: Callable[[str], str],
) -> str:
    cur = normalize_lang(current_lang)
    for zh_txt, en_txt in pairs:
        es_txt = translate_en_to_es(en_txt)
        if val in (zh_txt, en_txt, es_txt):
            if cur == "zh":
                return zh_txt
            if cur == "es":
                return es_txt
            return en_txt
    return localize_fn(val) if cur != "zh" else val


def swap_preset_visual(val: str, templates: Sequence[Any], current_lang: str) -> str:
    for tpl in templates:
        if tpl.visual_en and tpl.visual_en != tpl.visual_zh:
            es_vis = translate_en_to_es(tpl.visual_en)
            if val in (tpl.visual_zh, tpl.visual_en, es_vis):
                return tpl.visual
    return val
