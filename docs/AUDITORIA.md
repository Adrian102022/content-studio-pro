# Auditoría y matriz de capacidades

**Fecha:** 23 de noviembre de 2026. Se clonaron ambos repositorios a una carpeta de trabajo tras un bloqueo de DNS en el sandbox. Se revisaron todos los SKILL.md de ambos árboles, sus equivalentes instalados, scripts, JSON, plantillas, manifests, README, pruebas y licencias. Se inspeccionó Humanizer local antes de integrarlo. Versiones y avisos en [Atribuciones](ATRIBUCIONES.md).

## Fuentes y entorno

- **YouTube Agent.** Once skills, seis scripts estándar de Python, 21 fórmulas, plantilla compartida de voz y manifiestos Claude. El árbol público fijado no contiene una suite de pruebas. Las once instrucciones instaladas tienen ajustes para Codex o rutas de los scripts, con el mismo alcance funcional.
- **Redes.** Trece modos, seis comandos (gancho, ritmo, pie, limpieza, diagnóstico y viral), JSON de 26 fórmulas, léxico, rúbrica y 24 pruebas. El README llama «cinco» al conjunto en su resumen. La instalación de Codex divide instrucciones en 13 referencias y reubica recursos y comandos. Se conservó el flujo editorial modular y se reutilizó el paquete Python público completo.
- **Humanizer.** La versión local 3.1.0 documenta 26 patrones, ejemplos, voz, criterio de edición y elementos que conviene preservar. Tiene metadatos para varios agentes y un validador de paquete. Su aplicación editorial vive en una referencia breve y se conserva el texto íntegro en lectura bajo demanda.
- **Content Studio previo.** Se revisó el orquestador instalado como contexto. Compartía voz y fuentes mientras encadenaba skills originales. El nuevo paquete resuelve su propia ruta dentro de una sola skill y usa herramientas reutilizadas que se distribuyen con ella.
- **Windows.** En este entorno `python` y `py` apuntaron a alias no ejecutables. Usamos Python 3.12.14 y Pillow 13.0.0 ya empaquetados. No se instalaron dependencias nuevas. Las copias instaladas de origen se leyeron sin editarlas.

## Matriz

| Capacidad | YouTube Agent | Redes | Humanizer | CONTENT STUDIO PRO |
| --- | --- | --- | --- | --- |
| Investigación y viral | yt-viral, múltiplo por canal, fórmulas | Viral, mediana, banco de referencias |  | Investigación verificable por tema, consulta, público y competencia, con contexto y cobertura. Conserva ambos calculadores. |
| Estrategia | yt-plan, ancla y piezas de bajo esfuerzo | Plan, mezcla y registro |  | Capacidad real, pilares, series, planes semanales/mensuales, estimación y fuentes compartidas. |
| Guion | yt-script, cinco ganchos, 21 fórmulas, beats | Guion corto, 26 fórmulas, ritmo y rótulos | Voz y concisión | Guion hablado y visual, ganchos con rúbrica por idioma, guiones de post, carrusel y vertical. |
| Títulos y empaque | yt-package, diez propuestas, lint y pareja | Portada breve para social |  | Pesos editoriales, validación de cantidad, unicidad, fidelidad y razones para tres finalistas. |
| Imágenes | Texto de miniatura y previsualización | Composición y texto por lámina |  | Proveedor de imágenes, tres miniaturas reales, normalización en tres formatos, revisión a escala móvil y prompts si falla. |
| SEO | yt-seo, capítulos, tags y consultas | Texto, primera línea, búsqueda y hashtags | Preservación editorial | Metadatos, comentario fijado y CTA con nombres y hechos preservados. Capítulos cotejados con duración real. |
| Humanización | Perfil de voz | Limpieza y rúbrica heurística en español | Edición en 26 patrones | Edición contextual antes de publicar el paquete, revisión oral y herramientas opcionales en español. |
| Retención | yt-retention, fuga, cortes, caída, cierre | Hoja de ritmo, retención a 3 s | Ritmo de frase | Guía para guion y para curva, normalización de datos y contraste con la pieza original. |
| Reutilización | yt-shorts, selección autónoma y primera línea nueva | Reutilizar video, podcast y newsletter | Voz | Tres Shorts, versiones nativas por canal, fuente por sección o tiempo real y recursos para derivados. |
| Producción | yt-edit, transcripción, silencios y retomas | Ritmo, rótulos, subtítulos |  | Storyboards, escenas, B-roll, textos, preparación de subtítulos y lista de cortes. |
| Analítica y auditoría | yt-audit y yt-retention | Auditoría y rúbrica de perfil |  | Métricas observadas, CTR con denominador, análisis de canal/perfil, prueba con señales y ventanas. |
| Marca | Archivo de voz | Voz y registro | Imita preferencias del autor | JSON de proyecto, paleta, estilo, público, objetivos, CTA y muestras. |
| Comunidad | yt-comment, triage y fijado | Comentar, Responder, Mensajes | Voz | Clasificación, borradores contextuales, dos opciones en otros posts, mensajes y seguimientos. |
| Historias y carrusel |  | Recursos y flujos nativos |  | Módulo Social con secuencias y stickers, accesibilidad e imágenes al pedirlas. |
| Exportación y control | Bloques copiables y lint | Bloques copiables y checks | Texto final | Estructura de proyecto, manifiesto con SHA-256, validación técnica y checklist editorial. |

## Duplicidades y decisiones

1. Los bancos de ganchos se solapan en propósito y sus heurísticas pertenecen a idiomas y formatos distintos. Se elige una rúbrica por pieza y se conserva la otra disponible. Los puntajes sirven de diagnóstico editorial.
2. Los flujos de voz y edición se consolidaron en perfil y Humanizer. Las sustituciones de Redes son opcionales y se revisan por cambio de sentido. Se mantiene ortotipografía española normal.
3. Los caminos de investigación y auditoría comparten evidencia y reglas de comparación. Los umbrales heredados son heurísticos. Se documentó la inferencia del eje de retención y el mínimo de muestras de los scripts.
4. Las menciones Claude, la escritura global del registro, los comandos obligatorios y el cierre fijo se sustituyeron por rutas de Codex, datos locales y revisión adecuada al alcance. Eso evita bloqueos si todavía no existe una muestra de voz y reduce lecturas repetidas.
5. Los textos de portada y validaciones de SEO se conservan y se amplían con imagen, prueba de recorte, capítulos verificables y contrato de exportación. Los límites de interfaz y plataforma se revisan al publicar. La dimensión 1280 × 720 y el máximo conservador de 2 MB para YouTube se configuraron para este encargo. [Ayuda de miniaturas de YouTube](https://support.google.com/youtube/answer/72431).
6. La CLI implementa verificaciones de máquina; la calidad de voz, veracidad, intención y composición siguen requiriendo revisión editorial. Las fuentes privadas y el acceso a cada generador dependen de las herramientas autorizadas en la sesión.
