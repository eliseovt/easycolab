package app.easycolab.studio

/**
 * Traducción al español ("es") y localización de mensajes del servidor/puente
 * para el cliente Android de EasyColab (mismo glosario que windows_app/i18n_es.py).
 */
object LocalizationEs {

    private val CJK_REGEX = Regex("[\\u4e00-\\u9fff]")
    private val TS_PREFIX_REGEX = Regex("""^(\[\d{2}:\d{2}:\d{2}\]\s*)(.*)$""", RegexOption.DOT_MATCHES_ALL)

    fun fromCode(code: String?): AppLanguage {
        val norm = (code ?: "").trim().lowercase()
        return when {
            norm.startsWith("es") -> AppLanguage.ES
            norm.startsWith("en") -> AppLanguage.EN
            else -> AppLanguage.ZH
        }
    }

    fun nextLanguage(lang: AppLanguage): AppLanguage = when (lang) {
        AppLanguage.ZH -> AppLanguage.ES
        AppLanguage.ES -> AppLanguage.EN
        AppLanguage.EN -> AppLanguage.ZH
    }

    fun nextLangButtonLabel(lang: AppLanguage): String = when (lang) {
        AppLanguage.ZH -> "ES"
        AppLanguage.ES -> "EN"
        AppLanguage.EN -> "中文"
    }

    fun hasCjk(text: String): Boolean = CJK_REGEX.containsMatchIn(text)

    private fun stripLeadingDecor(text: String): String {
        var i = 0
        while (i < text.length) {
            val cp = Character.codePointAt(text, i)
            val isDecor = Character.isWhitespace(cp)
                || (cp in 0x1F1E6..0x1F1FF)
                || (cp in 0x1F300..0x1FAFF)
                || (cp in 0x2300..0x23FF)
                || (cp in 0x2600..0x27BF)
                || cp == 0xFE0F || cp == 0x200D || cp == 0x20E3 || cp == 0x2139
            if (!isDecor) break
            i += Character.charCount(cp)
        }
        return text.substring(i)
    }

    private fun plural(nStr: String, singular: String, plural: String): String =
        if (nStr == "1") singular else plural

    private fun translatePackTitle(title: String): String = when (title.trim()) {
        "万相 Wan2.2 14B · 图生视频 + 首尾帧双工作流" -> "Wan2.2 14B · Imagen a video + flujos duales inicio/fin"
        "MiniMax-H3 Turbo · 图生有声视频 + 首尾帧双工作流" -> "MiniMax-H3 Turbo · I2V audio-video + flujos inicio/fin"
        "MiniMax-H3 Turbo · 图生有声视频 + 首尾帧" -> "MiniMax-H3 Turbo · I2V audio-video + inicio/fin"
        "LTX-2.3 (22B) · 首尾帧电影级运镜有声工作流" -> "LTX-2.3 (22B) · Control de cámara cinematográfico inicio/fin + audio"
        "混元 HunyuanVideo 1.5 · 单图直出 1080P 超分工作流" -> "HunyuanVideo 1.5 · Flujo directo 1080P super-resolución desde 1 imagen"
        "混元 HunyuanVideo 1.5 · 单图直出 1080P 超分" -> "HunyuanVideo 1.5 · 1080P super-resolución desde 1 imagen"
        else -> translateEn(title)
    }

    private fun translateStageLabel(lbl: String): String = when (lbl.trim()) {
        "高清图像 VAE 解码" -> "decodificación VAE de imagen HD"
        "3D 视频 VAE 解码" -> "decodificación VAE de video 3D"
        "3D 视频与音频 VAE 解码" -> "decodificación VAE de video 3D y audio"
        "多模态提示词编码" -> "codificación multimodal de prompt"
        "32kHz 立体声解码" -> "decodificación estéreo 32kHz"
        else -> lbl
    }

    private fun translateGgufFit(fitDesc: String): String {
        if (fitDesc == "MoE 异构驻留 (Attention GPU + Experts CPU)") {
            return "Residencia híbrida MoE (Attention GPU + Experts CPU)"
        }
        if (fitDesc == "全量 GPU 驻留") {
            return "100% en GPU"
        }
        val m = Regex("""^混合驻留 \((\d+)/65 层 GPU\)$""").matchEntire(fitDesc)
        if (m != null) {
            return "Residencia mixta (${m.groupValues[1]}/65 capas GPU)"
        }
        return fitDesc
    }

    private fun translateModeLabel(lbl: String): String = lbl
        .replace("内存热备", "caché RAM")
        .replace("双主干", "doble troncal")
        .replace("BF16 原生", "BF16 nativo")
        .replace("8步极速 BF16", "BF16 turbo 8 pasos")
        .replace("全量 GPU", "100% GPU")

    // ─── Inglés -> Español: diccionario estático ────────────────────────────

