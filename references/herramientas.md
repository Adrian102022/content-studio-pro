# Herramientas locales

Usa Python 3.10+. En PowerShell prueba `py -3` o invoca por ruta absoluta un intérprete real, incluido el de Workspace Dependencies de Codex Desktop. La CLI base usa biblioteca estándar. El normalizador y el verificador de imágenes usan Pillow 9.1+ para comprobar dimensiones, integridad y decodificación. Los paquetes puramente textuales funcionan sin Pillow.

| Acción | Comando desde la skill |
| --- | --- |
| Ruta / módulo | `python scripts/studio.py plan "modo YouTube"` / `… plan SEO --module` |
| Proyecto / perfil | `… init <trabajo>` / `… profile <trabajo>/marca.json` |
| Títulos | `… titles <titulos.json>` |
| Capítulos | `… chapters <capitulos.json> --out <capitulos.txt>` |
| Imagen | `… image <origen> <destino.png> --format youtube` |
| CTR | `… metrics <datos.csv>` |
| Verificar/exportar | `… check <trabajo> --complete` / `… export <trabajo> <destino> --complete` |

Capítulos JSON: `fuente`, `duracion_s` entero y `capitulos` listando `{segundo,titulo}`. La fuente identifica la grabación o transcripción temporizada. CTR CSV: `segmento,impresiones,vistas_desde_impresiones` con conteos enteros. Para agregar usa segmentos disjuntos y comparables con la misma definición.

## Código original reutilizado

YouTube bajo `third-party/youtube/<skill>/`. En Windows invoca `python -X utf8` si procesas Unicode. Usa rutas absolutas de entrada. Los contratos detallados están en las docstrings.

- `yt-script/hookscore.py <hooks.txt> --json` o `--hook "…"`; banco de 21 fórmulas en `hooks.json`.
- `yt-package/title.py --title "…" --thumb "…"` o archivo de títulos.
- `yt-edit/deadair.py <transcripcion.srt> --floor 0.35 --json`. Acepta SRT, VTT y JSON de Whisper.
- `yt-chapters/chapters.py <transcripcion.srt> --target 8`. Requiere al menos seis cues. Revisa contra duración real con el nuevo validador.
- `yt-retention/retention.py <retencion.csv> --duration 600 --transcript <transcripcion.srt> --json`. Pon posición como porcentaje 0–100, retención como porcentaje y al menos ocho puntos; proporciona la duración real para evitar ambigüedad con segundos en videos cortos.
- `yt-viral/swipe.py <capturas.json> --min 2.0`. Campos `title`, `channel`, `views`, `url`. Calcula la mediana a partir de un mínimo de cuatro videos por canal.

Redes desde `third-party/redes`: `python -B -m herramientas.<nombre>` con rutas absolutas. Todos aceptan `--json`. `ganchos <hooks.txt>` o `ganchos --gancho "…"`, `ritmo <guion.txt> --objetivo 30 --ppm 170`, `pie <pie.txt> --red instagram --palabras "…"`, `humanizar <borrador.txt> --informe`, `detectar <antes.txt> <despues.txt>`, `viral <capturas.tsv> --md <banco.md>`. En `herramientas/` se guardan 26 fórmulas, léxico y rúbrica.
