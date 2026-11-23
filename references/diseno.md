# Diseño y archivos de imagen

Usa [las dimensiones configuradas](../config/studio.json): YouTube 1280 × 720, Reels y TikTok 1080 × 1920, carrusel 1080 × 1350. Para YouTube diseña tres conceptos distintos: título asociado, texto literal, sujeto, jerarquía, composición, márgenes y paleta. Comprueba superposiciones y recorte de perfil según ubicación. Consulta límites oficiales vigentes si afectan la entrega.

Descubre los generadores de la sesión y prioriza el de imágenes de OpenAI. Usa una llamada por variante. Pide proporción y espacio para ajuste. Para ortografía complicada, genera fondo limpio y añade la tipografía en un editor disponible. Evita representar material generado como evidencia fotográfica real.

Persiste el arte. Si difiere el tamaño, usa `studio.py image <origen> <destino> --format <youtube|vertical|carrusel>` con Pillow. Vuelve a mirar el resultado para tildes, peso, encuadre, artes sintéticas, márgenes, controles, contraste y lectura en móvil. En `diseno/direccion.md` registra prompts usados y decisión de QA. Usa `diseno/youtube-01.png` a `youtube-03.png` o equivalente JPG y prefijos `reel-`, `tiktok-`, `carrusel-` para otras portadas. Si falta una salida real, guarda la parte lograda, explica el motivo y deja prompts detallados en `diseno/prompts.md` para las variantes pendientes.