    private val EN_TO_ES: Map<String, String> = mapOf(
        // ColabNativeBridge.kt
        "Missing client_id or client_secret in JSON" to "Falta client_id o client_secret en el JSON",
        "Google account not bound" to "Cuenta de Google sin vincular",
        "Session expired, please sign in again" to "Sesión caducada, inicia sesión de nuevo",
        "Failed to refresh Google token" to "No se pudo actualizar el token de Google",
        "Too many active Colab instances (HTTP 412). Terminate existing VMs first." to "Demasiadas instancias Colab activas (HTTP 412). Libera las existentes primero.",
        "Failed to obtain assignment token. Check CU balance." to "No se pudo obtener el token de asignación. Revisa tu saldo CU.",
        "Allocation failed: check paid CU balance or try L4 / A100." to "Error al asignar GPU: revisa tu saldo CU o prueba con L4 / A100.",
        "Checking active Colab cloud instances on your account..." to "Comprobando instancias Colab activas en tu cuenta...",
        "Previous runtime expired; allocating a fresh VM..." to "La instancia anterior expiró; asignando una nueva VM...",
        "Uploading latest multi-model server engine (app.py)..." to "Subiendo código del servidor multimodelo (app.py)...",
        "Configuring Google Drive persistence, multi-model engine & public tunnel (~40–90s)..." to "Configurando persistencia en Google Drive, motores y túnel (~40-90s)...",
        "Timed out waiting for gradio.live tunnel URL" to "Tiempo agotado esperando la URL del túnel gradio.live",
        // MainActivity.kt: barra inferior y guía rápida
        "Create" to "Crear",
        "Cloud" to "Nube",
        "Gallery" to "Galería",
        "Console" to "Ajustes",
        "1. 1-Tap Google Sign-In" to "1. Vincula Google en 1 toque",
        "Sign in with Google via Chrome Custom Tabs — redirects right back to the app and syncs your paid CU balance." to "Inicia sesión con Google en Chrome Custom Tabs: volverás automáticamente a la app y se sincronizará tu saldo CU.",
        "2. Headless G4 (96GB) Wake" to "2. Activa G4 (96GB) sin navegador",
        "Provision an RTX PRO 6000 (96GB) VM headlessly with automatic rclone Google Drive weight persistence." to "Asigna una VM RTX PRO 6000 (96GB) directamente y monta Google Drive con rclone para conservar tus pesos.",
        "3. 5 Multimodal Engines + ComfyUI" to "3. 5 motores multimodales + ComfyUI",
        "Create stereo audio-videos, posters, photo edits, 256K CoT reasoning, and 4 preset ComfyUI video packs." to "Crea videos con audio estéreo, carteles, edición de fotos, razonamiento CoT 256K y 4 paquetes ComfyUI de video.",
        "4. Auto-Save & Zero Idle Drain" to "4. Guardado automático y ahorro de CU",
        "Outputs auto-save to Android Gallery; idle auto-sleep and 1-tap VM termination protect your CU balance." to "Las salidas se guardan en tu galería; el reposo por inactividad y el cierre en 1 toque protegen tus CU.",
        "Next" to "Siguiente",
        "Go to Cloud Tab" to "Ir a Nube",
        "Skip" to "Omitir",
        // StudioCloudAndSettingsViews.kt: Chat Qwen, API y ComfyUI
        "Sync" to "Sincronizar",
        "Thinking Mode" to "Modo pensamiento",
        "Tap to pick photo for Vision / Prompt Reverse" to "Toca para elegir imagen (visión / deducir prompt)",
        "Clear" to "Limpiar",
        "Ask anything, code, or reverse-prompt..." to "Escribe tu pregunta, código o análisis visual...",
        "Stop" to "Detener",
        "Send to Cloud Qwen3.8" to "Enviar a Qwen3.8",
        "▼ Hide Reasoning" to "▼ Ocultar razonamiento",
        "Thinking..." to "Pensando...",
        "Built-in dual-protocol gateway compatible with OpenAI (/v1) & Anthropic Claude Code (/v1/messages):" to "Pasarela dual integrada compatible con OpenAI (/v1) y Anthropic Claude Code (/v1/messages):",
        "Enable Bearer API Key Auth" to "Exigir autenticación con API Key",
        "API Key copied" to "API Key copiada",
        "Copied OpenAI /v1 URL" to "URL OpenAI /v1 copiada",
        "Copied Claude Code CLI setup" to "Configuración de Claude Code CLI copiada",
        "Cloud ComfyUI Node Studio" to "Estudio de nodos ComfyUI en la nube",
        "Running" to "En línea",
        "Stopped" to "Detenido",
        "Open Canvas" to "Abrir lienzo",
        "Start Cloud ComfyUI" to "Iniciar ComfyUI",
        "1-Tap Preset Video Workflow Packs" to "Paquetes de video predefinidos en 1 toque",
        "Ready · Open" to "Listo · Abrir",
        "Install Pack" to "Instalar",
        "Cloud 8-Thread Weight Downloader & Outputs" to "Descargador rápido (8 hilos) y salidas",
        "HF Repo or Direct Download URL" to "Repo HF o URL directa de descarga",
        "Download" to "Descargar",
        "Recent ComfyUI Outputs (Tap to pull to phone)" to "Salidas recientes de ComfyUI (toca para bajar)",
        "Pull" to "Bajar",
        // StudioCloudAndSettingsViews.kt: Nube GPU, túnel, auto-reposo, OAuth, consola y ajustes
        "Native Headless Colab Engine" to "Motor Colab nativo",
        "Google Colab Account" to "Cuenta de Google Colab",
        "Unbind" to "Desvincular",
        "Sign in Google" to "Vincular Google",
        "Paid CU Balance" to "Saldo CU",
        "Hourly Burn Rate" to "Consumo por hora",
        "Target GPU" to "GPU objetivo",
        "Provisioning Cloud GPU..." to "Asignando GPU en la nube...",
        "Colab Tunnel Endpoint (gradio.live)" to "Túnel de Colab (gradio.live)",
        "Connect & Sync" to "Conectar y sincronizar",
        "Tunnel URL copied" to "URL del túnel copiada",
        "Unload" to "Quitar",
        "15 min Idle Auto-Stop" to "Liberar tras 15 min inactivo",
        "30 min Idle Auto-Stop" to "Liberar tras 30 min inactivo",
        "60 min Idle Auto-Stop" to "Liberar tras 60 min inactivo",
        "Disable Auto-Sleep" to "Sin auto-liberación",
        "Idle CU Protection" to "Protección de saldo CU",
        "Terminate All Cloud VMs (0 CU/h)" to "Liberar instancias (0 CU/h)",
        "Terminate All Cloud Instances?" to "¿Liberar todas las instancias?",
        "Syncs ComfyUI outputs to Google Drive and unassigns all active Colab GPU runtimes so billing drops to 0.00 CU/h immediately." to "Sincroniza las salidas de ComfyUI con Google Drive y cierra todas las instancias Colab activas para detener el consumo (0.00 CU/h).",
        "Terminate Now" to "Liberar ahora",
        "Cancel" to "Cancelar",
        "Manual Google OAuth Code" to "Código manual de Google OAuth",
        "If your browser cannot redirect automatically, copy the auth link, sign in, and paste the 4/0A... authorization code here:" to "Si el navegador no vuelve automáticamente a la app, copia el enlace, inicia sesión y pega aquí el código 4/0A...:",
        "Copy Google Auth URL" to "Copiar URL de Google Auth",
        "Verify Code" to "Verificar código",
        "Close" to "Cerrar",
        "Console logs copied" to "Registros copiados al portapapeles",
        "Preferences" to "Preferencias",
        "Auto-Save to Android Gallery" to "Guardar automáticamente en galería",
        "Videos -> Movies/EasyColab, Images -> Pictures/EasyColab" to "Videos en Movies/EasyColab, imágenes en Pictures/EasyColab",
        "Streamer Privacy Mask" to "Máscara de privacidad",
        "Masks tunnel URL, account email & API key" to "Oculta la URL del túnel, correo y API Key",
        "Interface Language" to "Idioma de la interfaz",
        "HuggingFace Token (Optional)" to "HuggingFace Token (opcional)",
        "Advanced & Portable Tools" to "Herramientas avanzadas",
        "Export EasyColab_Server.ipynb" to "Exportar EasyColab_Server.ipynb",
        "Custom Google OAuth JSON (Active)" to "JSON Google OAuth propio (activo)",
        "Custom Google OAuth JSON (Optional)" to "JSON Google OAuth propio (opcional)",
        "Reopen 4-Step Quick Guide" to "Ver guía rápida de 4 pasos",
        "Custom Google OAuth Client JSON" to "JSON de cliente Google OAuth propio",
        "Built-in OAuth works out of the box. Paste your own Desktop client_secret.json to override, or save empty to restore default:" to "El OAuth integrado funciona directo. Pega tu propio client_secret.json de escritorio para reemplazarlo, o guarda vacío para restaurar el predeterminado:",
        "Save" to "Guardar",
        // StudioViewModel.kt & StudioViewModelServices.kt
        "Colab Server Disconnected" to "GPU en la nube sin conectar",
        "Not Loaded" to "Sin cargar",
        "Welcome to EasyColab Android Multimodal Cloud Studio" to "Bienvenido a EasyColab Android Multimodal Cloud Studio",
        "Pure-Kotlin native Colab G4 (96GB) client — 1-tap headless wake, auto-save to Gallery & idle CU protection." to "Cliente nativo de Colab G4 (96GB): activación en 1 toque, guardado en galería y ahorro de CU.",
        "Cloud ComfyUI Studio Not Started" to "ComfyUI en la nube no iniciado",
        "Google Drive Auto-Symlink Persistence" to "Persistencia automática por enlace en Google Drive",
        "Ready: Bind Google account in Cloud tab for 1-tap G4 wake, or paste an active gradio.live URL." to "Listo: vincula tu cuenta de Google en Nube para activar G4, o pega una URL gradio.live.",
        "Unbound" to "Sin vincular",
        "Authorized" to "Autorizada",
        "Auto-sleep off" to "Sin auto-liberación",
        "Failed to decode selected photo" to "No se pudo leer la foto seleccionada",
        "No active cloud runtime detected; cleared stale VRAM state." to "No hay instancia activa; estado de VRAM reiniciado.",
        "Sign in on the Google page and tap Allow — you will return to the app automatically..." to "Inicia sesión en Google y pulsa Permitir; volverás a la app automáticamente...",
        "Verifying Google authorization token..." to "Verificando token de autorización de Google...",
        "Google Account Bound!" to "¡Cuenta de Google vinculada!",
        "Auth URL copied — open in any browser" to "URL de acceso copiada; ábrela en un navegador",
        "Unbound local Google OAuth credentials." to "Credenciales locales de Google OAuth desvinculadas.",
        "Saved custom OAuth client JSON" to "JSON de cliente OAuth propio guardado",
        "Restored built-in OAuth client" to "Cliente OAuth integrado restaurado",
        "Please sign in with Google first." to "Vincula primero tu cuenta de Google.",
        "Terminating all cloud Colab VMs & stopping billing..." to "Liberando todas las instancias Colab y deteniendo el consumo...",
        "All cloud instances terminated (0 CU/h)." to "Todas las instancias en la nube liberadas (0 CU/h).",
        "Instances Terminated · 0 CU/h" to "Instancias liberadas · 0 CU/h",
        "Sent shutdown command to cloud runtime." to "Orden de cierre enviada a la instancia en la nube.",
        "Bind Google account to wake G4, or enter a gradio.live URL." to "Vincula tu cuenta de Google para activar G4 o introduce una URL gradio.live.",
        "Connecting & syncing cloud GPU status..." to "Conectando y sincronizando estado de la GPU...",
        "Lost connection to cloud server." to "Se perdió la conexión con el servidor en la nube.",
        "Weights Ready! Tap 'Load to VRAM'" to "¡Pesos listos! Toca '2. Cargar VRAM'",
        "Please tap 'Download Weights' first." to "Toca primero '1. Descargar' para bajar los pesos.",
        "Aborting cloud GPU inference..." to "Interrumpiendo inferencia en GPU...",
        "Stopped current generation job." to "Tarea de generación detenida.",
        "Please enter a prompt first!" to "¡Escribe primero un prompt!",
        "Please select at least 1 reference photo first." to "Elige primero al menos 1 foto de referencia.",
        "Not connected to Colab. Wake or connect in Cloud tab first." to "Sin conexión a Colab. Activa o conecta en la pestaña Nube primero.",
        "Tap 'Load to VRAM' above first." to "Toca primero '2. Cargar VRAM' arriba.",
        "Tap 'Download Weights' and 'Load to VRAM' first." to "Toca primero '1. Descargar' y '2. Cargar VRAM'.",
        "Please enter a valid HuggingFace Repo ID (e.g. unsloth/Qwen3.8-27B-GGUF)" to "Introduce un Repo ID de HuggingFace válido (ej. unsloth/Qwen3.8-27B-GGUF)",
        "Failed to resolve HuggingFace repo" to "No se pudo consultar el repo en HuggingFace",
        "Please connect to a cloud GPU runtime first." to "Conecta primero una instancia GPU en la nube.",
        "Deploying cloud ComfyUI & mounting Google Drive..." to "Desplegando ComfyUI en la nube y montando Google Drive...",
        "ComfyUI Canvas Ready!" to "¡Lienzo de ComfyUI listo!",
        "Synced to Google Drive" to "Sincronizado con Google Drive",
        "File no longer exists" to "El archivo ya no existe",
        "Video saved to Android Gallery!" to "¡Video guardado en la galería!",
        "Image saved to Android Gallery!" to "¡Imagen guardada en la galería!",
        "Failed to save to Android Gallery" to "Error al guardar en la galería",
        // TelemetryAndMediaViews.kt
        "Disk" to "Disco",
        "Live Cloud Telemetry" to "Telemetría en vivo",
        "Overlay" to "Superponer",
        "Split" to "Separar",
        "Google Drive" to "Google Drive",
        "Free" to "libre",
        "Delete this media item?" to "¿Eliminar este archivo?",
        "Delete" to "Eliminar",
        "Share" to "Compartir",
        "Local Gallery" to "Galería local",
        "No Downloaded Media Yet" to "Aún no hay archivos descargados",
        "Generated stereo videos, images, and pulled ComfyUI outputs appear here automatically." to "Los videos con audio, imágenes y salidas bajadas de ComfyUI aparecerán aquí.",
        "Save to Gallery" to "Guardar en galería",
        // WorkspaceViews.kt
        "Offline" to "Sin conexión",
        "+ Custom HF" to "+ Repo HF",
        "Import HF Repo" to "Importar repo HF",
        "Trending" to "Tendencias",
        "GGUF" to "GGUF",
        "LLM/VLM" to "LLM/VLM",
        "Img/Vid" to "Img/Vid",
        "Add Custom HuggingFace Repo" to "Añadir repositorio de HuggingFace",
        "Pick from live HuggingFace trending models below or enter any Repo ID. For gated/private repos, enter your HF Token and accept the license on HuggingFace." to "Elige un modelo en tendencia de HuggingFace o escribe un Repo ID. Para repos restringidos o privados, ingresa tu HF Token y acepta la licencia.",
        "Live HuggingFace Trending & Search" to "Tendencias y búsqueda en HuggingFace",
        "Loading..." to "Cargando...",
        "Refresh" to "Actualizar",
        "Search HF models..." to "Buscar modelos HF...",
        "Search" to "Buscar",
        "Fetching models, parameter counts & Colab VRAM fit..." to "Obteniendo modelos, parámetros y ajuste de VRAM...",
        "No models found. Tap 'Refresh' or try another keyword." to "Sin resultados. Toca 'Actualizar' o prueba otra palabra.",
        "[Gated] " to "[Con acceso] ",
        "Details" to "Info",
        "Model Details" to "Detalles del modelo",
        "Inspecting HuggingFace model metadata & shards..." to "Consultando metadatos y fragmentos en HuggingFace...",
        "Failed to load model details" to "No se pudieron cargar los detalles del modelo",
        "Weight Shards (Tap to Select):" to "Fragmentos disponibles (toca para elegir):",
        "README Excerpt:" to "Resumen del README:",
        "HuggingFace Repo ID or URL" to "Repo ID o URL de HuggingFace",
        "Pick from live trending above or enter owner/repo" to "Elige arriba o escribe usuario/repo",
        "Include Pattern (Optional)" to "Filtro de archivo (opcional)",
        "Display Name (Optional)" to "Nombre visible (opcional)",
        "Modality: Chat / Vision / API" to "Modalidad: Chat / visión / API",
        "Modality: Image Generation" to "Modalidad: Generación de imagen",
        "Modality: Video + Audio" to "Modalidad: Video + audio",
        "Modality: Auto-detect" to "Modalidad: Autodetectar",
        "Auto-detect" to "Autodetectar",
        "Chat / Vision / API" to "Chat / visión / API",
        "Image Generation" to "Generación de imagen",
        "Video + Audio" to "Video + audio",
        "HF Token (Required for Gated Repos)" to "HF Token (obligatorio en repos privados/restringidos)",
        "🔑 Get HF Token" to "🔑 Obtener HF Token",
        "🌐 Open Repo & Agree" to "🌐 Abrir repo y aceptar",
        "Add & Download" to "Añadir y bajar",
        "Add Model" to "Añadir modelo",
        "In VRAM" to "En VRAM",
        "Verify" to "Verificar",
        "1. Download" to "1. Descargar",
        "Unload VRAM" to "Quitar VRAM",
        "2. Load VRAM" to "2. Cargar VRAM",
        "Google Drive Persistence Active" to "Persistencia en Google Drive activa",
        "VRAM Offload" to "Gestión de VRAM",
        "Full GPU (96G)" to "Todo en GPU (96G)",
        "CPU RAM Offload" to "Caché en RAM CPU",
        "Smart Disk Offload" to "Modo disco inteligente",
        "Start Frame" to "Fotograma inicial",
        "Reference 1" to "Referencia 1",
        "End Frame (Opt)" to "Fotograma final (opc.)",
        "Reference 2 (Opt)" to "Referencia 2 (opc.)",
        "Visual & Camera Prompt" to "Prompt visual y movimiento de cámara",
        "Image & Typography Prompt" to "Prompt de imagen y tipografía",
        "Soundscape, Foley & Speech" to "Ambiente sonoro, efectos y diálogos",
        "Background Music" to "Música de fondo",
        "Output Resolution" to "Resolución de salida",
        "Randomize Seed" to "Seed aleatoria",
        "Batch Count" to "Cantidad por lote",
        "Generate Video + Stereo Audio" to "Generar video + audio estéreo",
        "Generate HD Image" to "Generar imagen HD",
        // LocalizationAndModels.kt: catálogo de modelos, resoluciones, plantillas y ComfyUI packs
        "MiniMax Video" to "MiniMax video",
        "Native BF16 · 134 GB" to "BF16 nativo · 134 GB",
        "Native BF16 HD video generation with synchronized 32kHz stereo SFX, speech & music" to "Generación BF16 nativa de video HD con efectos estéreo 32kHz, diálogos y música",
        "Text to Video+Audio" to "Texto a video + audio",
        "Generate HD video & stereo audio from visual and sound prompts" to "Genera video HD y audio estéreo describiendo escena y sonido",
        "Keyframes to Video" to "Fotogramas a video",
        "Pick start/end keyframes from Gallery to control motion" to "Elige fotogramas inicial/final de tu galería para guiar el movimiento",
        "Generate HD video & stereo audio from prompts" to "Genera video HD y audio estéreo a partir de prompts",
        "Pick start/end keyframes from Gallery" to "Elige fotogramas inicial/final de tu galería",
        "Z-Image Turbo" to "Z-Image turbo",
        "8-Step Turbo · 30.6 GB" to "Turbo 8 pasos · 30.6 GB",
        "8-step distilled photorealism & bilingual poster design model" to "Modelo destilado en 8 pasos para fotografía realista y carteles",
        "8-Step Text-to-Image" to "Texto a imagen en 8 pasos",
        "Seconds-fast commercial portrait & poster typography" to "Retratos comerciales y tipografía en carteles en segundos",
        "Image Restyle" to "Redibujo de imagen",
        "Pick a photo and adjust denoising strength" to "Elige una foto y ajusta la intensidad",
        "Pick a photo and adjust denoising strength to restyle" to "Elige una foto y ajusta la intensidad para reestilizar",
        "HD Text-to-Image" to "Texto a imagen HD",
        "Custom HuggingFace image generation" to "Generación de imagen personalizada en HuggingFace",
        "Qwen-Image 2.1" to "Qwen-Image 2.1",
        "Gen & Edit · 30.9 GB" to "Generar y editar · 30.9 GB",
        "Qwen flagship image generation & multi-image instruction editing" to "Modelo insignia de Qwen para generación de imagen y edición multi-imagen",
        "Complex layouts, accurate bilingual text & high-detail art" to "Composiciones complejas, texto preciso e ilustración detallada",
        "Instruction Photo Edit" to "Edición por instrucción",
        "Pick 1–2 photos to edit regions, swap backgrounds, or fuse subjects" to "Elige 1 o 2 fotos para editar zonas, cambiar fondos o fusionar sujetos",
        "Qwen3.8 GGUF" to "Qwen3.8 GGUF",
        "100 tok/s · 18.7 GB" to "100 tok/s · 18.7 GB",
        "UD-Q4_K_M + MTP speculative decoding (~100 tok/s), 256K context, vision & API gateway" to "Cuantización UD-Q4_K_M + decodificación MTP (~100 tok/s), 256K de contexto, visión y pasarela API",
        "Reasoning Chat" to "Chat de razonamiento",
        "CoT reasoning, coding & storyboards" to "Razonamiento CoT, programación y guiones",
        "Custom HuggingFace model chat & reasoning" to "Chat y razonamiento con modelo personalizado de HuggingFace",
        "Vision & Prompt" to "Visión y prompt",
        "Analyze photos, OCR & reverse-engineer prompts" to "Analiza fotos, extrae OCR y deduce prompts",
        "Multimodal photo analysis & prompt generation" to "Análisis multimodal de fotos y generación de prompts",
        "API Gateway" to "Pasarela API",
        "OpenAI (/v1) & Anthropic (/v1/messages) endpoints" to "Endpoints OpenAI (/v1) y Anthropic (/v1/messages)",
        "Qwen3.8 BF16" to "Qwen3.8 BF16",
        "Native BF16 · 51.8 GB" to "BF16 nativo · 51.8 GB",
        "Full native BF16 multimodal LLM, up to 256K context & vision understanding" to "LLM multimodal BF16 nativo completo, hasta 256K de contexto y visión",
        "Full BF16 CoT reasoning & scripting" to "Razonamiento CoT completo en BF16 y guiones",
        "High-precision photo analysis & prompt generation" to "Análisis visual de alta precisión y creación de prompts",
        "ComfyUI Studio" to "Estudio ComfyUI",
        "ComfyUI Node Studio" to "Estudio de nodos ComfyUI",
        "4 Preset Packs · Drive Sync" to "4 paquetes · sync Drive",
        "1-click cloud ComfyUI + 4 preset video packs, Chrome Custom Tab canvas & 1-tap pull to Android Gallery" to "ComfyUI en la nube en 1 toque + 4 paquetes de video, lienzo integrado y guardado en galería",
        "Workflows & Canvas" to "Flujos y lienzo",
        "Install Wan2.2 / MiniMax / LTX / Hunyuan packs & open canvas" to "Instala paquetes Wan2.2 / MiniMax / LTX / Hunyuan y abre el lienzo",
        "Weights & Outputs" to "Pesos y salidas",
        "8-thread cloud weight download & 1-tap pull outputs to phone" to "Descarga rápida en 8 hilos y envío de salidas al teléfono en 1 toque",
        "480 × 832 (9:16 Vertical Short · Pick)" to "480 × 832 (9:16 vertical corto · recomendado)",
        "832 × 480 (16:9 Landscape Standard)" to "832 × 480 (16:9 horizontal estándar)",
        "720 × 1280 (9:16 720P HD Vertical)" to "720 × 1280 (9:16 720P HD vertical)",
        "1280 × 720 (16:9 720P HD Landscape)" to "1280 × 720 (16:9 720P HD horizontal)",
        "640 × 640 (1:1 Square)" to "640 × 640 (1:1 cuadrado)",
        "768 × 1344 (9:16 Mobile Poster · Pick)" to "768 × 1344 (9:16 cartel móvil · recomendado)",
        "1024 × 1024 (1:1 Square HD)" to "1024 × 1024 (1:1 cuadrado HD)",
        "1344 × 768 (16:9 Cinematic Widescreen)" to "1344 × 768 (16:9 panorámico de cine)",
        "1536 × 1024 (3:2 DSLR Photo)" to "1536 × 1024 (3:2 foto DSLR)",
        "Makoto Shinkai · Cherry Blossom Railway" to "Makoto Shinkai · Paso a nivel entre cerezos",
        "Ufotable Sakuga · Azure Lightning Duel" to "Estilo ufotable · Duelo con relámpago azul",
        "Iceland Waterfall FPV Drone Dive" to "Dron FPV en cascada de Islandia",
        "Cyberpunk Neon Bund Poster" to "Cartel neón ciberpunk de Shanghái",
        "Storyboards" to "Storyboards",
        "Vision Prompt" to "Prompt visual",
        "Please design 3 vivid Makoto Shinkai-style anime short film storyboard shots. For each shot, provide: 1) Visual & Camera prompt; 2) Soundscape & SFX prompt; 3) Background Music prompt." to "Diseña 3 planos detallados para un corto de anime al estilo Makoto Shinkai. Para cada plano incluye: 1) prompt Visual & Camera (en inglés); 2) descripción de ambiente sonoro y SFX; 3) descripción de música de fondo.",
        "Carefully analyze the subject, lighting, color palette, camera framing, and artistic style of this image. First give a concise visual breakdown, then write a high-quality English image/video generation prompt." to "Analiza con detalle el sujeto, la iluminación, la paleta de color, el encuadre y el estilo artístico de esta imagen. Primero da un breve desglose en español y luego escribe un prompt de alta calidad en inglés para generar imagen o video.",
        // ComfyPresetPackItem
        "Wan2.2 14B · I2V + First/Last Frame" to "Wan2.2 14B · I2V + inicio/fin",
        "MiniMax-H3 Turbo · I2VA + Keyframes" to "MiniMax-H3 Turbo · I2VA + fotogramas",
        "LTX-2.3 (22B) · Cinematic Camera + Audio" to "LTX-2.3 (22B) · Cámara de cine + audio",
        "HunyuanVideo 1.5 · Direct 1080P Super-Res" to "HunyuanVideo 1.5 · 1080P super-resolución",
        "Beginner Pick · 4-Step" to "Recomendado · 4 pasos",
        "Stereo Audio · 8-Step" to "Audio estéreo · 8 pasos",
        "Camera Motion · 2 Weights" to "Cámara de cine · 2 pesos",
        "720P + 1080P Dual" to "Doble 720P + 1080P",
        "Single-Image I2V & First/Last-Frame templates (~25s on G4, 100% built-in nodes)" to "Flujos I2V de 1 imagen y transición inicio/fin (~25s en G4, nodos integrados)",
        "HD dynamic video + synchronized stereo SFX, speech & music in one pass" to "Video HD dinámico con efectos estéreo, diálogos y música sincronizados en una pasada",
        "Optimized for sweeping camera motion between start & end keyframes with audio" to "Optimizado para movimientos amplios de cámara entre fotogramas clave con audio",
        "Upload 1 image to render both 720P base video and 1920×1080 Full HD output" to "Sube 1 imagen para generar video base 720P y salida Full HD 1920×1080",
        // Etiquetas estáticas HF sizing
        "VRAM TBD" to "VRAM por determ.",
        "Size TBD" to "Tamaño por determ.",
        "T4 15G Ready" to "Apto T4 15G",
        "L4 24G Ready" to "Apto L4 24G",
        "A100 40G" to "A100 40G",
        "A100 80G" to "A100 80G",
        ">80G VRAM" to ">80G VRAM"
    )

