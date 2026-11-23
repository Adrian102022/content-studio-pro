# Control de calidad y exportación

Revisa ortografía, voz, evidencia, originalidad frente a fuentes, lectura móvil, SEO, CTA, adecuación por plataforma y cumplimiento de la promesa por título, arte y apertura. Registra revisión técnica y editorial. Identifica los activos listos para grabar, montar o publicar.

Usa `studio.py init <trabajo>`, escribe en las secciones configuradas y completa `LEEME.md`. Usa `shorts/01.md` a `03.md` para Completo. Para capítulos reales, guarda `seo/capitulos.json` y genera `seo/capitulos.txt`. CSV debe ser UTF-8 y apto para hojas de cálculo cuando proceda.

En `control/estado.json` registra `miniaturas` y `capitulos`, cada uno con `estado` y `detalle`. Miniaturas admite `lista`, `parcial`, `pendiente`, y requiere `diseno/prompts.md` si faltan variantes. Capítulos admite `lista` o `pendiente`. Anota fuentes, herramienta o dependencia.

Ejecuta `studio.py check <trabajo> --complete` y `studio.py export <trabajo> <salida> --complete`. Omite `--complete` para entregas parciales. La salida genera `manifiesto.json` con rutas, tamaños y SHA-256; evita sobrescribir. Mantén insumos privados y descartes fuera de las secciones destinadas a exportación.