    // ─── Inglés -> Español: plantillas regex para textos con variables ──────

    private val EN_REGEX_TO_ES: List<Pair<Regex, (MatchResult) -> String>> = listOf(
        // ColabNativeBridge.kt
        Regex("""^Terminated all cloud instances \((\d+)\)\. Current burn rate: ([\d.]+) CU/h$""") to { m ->
            "¡Instancias en la nube liberadas (${m.groupValues[1]})! Tasa actual: ${m.groupValues[2]} CU/h"
        },
        Regex("""^Requesting (.+?) instance from Google Colab\.\.\.$""") to { m ->
            "Solicitando instancia ${m.groupValues[1]} a Google Colab..."
        },
        Regex("""^Allocated (.+?) cloud VM! Waiting for Jupyter kernel\.\.\.$""") to { m ->
            "¡VM en la nube ${m.groupValues[1]} asignada! Esperando al kernel..."
        },
        Regex("""^Releasing \[(.+?)\] and switching to \[(.+?)\]\.\.\.$""") to { m ->
            "Liberando [${m.groupValues[1]}] y cambiando a [${m.groupValues[2]}]..."
        },
        Regex("""^Checking existing \((.+?)\) runtime connectivity\.\.\.$""") to { m ->
            "Comprobando conectividad de instancia (${m.groupValues[1]})..."
        },
        // StudioCloudAndSettingsViews.kt
        Regex("""^Context Window: (\d+)K Tokens$""") to { m ->
            "Ventana de contexto: ${m.groupValues[1]}K tokens"
        },
        Regex("""^Messages \((\d+)\)$""") to { m ->
            "Mensajes (${m.groupValues[1]})"
        },
        Regex("""^▶ View Reasoning \((\d+) chars\)$""") to { m ->
            "▶ Ver razonamiento (${m.groupValues[1]} caracteres)"
        },
        Regex("""^1-Tap Headless Wake \((.+?)\)$""") to { m ->
            "Activar GPU (${m.groupValues[1]}) en 1 toque"
        },
        Regex("""^Resident Models in VRAM \((\d+)\)$""") to { m ->
            "Modelos en VRAM (${m.groupValues[1]})"
        },
        Regex("""^Live Cloud Console \((.+?)\)$""") to { m ->
            "Consola en vivo (${m.groupValues[1]})"
        },
        // StudioViewModel.kt
        Regex("""^Auto-stop in (\d+)m (\d+)s$""") to { m ->
            "Auto-liberación en ${m.groupValues[1]}m ${m.groupValues[2]}s"
        },
        Regex("""^Cannot open browser: (.+)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "No se puede abrir el navegador: ${m.groupValues[1]}"
        },
        Regex("""^Failed to start auth session: (.+)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "Error al iniciar sesión de acceso: ${m.groupValues[1]}"
        },
        Regex("""^Signed in: (.+)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "Sesión iniciada: ${m.groupValues[1]}"
        },
        Regex("""^Sign-in incomplete: (.+)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "Inicio de sesión incompleto: ${m.groupValues[1]}"
        },
        Regex("""^Auth failed: (.+)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "Error de autenticación: ${m.groupValues[1]}"
        },
        Regex("""^Failed to create auth URL: (.+)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "Error al crear URL de autorización: ${m.groupValues[1]}"
        },
        Regex("""^Code verification failed: (.+)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            val err = if (m.groupValues[1] == "Invalid code") "código inválido" else m.groupValues[1]
            "Error al verificar código: $err"
        },
        Regex("""^Missing bundled app\.py in APK assets: (.+)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "Falta app.py integrado en el APK: ${m.groupValues[1]}"
        },
        Regex("""^Allocating (.+?) GPU & deploying server headlessly\.\.\.$""") to { m ->
            "Asignando GPU ${m.groupValues[1]} y desplegando servidor..."
        },
        Regex("""^=== Starting Native Headless Wake \((.+?)\) ===$""") to { m ->
            "=== Activando GPU Colab (${m.groupValues[1]}) ==="
        },
        Regex("""^Cloud (.+?) Ready & Connected!$""") to { m ->
            "¡${m.groupValues[1]} en la nube lista y conectada!"
        },
        Regex("""^Wake failed: (.+)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "Error al activar: ${localizeServerText(m.groupValues[1])}"
        },
        Regex("""^Cloud runtime unreachable \(HTTP (\d+)\)\.$""") to { m ->
            "Instancia en la nube inaccesible (HTTP ${m.groupValues[1]})."
        },
        // Nota de orden: reglas más específicas antes que `Connected to (.+)$`
        Regex("""^Connected to (.+?) · (.+?) ready in VRAM!$""") to { m ->
            "Conectado a ${m.groupValues[1]} · ¡${m.groupValues[2]} listo en VRAM!"
        },
        Regex("""^Connected to (.+?) · Ready to download & load models\.$""") to { m ->
            "Conectado a ${m.groupValues[1]} · Listo para descargar y cargar modelos."
        },
        Regex("""^Connected to (.+)$""") to { m ->
            "Conectado a ${m.groupValues[1]}"
        },
        Regex("""^Connection failed: (.+)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "Error de conexión: ${m.groupValues[1]}"
        },
        Regex("""^Starting 8-thread cloud download for (.+?)\.\.\.$""") to { m ->
            "Iniciando descarga en 8 hilos de ${m.groupValues[1]}..."
        },
        Regex("""^Weight download failed: (.+)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "Error al descargar pesos: ${m.groupValues[1]}"
        },
        Regex("""^Loading (.+?) into cloud GPU VRAM\.\.\.$""") to { m ->
            "Cargando ${m.groupValues[1]} en VRAM de la nube..."
        },
        Regex("""^(.+?) Loaded in VRAM!$""") to { m ->
            "¡${m.groupValues[1]} cargado en VRAM!"
        },
        Regex("""^Load model failed: (.+)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "Error al cargar modelo: ${m.groupValues[1]}"
        },
        Regex("""^VRAM Freed · ([\d.]+) GB Free$""") to { m ->
            "VRAM liberada · ${m.groupValues[1]} GB libres"
        },
        Regex("""^Failed to submit job: (.+)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "Error al enviar la tarea: ${m.groupValues[1]}"
        },
        // StudioViewModelServices.kt
        Regex("""^Added custom model '(.+?)' \((.+?)\)\. Connect to Colab to download weights to Google Drive\.$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "Modelo personalizado '${m.groupValues[1]}' (${m.groupValues[2]}) añadido. Conecta Colab para descargar los pesos a Google Drive."
        },
        Regex("""^Failed to start ComfyUI: (.+)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "Error al iniciar ComfyUI: ${m.groupValues[1]}"
        },
        Regex("""^Installing preset pack "(.+?)"\.\.\.$""") to { m ->
            "Instalando paquete \"${m.groupValues[1]}\"..."
        },
        Regex("""^Deleted: (.+)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "Eliminado: ${m.groupValues[1]}"
        },
        Regex("""^Failed to delete: (.+)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "No se pudo eliminar: ${m.groupValues[1]}"
        },
        Regex("""^Saved: (.+)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "Guardado: ${m.groupValues[1]}"
        },
        Regex("""^Failed to download media: (.+)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "Error al bajar archivo: ${m.groupValues[1]}"
        },
        Regex("""^Failed to save to Gallery: (.+)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "Error al guardar en galería: ${m.groupValues[1]}"
        },
        Regex("""^Share failed: (.+)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "Error al compartir: ${m.groupValues[1]}"
        },
        Regex("""^Export failed: (.+)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "Error al exportar: ${m.groupValues[1]}"
        },
        // TelemetryAndMediaViews.kt
        Regex("""^Remove "(.+?)" from EasyColab's local gallery \(copies already saved to Android Gallery are unaffected\)\.$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "Se quitará \"${m.groupValues[1]}\" de la galería local de EasyColab (las copias ya guardadas en la galería de Android no se borran)."
        },
        Regex("""^(\d+) items · 1-tap export to Android Gallery & Share$""") to { m ->
            val n = m.groupValues[1]
            "$n ${plural(n, "elemento", "elementos")} · guarda en galería o comparte en 1 toque"
        },
        // WorkspaceViews.kt
        Regex("""^Weight Shards \((\d+)/(\d+)\)$""") to { m ->
            "Fragmentos de pesos (${m.groupValues[1]}/${m.groupValues[2]})"
        },
        Regex("""^…(\d+) weight shards total$""") to { m ->
            "…${m.groupValues[1]} fragmentos en total"
        },
        Regex("""^Frames: (\d+) \(~([\d.]+)s\)$""") to { m ->
            "Fotogramas: ${m.groupValues[1]} (~${m.groupValues[2]}s)"
        },
        Regex("""^Sampling Steps: (\d+)$""") to { m ->
            "Pasos de muestreo: ${m.groupValues[1]}"
        },
        Regex("""^Denoising Strength: ([\d.]+)$""") to { m ->
            "Intensidad de redibujo: ${m.groupValues[1]}"
        },
        // LocalizationAndModels.kt dinámicos
        Regex("""^Custom ([A-Za-z0-9_+-]+) · ([\d.]+) GB$""") to { m ->
            "${m.groupValues[1]} personalizado · ${m.groupValues[2]} GB"
        },
        Regex("""^Custom HF · ([A-Za-z0-9_+-]+)$""") to { m ->
            "HF personalizado · ${m.groupValues[1]}"
        },
        Regex("""^Custom HuggingFace repo (.+)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "Repo HuggingFace personalizado ${m.groupValues[1]}"
        },
        Regex("""^Custom Pipeline \((.+?)\)$""") to { m ->
            "Pipeline no integrado (${m.groupValues[1]})"
        },
        Regex("""^Fit: T4 15G \((.+?)\)$""") to { m ->
            "Apto: T4 15G (${m.groupValues[1]})"
        },
        Regex("""^Fit: L4 24G \((.+?)\)$""") to { m ->
            "Apto: L4 24G (${m.groupValues[1]})"
        },
        Regex("""^Fit: A100 40G \((.+?)\)$""") to { m ->
            "Apto: A100 40G (${m.groupValues[1]})"
        },
        Regex("""^Needs A100 80G \((.+?)\)$""") to { m ->
            "Requiere A100 80G (${m.groupValues[1]})"
        },
        Regex("""^A100 80G \+ Offload \((.+?)\)$""") to { m ->
            "A100 80G + Offload (${m.groupValues[1]})"
        },
        Regex("""^Too Large \((.+?) · Try GGUF\)$""") to { m ->
            "Demasiado grande (${m.groupValues[1]} · prueba GGUF)"
        }
    )

    fun translateEn(en: String): String {
        if (en.isEmpty()) return en
        EN_TO_ES[en]?.let { return it }
        for ((pattern, repl) in EN_REGEX_TO_ES) {
            pattern.matchEntire(en)?.let { return repl(it) }
        }
        return en
    }

    // ─── Descripciones de fragmentos de modelo (Chino / Inglés -> Español) ───

    private val SHARD_EXACT_ES: Map<String, String> = mapOf(
        "3D 视频 VAE BF16 (9.7 GB)" to "VAE de video 3D BF16 (9.7 GB)",
        "32kHz 立体声 VAE BF16 (0.6 GB)" to "VAE de audio estéreo 32kHz BF16 (0.6 GB)",
        "Unsloth UD-Q4_K_M 主模型 (16.5 GB)" to "Pesos principales Unsloth UD-Q4_K_M (16.5 GB)",
        "多模态视觉投影器 (0.93 GB)" to "Proyector visual multimodal (0.93 GB)",
        "Unsloth MTP 多词元投机解码头 (1.31 GB)" to "Cabeza especulativa Unsloth MTP (1.31 GB)",
        "图像 VAE" to "VAE de imagen",
        "3D Video VAE BF16 (9.7 GB)" to "VAE de video 3D BF16 (9.7 GB)",
        "32kHz Stereo Audio VAE BF16 (0.6 GB)" to "VAE de audio estéreo 32kHz BF16 (0.6 GB)",
        "Unsloth UD-Q4_K_M Main Model (16.5 GB)" to "Pesos principales Unsloth UD-Q4_K_M (16.5 GB)",
        "Unsloth UD-Q4_K_M Main Weights (16.5 GB)" to "Pesos principales Unsloth UD-Q4_K_M (16.5 GB)",
        "Multimodal Vision Projector (0.93 GB)" to "Proyector visual multimodal (0.93 GB)",
        "Unsloth MTP Speculative Decoding Head (1.31 GB)" to "Cabeza especulativa Unsloth MTP (1.31 GB)",
        "Unsloth MTP Speculative Head (1.31 GB)" to "Cabeza especulativa Unsloth MTP (1.31 GB)",
        "Image VAE" to "VAE de imagen"
    )

    private val SHARD_SUB_ES: List<Pair<String, String>> = listOf(
        " [RAM内存盘]" to " [RAMDisk]",
        " [RAM Disk]" to " [RAMDisk]",
        "DiT 音视频主干 BF16" to "Troncal DiT A/V BF16",
        "DiT Audio-Video Backbone BF16" to "Troncal DiT A/V BF16",
        "DiT A/V Backbone BF16" to "Troncal DiT A/V BF16",
        "多模态编码器 BF16" to "Codificador multimodal BF16",
        "Multimodal Encoder BF16" to "Codificador multimodal BF16",
        "3D 视频 VAE BF16" to "VAE de video 3D BF16",
        "3D Video VAE BF16" to "VAE de video 3D BF16",
        "32kHz 立体声 VAE BF16" to "VAE de audio estéreo 32kHz BF16",
        "32kHz Stereo Audio VAE BF16" to "VAE de audio estéreo 32kHz BF16",
        "权重分片" to "Fragmento de pesos",
        "Weight Shard" to "Fragmento de pesos",
        "Unsloth UD-Q4_K_M 主模型" to "Pesos principales Unsloth UD-Q4_K_M",
        "Unsloth UD-Q4_K_M Main Model" to "Pesos principales Unsloth UD-Q4_K_M",
        "多模态视觉投影器" to "Proyector visual multimodal",
        "Multimodal Vision Projector" to "Proyector visual multimodal",
        "Unsloth MTP 多词元投机解码头" to "Cabeza especulativa Unsloth MTP",
        "Unsloth MTP Speculative Decoding Head" to "Cabeza especulativa Unsloth MTP",
        "图像 VAE" to "VAE de imagen",
        "Image VAE" to "VAE de imagen",
        "编码器" to "Codificador",
        "Text Encoder" to "Codificador de texto",
        "Encoder" to "Codificador"
    )

    fun localizeModelFileDesc(raw: String): String {
        if (raw.isEmpty()) return raw
        SHARD_EXACT_ES[raw]?.let { return it }
        var out = raw
        for ((src, dst) in SHARD_SUB_ES) {
            if (out.contains(src)) {
                out = out.replace(src, dst)
            }
        }
        return out
    }

    // ─── Mensajes del servidor / colab_bridge / consola (Chino -> Español) ──

    private val SERVER_EXACT_ZH_TO_ES: Map<String, String> = mapOf(
        "未加载" to "Sin cargar",
        "未连接 Colab 服务端" to "GPU en la nube sin conectar",
        "尚未连接云端 GPU" to "GPU en la nube sin conectar",
        "尚未启动云端 ComfyUI 工作台" to "ComfyUI en la nube no iniciado",
        "云端 ComfyUI 尚未启动" to "ComfyUI en la nube no iniciado",
        "Google Drive 自动软链持久化" to "Persistencia automática por enlace en Google Drive",
        "Google Drive 实时软链挂载" to "Enlace directo en vivo de Google Drive montado",
        "Google Drive 云盘自动持久化" to "Persistencia automática en la nube con Google Drive",
        "实例本地高速存储" to "Almacenamiento local rápido de la instancia",
        "欢迎使用 EasyColab Android 多模态云端工作台" to "Bienvenido a EasyColab Android Multimodal Cloud Studio",
        "纯 Kotlin 原生直连 Google Colab G4 (96GB)，支持一键免网页唤醒、生视频/生图自动存系统相册与闲置省额度保护。" to "Cliente nativo de Colab G4 (96GB): activación en 1 toque, guardado en galería y ahorro de CU.",
        "就绪：可在「云算力」页绑定账号一键唤醒 G4，或粘贴已有 gradio.live 地址连接。" to "Listo: vincula tu cuenta de Google en Nube para activar G4, o pega una URL gradio.live.",
        "尚未启动（支持一键拉起 ComfyUI + Google Drive 自动软链持久化）" to "No iniciado (ComfyUI en 1 toque + persistencia automática en Google Drive)",
        "ComfyUI 已停止（节点、模型与工作流已持久化保存至 Google Drive）" to "ComfyUI detenido (nodos, modelos y flujos guardados en Google Drive)",
        "正在初始化 ComfyUI 环境与 Google Drive 持久化目录..." to "Inicializando entorno ComfyUI y carpetas persistentes de Google Drive...",
        "正在释放现有常驻模型显存，为 ComfyUI 腾出完整 96GB 空间..." to "Liberando modelos residentes de la VRAM para dejar los 96GB libres a ComfyUI...",
        "正在从 Google Drive 恢复历史持久化的 ComfyUI 节点、模型与工作流..." to "Restaurando nodos personalizados, modelos y flujos de ComfyUI desde Google Drive...",
        "正在克隆官方最新 ComfyUI 核心引擎..." to "Clonando el motor oficial más reciente de ComfyUI...",
        "正在安装 ComfyUI 核心依赖（保留当前 G4 Blackwell CUDA PyTorch）..." to "Instalando dependencias de ComfyUI (conservando CUDA PyTorch actual)...",
        "正在恢复已持久化的自定义节点并配置 ComfyUI-Manager..." to "Restaurando nodos personalizados y configurando ComfyUI-Manager...",
        "正在检查并安装已保存自定义节点的 Python 依赖包..." to "Comprobando e instalando paquetes Python de los nodos personalizados...",
        "正在拉起 ComfyUI 节点推理引擎 (端口 8188)..." to "Iniciando motor de nodos ComfyUI (puerto 8188)...",
        "正在拉起 ComfyUI 节点推理引擎 (本地后端)..." to "Iniciando motor de nodos ComfyUI (backend local)...",
        "ComfyUI 内核已就绪，正在建立 Cloudflare 高速全屏画布隧道..." to "Núcleo de ComfyUI listo; abriendo túnel Cloudflare para el lienzo...",
        "正在先从 Google Drive 检查已持久化的历史模型权重..." to "Comprobando pesos de modelos ya guardados en Google Drive...",
        "正在将配齐的模型与中文工作流持久化同步至 Google Drive..." to "Sincronizando modelos instalados y flujos con Google Drive...",
        "正在预装并校验 llama.cpp CUDA 高速推理引擎..." to "Preinstalando y verificando el motor de inferencia CUDA llama.cpp...",
        "正在映射 MiniMax-H3 BF16 多模态编码器权重 (14 分片)..." to "Mapeando pesos del codificador multimodal MiniMax-H3 BF16 (14 fragmentos)...",
        "正在映射 MiniMax-H3 BF16 33B DiT 主干权重 (13 分片)..." to "Mapeando pesos de la troncal DiT 33B MiniMax-H3 BF16 (13 fragmentos)...",
        "正在映射 3D 视频 VAE 与 32kHz 立体声 VAE 权重..." to "Mapeando pesos de VAE de video 3D y VAE de audio estéreo 32kHz...",
        "正在构建 MiniMax-H3 BF16 原生 GPU 计算图与 Processor..." to "Construyendo grafo GPU nativo BF16 y Processor de MiniMax-H3...",
        "正在映射 Qwen-Image-2.1 权重并构建 GPU 管线..." to "Mapeando pesos de Qwen-Image-2.1 y construyendo pipeline GPU...",
        "正在映射 Z-Image-Turbo 权重并构建 8 步极速生图管线..." to "Mapeando pesos de Z-Image-Turbo y construyendo pipeline turbo de 8 pasos...",
        "正在预热 Qwen3.8-27B-UD-Q4_K_M.gguf 与 mmproj 视觉权重..." to "Precalentando Qwen3.8-27B-UD-Q4_K_M.gguf y pesos visuales mmproj...",
        "正在自动补齐 Unsloth MTP 投机解码加速头 (1.31 GB)..." to "Descargando cabeza especulativa Unsloth MTP (1.31 GB)...",
        "正在检查账号下已有的 Colab 实例..." to "Comprobando instancias Colab existentes en tu cuenta...",
        "正在检查账号下已有的 Colab 云端实例..." to "Comprobando instancias Colab activas en tu cuenta...",
        "旧实例已失效或正在销毁，正在自动清理并重新分配新实例..." to "La instancia anterior expiró; limpiando y asignando una nueva...",
        "旧实例已过期，正在自动清理并分配全新实例..." to "La instancia anterior expiró; asignando una nueva VM...",
        "容器仍在初始化，继续尝试连接内核..." to "El contenedor sigue inicializándose; reintentando conexión al kernel...",
        "正在上传最新多模型开源服务端代码 (app.py)..." to "Subiendo código del servidor multimodelo (app.py)...",
        "正在云端配置 Google Drive 持久化、多模型引擎并启动隧道 (约需 40~90 秒)..." to "Configurando persistencia en Google Drive, motores y túnel (~40-90s)...",
        "尚未授权登录 Google 账号，请先点击「绑定账号」" to "Cuenta de Google sin autorizar. Toca primero 'Vincular Google'.",
        "尚未登录 Google Colab CLI" to "Sesión no iniciada en Google Colab",
        "已彻底释放全部云端实例，计费速率归零。" to "Todas las instancias Colab liberadas. Tasa de consumo: 0 CU/h.",
        "已释放全部云端实例" to "Todas las instancias en la nube liberadas",
        "已释放全部云端实例。" to "Todas las instancias en la nube liberadas.",
        "检测到账号下残留未释放实例占用并发名额，正在自动清理后重试..." to "Se detectaron instancias residuales ocupando cuota; limpiando y reintentando...",
        "正在克隆 DiffSynth-Studio..." to "Clonando DiffSynth-Studio...",
        "已通过 Google OAuth 自动挂载 Google Drive (/content/drive/MyDrive)！" to "¡Google Drive montado automáticamente mediante Google OAuth (/content/drive/MyDrive)!",
        "已通过自定义 OAuth 自动挂载 Google Drive (/content/drive/MyDrive)！" to "¡Google Drive montado automáticamente mediante OAuth personalizado (/content/drive/MyDrive)!",
        "─── 实时下载/采样进度流 ───" to "─── Progreso de descarga/muestreo en vivo ───",
        "等待检查模型状态..." to "Esperando comprobación del estado de modelos...",
        "缺失依赖自动安装完成。" to "Dependencias faltantes instaladas correctamente.",
        "正在安装 Qwen3.8 GatedDeltaNet 原生 Triton 算子 (fla-core + flash-linear-attention)..." to "Instalando operadores Triton nativos Qwen3.8 GatedDeltaNet (fla-core + flash-linear-attention)...",
        "[MiniMax-H3-Image] 检测到当前 diffusers 版本不含 MiniMaxH3ImageModularPipeline，正在升级 diffusers>=0.43.0 ..." to "[MiniMax-H3-Image] La versión de diffusers no incluye MiniMaxH3ImageModularPipeline; actualizando diffusers>=0.43.0...",
        "[MiniMax-H3-Image] diffusers>=0.43.0 热升级校验通过！" to "[MiniMax-H3-Image] ¡Actualización a diffusers>=0.43.0 verificada!",
        "[MiniMax-H3-Image] 检测到高分辨率解码显存峰值，自动开启 VAE Tiling 并清理瞬态缓存重试..." to "[MiniMax-H3-Image] Pico de VRAM al decodificar alta resolución; activando VAE Tiling y reintentando...",
        "[GGUF 引擎] 检测到尚未缓存 MTP 投机解码权重，正在 8 路并发极速补齐..." to "[Motor GGUF] Pesos MTP sin caché; descargando en 8 hilos...",
        "[PromptCache] 命中 Qwen3-VL 32B 多模态编码缓存，0ms 瞬时跳过文本编码阶段！" to "[PromptCache] ¡Acierto en caché multimodal Qwen3-VL 32B; codificación de texto omitida en 0ms!",
        "整帧 VAE 解码显存触顶，正在清理缓存并自动切换为 Tiled 分块安全解码..." to "VRAM al límite en decodificación VAE completa; cambiando a decodificación por bloques Tiled...",
        "超长序列注意力显存触顶，正在自动释放闲置子模块并启用梯度检查点安全重试..." to "VRAM al límite en secuencia larga; liberando submódulos y reintentando con checkpointing...",
        "[ComfyUI] 服务与公网隧道已停止，GPU 显存已回收。" to "[ComfyUI] Servicio y túnel detenidos; VRAM de la GPU recuperada.",
        "[ComfyUI] 正在从 Google Drive 同步已保存的节点、模型与工作流..." to "[ComfyUI] Sincronizando nodos, modelos y flujos guardados desde Google Drive...",
        "[ComfyUI] 正在克隆官方最新 ComfyUI 仓库..." to "[ComfyUI] Clonando el repositorio oficial más reciente de ComfyUI...",
        "[ComfyUI 云盘同步] 正在通过高速通道将自定义节点、模型与工作流同步至 Google Drive..." to "[ComfyUI Sync Drive] Sincronizando nodos, modelos y flujos con Google Drive...",
        "[ComfyUI 预置包] 权重与工作流已就绪，正在自动拉起 ComfyUI 全屏画布..." to "[Paquete ComfyUI] Pesos y flujos listos; iniciando lienzo ComfyUI...",
        "[任务控制] 已收到停止指令，正在中断当前 GPU 推理并清空进度缓存..." to "[Control de tareas] Señal de parada recibida; interrumpiendo inferencia GPU y limpiando caché...",
        "已手动停止当前推理任务" to "Tarea de inferencia detenida manualmente",
        "已被新提交任务接替中断" to "Interrumpida por una nueva tarea enviada",
        "任务已提交至 Colab 队列..." to "Tarea enviada a la cola de Colab...",
        "尚未有任何模型加载至 GPU 显存！请先在左侧点击「下载权重」与「加载到显存」。" to "¡No hay ningún modelo cargado en VRAM! Toca primero '1. Descargar' y '2. Cargar VRAM'.",
        "当前指定模型未驻留显存，无需卸载。" to "El modelo indicado no está en VRAM; no hace falta quitarlo.",
        "已终止推理并从显存卸载该模型" to "Inferencia detenida y modelo descargado de la VRAM",
        "已释放 ComfyUI 驻留模型与显存缓存（画布保持在线）" to "Modelos de ComfyUI y caché VRAM liberados (el lienzo sigue activo)",
        "首尾帧模式下请至少提供首帧或尾帧图片" to "El modo fotograma inicial/final requiere al menos una imagen de inicio o fin",
        "图像编辑/重绘模式下请至少拖入一张输入图片" to "El modo de edición / redibujo requiere al menos una imagen de entrada",
        "正在同步 MiniMax-H3-Image 模块化配置与 Diffusers>=0.43 运行时..." to "Sincronizando configuración modular de MiniMax-H3-Image y entorno Diffusers>=0.43...",
        "正在自动升级 diffusers>=0.43.0 以支持 MiniMax-H3-Image 模块化管线..." to "Actualizando diffusers>=0.43.0 para soportar el pipeline modular de MiniMax-H3-Image...",
        "正在构建 MiniMax-H3-Image 本地零拷贝组装目录与共享编码器映射..." to "Construyendo carpeta local sin copia de MiniMax-H3-Image y mapa de codificador compartido...",
        "正在加载 MiniMax-H3-Image 调度器与多模态 Processor..." to "Cargando planificador y Processor multimodal de MiniMax-H3-Image...",
        "正在分层装载 32B 视觉文本编码器 (1/3)..." to "Cargando por capas el codificador visual-texto 32B (1/3)...",
        "正在分层装载 33B 图像 DiT 主干 (2/3)..." to "Cargando por capas la troncal DiT de imagen 33B (2/3)...",
        "正在装载 4K 16MP 图像 VAE 并开启分块解码保护 (3/3)..." to "Cargando VAE de imagen 4K 16MP con protección de decodificación por bloques (3/3)...",
        "正在将 32B 文本编码器装载至系统内存热备池（后续解析新提示词仅需 ~5 秒）..." to "Cargando codificador de texto 32B en caché RAM (~5s al cambiar de prompt)...",
        "正在准备潜空间与多模态编码..." to "Preparando espacio latente y codificación multimodal...",
        "正在合成 32kHz 立体声音轨与 MP4 视频..." to "Sintetizando pista estéreo 32kHz y video MP4...",
        "Qwen3.8-27B / Qwen3.8-27B-GGUF 尚未加载至 Colab GPU 显存，请先在 Mac 客户端点击「加载到显存」。" to "Qwen3.8-27B / Qwen3.8-27B-GGUF aún no está en VRAM. Toca primero '2. Cargar VRAM'.",
        "请先在客户端加载 MiniMax-H3-Image、Qwen-Image-2.1 或 Z-Image-Turbo 至显存。" to "Carga primero MiniMax-H3-Image, Qwen-Image-2.1 o Z-Image-Turbo en la VRAM.",
        "已自动切换至内置专属引擎「MiniMax-H3-Image (33B · 4K)」（仅下载 Diffusers 必需 27 个分片，并自动零拷贝共享 MiniMax-H3 的 66.7GB 编码器权重）！" to "¡Cambiado al motor integrado 'MiniMax-H3-Image (33B · 4K)' (solo baja los 27 fragmentos de Diffusers y comparte sin copia los 66.7GB del codificador de MiniMax-H3)!"
    )

    private val SERVER_REGEX_ZH_TO_ES: List<Pair<Regex, (MatchResult) -> String>> = listOf(
        // Puente / Wake & Stop
        Regex("""^尚未授权登录 Google 账号，请先点击「\s*绑定账号」$""") to {
            "Cuenta de Google sin autorizar. Toca primero 'Vincular Google'."
        },
        Regex("""^已彻底释放全部云端实例(?:\s*\((\d+)\s*台\))?！当前计费速率:\s*([\d.]+)\s*CU/(?:小时|h)$""") to { m ->
            val cnt = m.groupValues[1]
            val rate = m.groupValues[2]
            if (cnt.isNotEmpty()) {
                "¡Todas las instancias en la nube liberadas ($cnt)! Tasa de consumo actual: $rate CU/h"
            } else {
                "¡Todas las instancias en la nube liberadas! Tasa de consumo actual: $rate CU/h"
            }
        },
        Regex("""^Google Colab 当前区域 (.+?) 算力池繁忙 \((.+?)\)，(\d+) 秒后进行第 (\d+)/(\d+) 次申请\.\.\.$""") to { m ->
            "Pool de ${m.groupValues[1]} ocupado en esta región de Google Colab (${m.groupValues[2]}); reintento ${m.groupValues[4]}/${m.groupValues[5]} en ${m.groupValues[3]}s..."
        },
        Regex("""^Google Colab 云端当前时段 (.+?) 算力池库存不足 \((.+?)\)，连续 (\d+) 次申请均未分到机器（属于 Colab 官方高配机型时段性缺货，非本地客户端故障）。建议稍等几分钟再试，或在左侧临时切换为 A100 / L4 实例。$""") to { m ->
            "Sin stock disponible para ${m.groupValues[1]} en Google Colab ahora (${m.groupValues[2]}) tras ${m.groupValues[3]} intentos (falta temporal de capacidad en Colab, no es un fallo de la app). Espera unos minutos o prueba con A100 / L4."
        },
        Regex("""^Google Colab 拒绝分配 (.+?) \(HTTP 412\)：当前账号并发实例数已达上限，或该时段高配机型触发临时配额限制。请确认未在其他浏览器标签页占用实例，稍后重试或临时切换为 A100 / L4。$""") to { m ->
            "Google Colab rechazó asignar ${m.groupValues[1]} (HTTP 412): límite de instancias concurrentes o cuota temporal alcanzada. Verifica que no tengas otra instancia abierta en el navegador, reintenta luego o prueba A100 / L4."
        },
        Regex("""^Google Colab 后端拒绝分配 (.+?) \(HTTP 400\)：当前账号订阅等级可能暂不支持该机型或可用计算单元不足，建议切换为 A100 / L4 / T4 实例。$""") to { m ->
            "Google Colab rechazó asignar ${m.groupValues[1]} (HTTP 400): es posible que tu suscripción no admita esta GPU o falten CU. Prueba con A100 / L4 / T4."
        },
        Regex("""^检测到云端(?:已在后台|已)完成 (.+?) 实例分配，直接接管！$""") to { m ->
            "¡Instancia ${m.groupValues[1]} asignada en segundo plano detectada en la nube; tomando control!"
        },
        Regex("""^正在向 Google Colab 申请分配 (.+?) 实例\.\.\.$""") to { m ->
            "Solicitando instancia ${m.groupValues[1]} a Google Colab..."
        },
        Regex("""^成功分配 (.+?) 云端虚拟机！正在等待容器内核就绪\.\.\.$""") to { m ->
            "¡VM en la nube ${m.groupValues[1]} asignada! Esperando a que el kernel arranque..."
        },
        Regex("""^正在检查已有实例 [\[（(](.+?)[\]）)] \((.+?)\) 连通性\.\.\.$""") to { m ->
            "Comprobando conectividad de la instancia existente [${m.groupValues[1]}] (${m.groupValues[2]})..."
        },
        Regex("""^正在检查已有实例 \((.+?)\) 连通性\.\.\.$""") to { m ->
            "Comprobando conectividad de la instancia existente (${m.groupValues[1]})..."
        },
        Regex("""^当前实例型号为 \[(.+?)\]，正在释放并切换为 \[(.+?)\]\.\.\.$""") to { m ->
            "Liberando [${m.groupValues[1]}] y cambiando a [${m.groupValues[2]}]..."
        },
        Regex("""^旧实例 \((.+?)\) 已失效或正在销毁，准备清理\.\.\.$""") to { m ->
            "La instancia anterior (${m.groupValues[1]}) expiró o se está cerrando; preparando limpieza..."
        },
        Regex("""^当前已占用实例 \[(.+?)\]，正在彻底释放并等待配额就绪以切换为 \[(.+?)\]\.\.\.$""") to { m ->
            val inst = if (m.groupValues[1] == "旧实例") "instancia anterior" else m.groupValues[1]
            "Instancia actual [$inst] en uso; liberando y esperando cuota para cambiar a [${m.groupValues[2]}]..."
        },
        Regex("""^当前已分配实例型号为 \[(.+?)\]，正在释放并切换为您选择的 \[(.+?)\]\.\.\.$""") to { m ->
            "Instancia asignada actual [${m.groupValues[1]}]; liberando y cambiando a [${m.groupValues[2]}]..."
        },
        Regex("""^启动超时，日志尾部:\s*(.*)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "Tiempo de arranque agotado. Últimos registros: ${m.groupValues[1]}"
        },
        // Reglas de app.py: descargas, RAMDisk, GGUF, VRAM, ComfyUI, inferencia
        Regex("""^已无缝接管在线 ComfyUI 画布（(.+?)）$""") to { m ->
            "Reconectado al lienzo activo de ComfyUI (${localizeServerText(m.groupValues[1])})"
        },
        Regex("""^ComfyUI 进程已退出 \(code=([^)]+)\)，可点击重新启动$""") to { m ->
            "El proceso de ComfyUI terminó (code=${m.groupValues[1]}). Toca para reiniciar."
        },
        Regex("""^正在建立 (.+?) 目录软链 \(models / workflows / output\)\.\.\.$""") to { m ->
            "Enlazando directorios de ${localizeServerText(m.groupValues[1])} (models / workflows / output)..."
        },
        Regex("""^正在 8 线程极速下载 (.+?) 至 (.+?)\.\.\.$""") to { m ->
            "Descargando en 8 hilos ${m.groupValues[1]} a ${m.groupValues[2]}..."
        },
        Regex("""^正在下载 (.+?) 至 (.+?)\.\.\.$""") to { m ->
            "Descargando ${m.groupValues[1]} a ${m.groupValues[2]}..."
        },
        Regex("""^正在准备配齐「(.+?)」（共 (\d+) 个官方权重）\.\.\.$""") to { m ->
            """Preparando paquete "${translatePackTitle(m.groupValues[1])}" (${m.groupValues[2]} pesos oficiales)..."""
        },
        Regex("""^正在生成「(.+?)」全中文三步傻瓜注释工作流\.\.\.$""") to { m ->
            """Generando plantillas guiadas para "${translatePackTitle(m.groupValues[1])}"..."""
        },
        Regex("""^正在为 (.+?) 启动 8 路并发 HTTP Range 极速下载通道\.\.\.$""") to { m ->
            "Iniciando descarga HTTP Range en 8 hilos para ${m.groupValues[1]}..."
        },
        Regex("""^\[(\d+/\d+)\] (.+?) 已就绪 \((.+?)\)，跳过下载$""") to { m ->
            "[${m.groupValues[1]}] ${m.groupValues[2]} listo (${m.groupValues[3]}), omitido"
        },
        Regex("""^\[(\d+/\d+)\] 正在 8 线程并发下载 (.+?) \((.+?)\)\.\.\.$""") to { m ->
            "[${m.groupValues[1]}] Descargando en 8 hilos ${m.groupValues[2]} (${localizeModelFileDesc(m.groupValues[3])})..."
        },
        Regex("""^正在获取 (.+?) 的分词器与 Processor 配置文件\.\.\.$""") to { m ->
            "Obteniendo tokenizador y configuración de Processor para ${m.groupValues[1]}..."
        },
        Regex("""^正在评估显存余量并装载 (.+?) 至 GPU\.\.\.$""") to { m ->
            "Evaluando VRAM libre y cargando ${m.groupValues[1]} en GPU..."
        },
        Regex("""^\[显存常驻加速\] 正在将子模块 (.+?) 预热锁入 GPU 显存\.\.\.$""") to { m ->
            "[Caché VRAM] Precalentando y fijando submódulo ${m.groupValues[1]} en VRAM..."
        },
        Regex("""^\[RAMDisk 内存盘加速已开启\] /dev/shm 可用空间 ([\d.]+) GB \(2\.4GB/s 零延迟读写\)$""") to { m ->
            "[RAMDisk activado] /dev/shm libre: ${m.groupValues[1]} GB (lectura/escritura rápida 2.4GB/s)"
        },
        Regex("""^正在自动安装缺失的运行期依赖:\s*(.+?)\s*\.\.\.$""") to { m ->
            "Instalando dependencias faltantes en tiempo de ejecución: ${m.groupValues[1]}..."
        },
        Regex("""^检测到 torchaudio 动态库异常 \((.+?)\)，正在自动对齐 PyTorch \((.+?)\) ABI\.\.\.$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "Detectada incompatibilidad en torchaudio (${m.groupValues[1]}); alineando ABI con PyTorch (${m.groupValues[2]})..."
        },
        Regex("""^torchaudio 已自动修复对齐至 (.+?)！$""") to { m ->
            "¡torchaudio reparado y alineado a ${m.groupValues[1]}!"
        },
        Regex("""^\[加速引擎\] Triton causal_conv1d 注册跳过:\s*(.+)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "[Motor acelerado] Registro Triton causal_conv1d omitido: ${m.groupValues[1]}"
        },
        Regex("""^\[加速引擎\] accelerate hook 拆除跳过:\s*(.+)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "[Motor acelerado] Retirada de hook accelerate omitida: ${m.groupValues[1]}"
        },
        Regex("""^\[加速引擎\] 算子融合未完成 \((.+)\)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "[Motor acelerado] Fusión de operadores no completada (${m.groupValues[1]})"
        },
        Regex("""^\[加速引擎\] 全 64 层融合算子 \+ CUDAGraph 静态图引擎已就绪 \(CUDAGraph 静态加速 (\d+) tokens / 动态最大上下文 (\d+) tokens\)！$""") to { m ->
            "[Motor acelerado] 64 capas fusionadas + CUDAGraph listos (estático ${m.groupValues[1]} tokens / contexto máx. ${m.groupValues[2]} tokens)"
        },
        Regex("""^\[加速引擎\] CUDAGraph 未捕获，融合算子仍保留 \((.+)\)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "[Motor acelerado] CUDAGraph no capturado; se conservan operadores fusionados (${m.groupValues[1]})"
        },
        Regex("""^\[自定义模型\] 读取 (.+?) 跳过:\s*(.+)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "[Modelo personalizado] Lectura de ${m.groupValues[1]} omitida: ${m.groupValues[2]}"
        },
        Regex("""^\[自定义模型\] 写入 (.+?) 跳过:\s*(.+)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "[Modelo personalizado] Escritura de ${m.groupValues[1]} omitida: ${m.groupValues[2]}"
        },
        Regex("""^\[自定义模型\] (.+)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "[Modelo personalizado] ${localizeServerText(m.groupValues[1])}"
        },
        Regex("""^\[显存管理\] (.+)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "[Gestión VRAM] ${localizeServerText(m.groupValues[1])}"
        },
        Regex("""^\[ComfyUI 云盘持久化\] (.+)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "[ComfyUI Drive] ${localizeServerText(m.groupValues[1])}"
        },
        Regex("""^\[Google Drive 同步完成\] (.+?) -> (.+)$""") to { m ->
            "[Sync Google Drive completado] ${m.groupValues[1]} -> ${m.groupValues[2]}"
        },
        Regex("""^\[Google Drive 同步失败\] (.+?):\s*(.+)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "[Error al sincronizar Google Drive] ${m.groupValues[1]}: ${m.groupValues[2]}"
        },
        Regex("""^\[Google Drive 同步异常\] (.+?):\s*(.+)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "[Excepción al sincronizar Google Drive] ${m.groupValues[1]}: ${m.groupValues[2]}"
        },
        Regex("""^\[后台云盘同步完成\] (.+?) 已持久化保存至 Google Drive$""") to { m ->
            "[Sync en segundo plano listo] ${m.groupValues[1]} guardado en Google Drive"
        },
        Regex("""^\[后台云盘同步跳过\] (.+?):\s*(.+)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "[Sync en segundo plano omitido] ${m.groupValues[1]}: ${m.groupValues[2]}"
        },
        Regex("""^多线程分片直连回退至标准 HF 下载 \((.+)\)\.\.\.$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "Descarga directa multihilo recurriendo a descarga estándar de HF (${m.groupValues[1]})..."
        },
        Regex("""^\[自动省额度看门狗\] 已连续闲置 (\d+) 分钟，正在自动释放 Colab 虚拟机\.\.\.$""") to { m ->
            "[Vigilancia CU] ${m.groupValues[1]} min sin actividad; liberando instancia Colab automáticamente..."
        },
        Regex("""^Google Drive 剩余空间 \(([\d.]+) GB\) 小于 (.+?) 待下载增量 \(([\d.]+) GB\)，自动改用实例本地高速 NVMe 磁盘 \((.+?)\) 存储！$""") to { m ->
            "Espacio libre en Google Drive (${m.groupValues[1]} GB) menor que la descarga pendiente de ${m.groupValues[2]} (${m.groupValues[3]} GB); usando disco NVMe local (${m.groupValues[4]})."
        },
        Regex("""^\[MiniMax-H3-Image\] 已启用官方 ComponentsManager 自动显存/内存热备轮换 \(VRAM ([\d.]+)GB / 可用 RAM ([\d.]+)GB\)$""") to { m ->
            "[MiniMax-H3-Image] Rotación automática VRAM/RAM con ComponentsManager activada (VRAM ${m.groupValues[1]}GB / RAM libre ${m.groupValues[2]}GB)"
        },
        Regex("""^正在将 (.+?) \(([\d.]+) GB\) 高速预热至 /dev/shm 内存盘\.\.\.$""") to { m ->
            "Precargando ${m.groupValues[1]} (${m.groupValues[2]} GB) en RAMDisk /dev/shm..."
        },
        Regex("""^(.+?) 内存盘预热完成 \((\d+) MB/s\)$""") to { m ->
            "${m.groupValues[1]} precargado en RAMDisk (${m.groupValues[2]} MB/s)"
        },
        Regex("""^内存盘预热跳过 \((.+)\)，直接读取原路径$""") to { m ->
            "Precarga en RAMDisk omitida (${m.groupValues[1]}); leyendo desde ruta original"
        },
        Regex("""^\[NVMe 高速缓存\] 正在将 (.+?) \((\d+) 个分片 / ([\d.]+) GB\) 从云盘顺序预热至本地 NVMe SSD\.\.\.$""") to { m ->
            "[Caché NVMe] Copiando ${m.groupValues[1]} (${m.groupValues[2]} fragmentos / ${m.groupValues[3]} GB) desde Drive al SSD NVMe local..."
        },
        Regex("""^\[NVMe 高速缓存\] (.+?) 本地 SSD 预热完成 \((\d+) MB/s\)$""") to { m ->
            "[Caché NVMe] Precarga en SSD local de ${m.groupValues[1]} completada (${m.groupValues[2]} MB/s)"
        },
        Regex("""^本地 NVMe 预热跳过 \((.+)\)，继续读取原路径$""") to { m ->
            "Precarga en NVMe local omitida (${m.groupValues[1]}); leyendo desde ruta original"
        },
        Regex("""^\[GGUF 引擎\] GitHub Releases 查询跳过，使用稳定镜像版本 ([^\s]+) \((.+)\)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "[Motor GGUF] Consulta a GitHub Releases omitida; usando versión estable ${m.groupValues[1]} (${m.groupValues[2]})"
        },
        Regex("""^\[GGUF 引擎\] 正在下载官方预编译 llama\.cpp CUDA 12 推理后端:\s*(.+?)\s*\.\.\.$""") to { m ->
            "[Motor GGUF] Descargando binario CUDA 12 de llama.cpp: ${m.groupValues[1]}..."
        },
        Regex("""^\[GGUF 引擎\] 正在下载配套 CUDA 12 Runtime 动态库 \((.+?)\)\.\.\.$""") to { m ->
            "[Motor GGUF] Descargando librerías CUDA 12 Runtime (${m.groupValues[1]})..."
        },
        Regex("""^\[GGUF 引擎\] llama-server CUDA 引擎校验通过 \((.+)\)$""") to { m ->
            "[Motor GGUF] Motor CUDA llama-server verificado (${m.groupValues[1]})"
        },
        Regex("""^\[GGUF 引擎\] 正在启动 (.+?) 服务 \(上下文 (\d+K)=(\d+), KV=([^,]+), GPU采样, ([^,]+), port=(\d+)\)\.\.\.$""") to { m ->
            val modelName = m.groupValues[1].replace(" + MTP 多词元投机解码", " + decodificación MTP")
            "[Motor GGUF] Iniciando $modelName (contexto ${m.groupValues[2]}=${m.groupValues[3]}, KV=${m.groupValues[4]}, muestreo GPU, ${translateGgufFit(m.groupValues[5])}, puerto=${m.groupValues[6]})..."
        },
        Regex("""^正在将 (.+?) 装载至 GPU \((\d+K) 上下文 · KV ([^·]+?) · (.+?)\)\.\.\.$""") to { m ->
            val modelName = m.groupValues[1].replace(" + MTP 多词元投机解码", " + decodificación MTP")
            "Cargando $modelName en GPU (contexto ${m.groupValues[2]} · KV ${m.groupValues[3].trim()} · ${translateGgufFit(m.groupValues[4])})..."
        },
        Regex("""^\[GGUF 引擎\] (.+?) 已就绪 \((.+)\)$""") to { m ->
            "[Motor GGUF] ${m.groupValues[1]} listo (${translateModeLabel(m.groupValues[2])})"
        },
        Regex("""^\[GGUF 引擎\] 当前配置 \((.+?)\) 显存触顶，自动降级重试\.\.\.$""") to { m ->
            "[Motor GGUF] VRAM al límite con (${m.groupValues[1]}); reintentando con perfil reducido..."
        },
        Regex("""^\[GGUF 引擎\] MTP 投机权重获取跳过，将以标准模式启动:\s*(.+)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "[Motor GGUF] Descarga de pesos MTP omitida; iniciando en modo estándar: ${m.groupValues[1]}"
        },
        Regex("""^\[G4 大内存热备\] 检测到充裕系统内存 \(([\d.]+)/([\d.]+) GB\)，已启用 32B 文本编码器 \+ 33B DiT 双主干 DDR5 内存常驻热备（阶段切换仅需 ~5 秒）！$""") to { m ->
            "[Caché RAM G4] Memoria amplia (${m.groupValues[1]}/${m.groupValues[2]} GB); activada caché DDR5 para codificador 32B + DiT 33B (cambio en ~5s)."
        },
        Regex("""^正在将 MiniMax-H3 预装载至 (\d+)GB 高速系统内存热备池（首次载入后换提示词仅需 ~5 秒）\.\.\.$""") to { m ->
            "Precargando MiniMax-H3 en caché RAM de ${m.groupValues[1]}GB (tras la carga inicial, cambiar de prompt tarda ~5s)..."
        },
        Regex("""^\[混合内存热备\] 系统可用内存 ([\d.]+)/([\d.]+) GB，已将 32B 文本编码器锁入系统内存热备（换提示词 ~5 秒极速换入），DiT 走本地高速存储！$""") to { m ->
            "[Caché RAM híbrida] RAM disponible ${m.groupValues[1]}/${m.groupValues[2]} GB; codificador 32B fijado en RAM (~5s al cambiar prompt) y DiT en disco rápido."
        },
        Regex("""^检测到分词器或 transformers 组件缺失 \((.+)\)，正在自动升级 transformers 及分词器依赖\.\.\.$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "Falta tokenizador o componente de transformers (${m.groupValues[1]}); actualizando dependencias..."
        },
        Regex("""^\[PromptEmbedder\] 多模态提示词解析完成，总耗时 ([\d.]+)s（已写入缓存，同提示词换种子后续 0ms）$""") to { m ->
            "[PromptEmbedder] Codificación multimodal completada en ${m.groupValues[1]}s (guardada en caché; 0ms al cambiar de Seed)"
        },
        Regex("""^\[PromptEmbedder\] 多模态提示词解析完成，总耗时 ([\d.]+)s$""") to { m ->
            "[PromptEmbedder] Codificación multimodal completada en ${m.groupValues[1]}s"
        },
        Regex("""^Prompt 缓存挂载跳过:\s*(.+)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "Montaje de caché de prompts omitido: ${m.groupValues[1]}"
        },
        Regex("""^\[极速显存换入\] 子模块 (.+?) 已整块载入 GPU 显存，耗时 ([\d.]+)s$""") to { m ->
            "[Carga rápida VRAM] Submódulo ${m.groupValues[1]} cargado en GPU en ${m.groupValues[2]}s"
        },
        Regex("""^\[大显存常驻已激活\] 管线子模块已预热至显存 \(当前总驻留 ([\d.]+) GB / ([\d.]+) GB\)$""") to { m ->
            "[Residencia VRAM activa] Submódulos precargados en VRAM (${m.groupValues[1]} GB / ${m.groupValues[2]} GB en uso)"
        },
        // Catálogo, descargas, carga y descarga de VRAM
        Regex("""^无法获取仓库 (.+?) 详情，请检查名称或填写 HF Token$""") to { m ->
            "No se pudieron obtener detalles de ${m.groupValues[1]}; revisa el nombre o tu HF Token"
        },
        Regex("""^已成功导入自定义模型「(.+?)」\((.+?) · 共 (\d+) 个文件 / 约 ([\d.]+) GB\)，可立即下载权重并加载到显存！$""") to { m ->
            "Modelo personalizado '${m.groupValues[1]}' importado (${m.groupValues[2]} · ${m.groupValues[3]} archivos / ~${m.groupValues[4]} GB). ¡Ya puedes bajar los pesos y cargarlo en VRAM!"
        },
        Regex("""^已从模型中心移除自定义模型「(.+?)」$""") to { m ->
            "Modelo personalizado '${m.groupValues[1]}' eliminado del catálogo"
        },
        Regex("""^(.+?) 全部 (\d+)/(\d+) 个权重文件已就绪（共 ([\d.]+) GB），现在可点击「加载到显存」！$""") to { m ->
            "¡Todos los pesos de ${m.groupValues[1]} listos (${m.groupValues[2]}/${m.groupValues[3]} · ${m.groupValues[4]} GB)! Toca '2. Cargar VRAM'."
        },
        Regex("""^下载 (.+?) 权重出错:\s*(.+)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "Error al descargar pesos de ${m.groupValues[1]}: ${m.groupValues[2]}"
        },
        Regex("""^正在通过 ComponentsManager 装载 MiniMax-H3-Image 至 (\d+)GB 内存热备池与 GPU\.\.\.$""") to { m ->
            "Cargando MiniMax-H3-Image con ComponentsManager en caché RAM de ${m.groupValues[1]}GB y GPU..."
        },
        Regex("""^正在将 (.+?) 高速缓存至本地 SSD \((\d+)/(\d+)\)，消除后续换入延迟\.\.\.$""") to { m ->
            "Cacheando ${m.groupValues[1]} en SSD local (${m.groupValues[2]}/${m.groupValues[3]}) para evitar esperas..."
        },
        Regex("""^正在使用 Diffusers 装载自定义图像模型 (.+?)\.\.\.$""") to { m ->
            "Cargando modelo de imagen personalizado ${m.groupValues[1]} con Diffusers..."
        },
        Regex("""^正在装载 (.+?) Transformers 原生权重 \(上下文上限 (\d+K)\)\.\.\.$""") to { m ->
            "Cargando pesos nativos Transformers de ${m.groupValues[1]} (contexto máx. ${m.groupValues[2]})..."
        },
        Regex("""^正在预热 (.+?) GGUF 权重并启动 llama\.cpp CUDA 引擎\.\.\.$""") to { m ->
            "Precalentando pesos GGUF de ${m.groupValues[1]} e iniciando motor CUDA llama.cpp..."
        },
        Regex("""^加载 (.+?) 至显存失败:\s*(.+)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "Error al cargar ${m.groupValues[1]} en VRAM: ${m.groupValues[2]}"
        },
        Regex("""^已从显存卸载 (.+?)，当前可用显存 ([\d.]+) GB （(.+?)）$""") to { m ->
            val rem = Regex("""显存中仍保留 (\d+) 个常驻模型""").replace(m.groupValues[3]) { rm ->
                val c = rm.groupValues[1]
                if (c == "1") "queda 1 modelo en VRAM" else "quedan $c modelos en VRAM"
            }.replace("显存已完全清空", "VRAM completamente libre")
            "${m.groupValues[1]} descargado de la VRAM; VRAM libre: ${m.groupValues[2]} GB ($rem)"
        },
        Regex("""^(.+?) 已装载至显存 \(([^，]+)，约 ([\d.]+)GB，耗时 ([\d.]+)s\)(?: \| 当前共 (\d+) 个模型同时常驻显存，切换 0 等待)?！(（因显存上限已自动腾退 [^）]+）)?(.*)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            val coresident = if (m.groupValues[5].isNotEmpty()) {
                " | ${m.groupValues[5]} modelos residentes a la vez (cambio instantáneo)"
            } else ""
            val evicted = if (m.groupValues[6].isNotEmpty()) {
                Regex("""（因显存上限已自动腾退 ([^）]+)）""").replace(m.groupValues[6]) { em ->
                    " (se liberó ${em.groupValues[1]} por límite de VRAM)"
                }
            } else ""
            "¡${m.groupValues[1]} cargado en VRAM (${translateModeLabel(m.groupValues[2])}, ~${m.groupValues[3]}GB, ${m.groupValues[4]}s)$coresident$evicted${m.groupValues[7]}"
        },
        // ComfyUI logs y estado
        Regex("""^\[ComfyUI\] 生成默认占位参考图提示:\s*(.+)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "[ComfyUI] Aviso al generar imagen de referencia inicial: ${m.groupValues[1]}"
        },
        Regex("""^\[ComfyUI\] 写入 EasyColab 默认工作流引导扩展提示:\s*(.+)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "[ComfyUI] Aviso al escribir extensión guía de flujos: ${m.groupValues[1]}"
        },
        Regex("""^\[ComfyUI 工作流生成\] (.+?) 模板处理异常:\s*(.+)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "[Generador ComfyUI] Excepción en plantilla ${m.groupValues[1]}: ${m.groupValues[2]}"
        },
        Regex("""^\[ComfyUI\] 已自动接管实例上正在运行的 ComfyUI 服务:\s*(.+)$""") to { m ->
            "[ComfyUI] Conectado al servicio ComfyUI ya activo en la instancia: ${m.groupValues[1]}"
        },
        Regex("""^\[ComfyUI\] 正在为已持久化的自定义节点自动恢复 (\d+) 项 Python 依赖\.\.\.$""") to { m ->
            "[ComfyUI] Restaurando ${m.groupValues[1]} dependencias Python de nodos personalizados..."
        },
        Regex("""^\[ComfyUI\] 正在预装核心插件 (.+?)\.\.\.$""") to { m ->
            "[ComfyUI] Preinstalando extensión clave ${m.groupValues[1]}..."
        },
        Regex("""^\[ComfyUI\] 画布公网隧道已开通:\s*(.+)$""") to { m ->
            "[ComfyUI] Túnel público del lienzo abierto: ${m.groupValues[1]}"
        },
        Regex("""^\[ComfyUI 极速下载\] (.+?) -> (.+?) -> (.+)$""") to { m ->
            "[ComfyUI descarga rápida] ${m.groupValues[1]} -> ${m.groupValues[2]} -> ${m.groupValues[3]}"
        },
        Regex("""^\[ComfyUI 直链下载\] (.+?) -> (.+)$""") to { m ->
            "[ComfyUI descarga directa] ${m.groupValues[1]} -> ${m.groupValues[2]}"
        },
        Regex("""^\[ComfyUI 预置包\] \((\d+/\d+)\) 已存在跳过:\s*(.+)$""") to { m ->
            "[Paquete ComfyUI] (${m.groupValues[1]}) Ya existe, omitido: ${m.groupValues[2]}"
        },
        Regex("""^\[ComfyUI 预置包\] \((\d+/\d+)\) 开始 8 线程下载 (.+?) -> (.+)$""") to { m ->
            "[Paquete ComfyUI] (${m.groupValues[1]}) Iniciando descarga en 8 hilos ${m.groupValues[2]} -> ${m.groupValues[3]}"
        },
        Regex("""^\[ComfyUI 预置包\] (.+)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "[Paquete ComfyUI] ${localizeServerText(m.groupValues[1])}"
        },
        Regex("""^已持久化至 (.+?)（节点 (\d+) 个 · 权重 (\d+) 个 · 工作流 (\d+) 个）$""") to { m ->
            "Guardado en ${localizeServerText(m.groupValues[1])} (${m.groupValues[2]} nodos · ${m.groupValues[3]} pesos · ${m.groupValues[4]} flujos)"
        },
        Regex("""^ComfyUI 已就绪（(.+?) · 节点 (\d+) 个 · 权重 (\d+) 个）$""") to { m ->
            "ComfyUI listo (${localizeServerText(m.groupValues[1])} · ${m.groupValues[2]} nodos · ${m.groupValues[3]} pesos)"
        },
        Regex("""^ComfyUI 启动出错:\s*(.+)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "Error al iniciar ComfyUI: ${m.groupValues[1]}"
        },
        Regex("""^权重 (.+?) \(([\d.]+) GB\) 已下载至 models/(.+?) 并持久化到 (.+?)（在画布按 R 键即可刷新选用）$""") to { m ->
            "Peso ${m.groupValues[1]} (${m.groupValues[2]} GB) descargado en models/${m.groupValues[3]} y guardado en ${localizeServerText(m.groupValues[4])} (actualiza en el lienzo para usarlo)"
        },
        Regex("""^\[(\d+/\d+)\] 正在 8 线程极速下载 (.+?) \(约 ([\d.]+) GB\)\.\.\.$""") to { m ->
            "[${m.groupValues[1]}] Descargando en 8 hilos ${m.groupValues[2]} (~${m.groupValues[3]} GB)..."
        },
        Regex("""^「(.+?)」已全部配齐！打开画布左侧「工作流」点击 (.+?) 即可直接传图运行$""") to { m ->
            "¡'${translatePackTitle(m.groupValues[1])}' listo! Abre 'Workflows' en el lienzo y elige ${m.groupValues[2]} para ejecutarlo."
        },
        Regex("""^「(.+?)」已配齐且画布已启动！在左侧「工作流」打开中文模板即可直接出片$""") to { m ->
            "¡'${translatePackTitle(m.groupValues[1])}' instalado y lienzo iniciado! Abre una plantilla en 'Workflows' para empezar."
        },
        // Inferencia y generación
        Regex("""^(.+?): 子阶段已完成，正在继续后续合成封装\.\.\.$""") to { m ->
            "${translateStageLabel(m.groupValues[1])}: subetapa completada; empaquetando resultado..."
        },
        Regex("""^(\[[^\]]+\]\s*)?(.+?) 正在编码多模态上下文并启动推理\.\.\.$""") to { m ->
            "${m.groupValues[1]}${m.groupValues[2]} codificando contexto multimodal e iniciando inferencia..."
        },
        Regex("""^(.+?) 正在深度思考 \((.+)\)\.\.\.$""") to { m ->
            "${m.groupValues[1]} pensando en profundidad (${m.groupValues[2]})..."
        },
        Regex("""^(.+?) 正在流式输出回复 \((.+)\)\.\.\.$""") to { m ->
            "${m.groupValues[1]} transmitiendo respuesta (${m.groupValues[2]})..."
        },
        Regex("""^(.+?) 推理完成！耗时 ([\d.]+s)(.*)$""") to { m ->
            "¡Inferencia de ${m.groupValues[1]} completada! Duración ${m.groupValues[2]}" +
                m.groupValues[3].replace(" · 共 ", " · ")
        },
        Regex("""^\[(.+?)\] 推理完成 \| (\d+) tokens \| ([\d.]+) tok/s \| 耗时 ([\d.]+s)$""") to { m ->
            "[${m.groupValues[1]}] Inferencia completada | ${m.groupValues[2]} tokens | ${m.groupValues[3]} tok/s | Duración ${m.groupValues[4]}"
        },
        Regex("""^(\[[^\]]+\]\s*)?(.+?) 正在使用多模态编码器解析提示词 \((\d+)%\)\.\.\.$""") to { m ->
            "${m.groupValues[1]}${m.groupValues[2]} codificando prompt con el codificador multimodal (${m.groupValues[3]}%)..."
        },
        Regex("""^(\[[^\]]+\]\s*)?DiT 采样已完成，正在执行(.+?) \((\d+)%\)\.\.\.$""") to { m ->
            "${m.groupValues[1]}Muestreo DiT completado; ejecutando ${translateStageLabel(m.groupValues[2])} (${m.groupValues[3]}%)..."
        },
        Regex("""^(\[[^\]]+\]\s*)?视频帧解码完成，正在执行 32kHz 立体声音轨解码 \((\d+)%\)\.\.\.$""") to { m ->
            "${m.groupValues[1]}Fotogramas decodificados; decodificando pista de audio estéreo 32kHz (${m.groupValues[2]}%)..."
        },
        Regex("""^(\[[^\]]+\]\s*)?(.+?) 正在执行去噪采样第 (\d+)/(\d+) 步 \((\d+)%\)\.\.\.$""") to { m ->
            "${m.groupValues[1]}${m.groupValues[2]} ejecutando paso de muestreo ${m.groupValues[3]}/${m.groupValues[4]} (${m.groupValues[5]}%)..."
        },
        Regex("""^(\[[^\]]+\]\s*)?(.+?) 正在采样 (\d+)/(\d+) 步 \(总进度 (\d+)% · ([\d.]+s)/步 · 采样剩余约 (\d+s)\)\.\.\.$""") to { m ->
            "${m.groupValues[1]}${m.groupValues[2]} muestreando paso ${m.groupValues[3]}/${m.groupValues[4]} (total ${m.groupValues[5]}% · ${m.groupValues[6]}/paso · ~${m.groupValues[7]} restantes)..."
        },
        Regex("""^(\[[^\]]+\]\s*)?DiT 采样已完成 \((\d+/\d+)\)，正在进入(.+?) \((\d+)%\)\.\.\.$""") to { m ->
            "${m.groupValues[1]}Muestreo DiT completado (${m.groupValues[2]}); iniciando ${translateStageLabel(m.groupValues[3])} (${m.groupValues[4]}%)..."
        },
        Regex("""^\[(.+?)\] DiT 采样 (\d+/\d+) 步完成 \(([\d.]+s)\)，开始执行(.+?)\.\.\.$""") to { m ->
            "[${m.groupValues[1]}] Muestreo DiT ${m.groupValues[2]} pasos listo (${m.groupValues[3]}); iniciando ${translateStageLabel(m.groupValues[4])}..."
        },
        Regex("""^(.+?) 尚未加载到 GPU 显存！请先在左侧点击「加载到显存」（显存充裕时可与现有模型同时常驻）。$""") to { m ->
            "¡${m.groupValues[1]} aún no está en VRAM! Toca '2. Cargar VRAM' (si hay VRAM libre, convive con los modelos activos)."
        },
        Regex("""^(.+?) 尚未加载至 GPU 显存！请先在左侧点击「加载到显存」。$""") to { m ->
            "¡${m.groupValues[1]} aún no está en VRAM! Toca primero '2. Cargar VRAM'."
        },
        Regex("""^(.+?) 尚未加载到显存（当前已常驻：(.+?)）。请点击左侧「加载到显存」，显存充裕时可同时常驻无需卸载现有模型。$""") to { m ->
            "${m.groupValues[1]} no está en VRAM (activos: ${m.groupValues[2]}). Toca '2. Cargar VRAM'; si hay espacio, conviven sin quitarlos."
        },
        Regex("""^正在准备 (.+?) 推理管线(?: \(共 (\d+) 项\))?\.\.\.$""") to { m ->
            val cnt = if (m.groupValues[2].isNotEmpty()) " (${m.groupValues[2]} elementos)" else ""
            "Preparando pipeline de inferencia de ${m.groupValues[1]}$cnt..."
        },
        Regex("""^(\[[^\]]+\]\s*)?正在等待上一任务释放 GPU 显存锁\.\.\.$""") to { m ->
            "${m.groupValues[1]}Esperando a que la tarea anterior libere el bloqueo de GPU..."
        },
        Regex("""^(\[[^\]]+\]\s*)?(.+?) 正在初始化潜空间并准备 (\d+) 步推理 \(Seed: (\d+)\)\.\.\.$""") to { m ->
            "${m.groupValues[1]}${m.groupValues[2]} inicializando espacio latente y preparando ${m.groupValues[3]} pasos (Seed: ${m.groupValues[4]})..."
        },
        Regex("""^(\[[^\]]+\]\s*)?VAE 解码完成，正在合成 32kHz 立体声音轨并封装 MP4 \((\d+)%\)\.\.\.$""") to { m ->
            "${m.groupValues[1]}Decodificación VAE lista; mezclando pista estéreo 32kHz y empaquetando MP4 (${m.groupValues[2]}%)..."
        },
        Regex("""^(\[[^\]]+\]\s*)?正在写入无损 PNG 图像文件 \((\d+)%\)\.\.\.$""") to { m ->
            "${m.groupValues[1]}Guardando archivo de imagen PNG sin pérdida (${m.groupValues[2]}%)..."
        },
        Regex("""^(\[[^\]]+\]\s*)?正在执行 MiniMax-H3-Image (\d+) 步 PDD 蒸馏原生超清采样 \(([^)]+)\)\.\.\.$""") to { m ->
            "${m.groupValues[1]}Ejecutando muestreo HD destilado PDD de ${m.groupValues[2]} pasos en MiniMax-H3-Image (${m.groupValues[3]})..."
        },
        Regex("""^第 (\d+/\d+) 项已完成 \(([\d.]+s)\)，已同步回传 Mac！继续生成第 (\d+) 项\.\.\.$""") to { m ->
            "Elemento ${m.groupValues[1]} completado (${m.groupValues[2]}). Generando el elemento ${m.groupValues[3]}..."
        },
        Regex("""^批量生成 (\d+) 项全部完成！总耗时 ([\d.]+s) \(平均 ([\d.]+s)/项\)$""") to { m ->
            "¡Lote de ${m.groupValues[1]} elementos completado! Total ${m.groupValues[2]} (promedio ${m.groupValues[3]}/elemento)"
        },
        Regex("""^生成完成！耗时 ([\d.]+s) \(Seed: (\d+)\)$""") to { m ->
            "¡Generación completada! Duración ${m.groupValues[1]} (Seed: ${m.groupValues[2]})"
        },
        Regex("""^\[(.+?)\] (图像|视频)生成完成 \| 耗时 ([\d.]+s) \| Seed: (\d+) \| 已保存:\s*(.+)$""") to { m ->
            val kind = if (m.groupValues[2] == "图像") "Imagen generada" else "Video generado"
            "[${m.groupValues[1]}] $kind | Duración ${m.groupValues[3]} | Seed: ${m.groupValues[4]} | Guardado: ${m.groupValues[5]}"
        },
        Regex("""^生成出错:\s*(.+)$""", RegexOption.DOT_MATCHES_ALL) to { m ->
            "Error al generar: ${m.groupValues[1]}"
        },
        Regex("""^\[任务控制\] 任务 (.+?) 已中断并释放 GPU 显存锁\.$""") to { m ->
            "[Control de tareas] Tarea ${m.groupValues[1]} interrumpida; bloqueo de VRAM liberado."
        },
        Regex("""^任务已提交至 Colab 队列 \(共 (\d+) 项\)\.\.\.$""") to { m ->
            "Tarea enviada a la cola de Colab (${m.groupValues[1]} elementos)..."
        },
        Regex("""^\[上下文配置\] 目标最大上下文长度已设为 (\d+K) \((\d+) tokens\)$""") to { m ->
            "[Contexto] Longitud máxima de contexto ajustada a ${m.groupValues[1]} (${m.groupValues[2]} tokens)"
        },
        Regex("""^\[(OpenAI|Anthropic) API\] 流式完成 \| (\d+) tokens \| ([\d.]+) tok/s$""") to { m ->
            "[${m.groupValues[1]} API] Stream completado | ${m.groupValues[2]} tokens | ${m.groupValues[3]} tok/s"
        }
    )

    fun localizeServerText(text: String): String {
        if (text.isEmpty()) return text
        val mTs = TS_PREFIX_REGEX.matchEntire(text)
        val tsPrefix = mTs?.groupValues?.get(1) ?: ""
        val body = (mTs?.groupValues?.get(2) ?: text).trim()
        val stripped = stripLeadingDecor(body)
        if (stripped.isEmpty()) return text

        if (stripped.startsWith("WAKE_ERROR:")) {
            val rest = stripped.removePrefix("WAKE_ERROR:").trim()
            return "${tsPrefix}Error de activación: ${localizeServerText(rest)}"
        }

        SERVER_EXACT_ZH_TO_ES[stripped]?.let { return tsPrefix + it }
        for ((pattern, repl) in SERVER_REGEX_ZH_TO_ES) {
            pattern.matchEntire(stripped)?.let { return tsPrefix + repl(it) }
        }

        val shardOut = localizeModelFileDesc(stripped)
        if (shardOut != stripped) {
            return tsPrefix + shardOut
        }
        if (!hasCjk(stripped)) {
            return tsPrefix + translateEn(stripped)
        }
        return tsPrefix + stripped
    }
}
