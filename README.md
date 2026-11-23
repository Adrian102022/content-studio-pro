# CONTENT STUDIO PRO

[Español](#español) · [English](#english)

## Español

Skill de Codex para investigar, producir y optimizar contenido para YouTube, Shorts, Instagram y TikTok. Incluye diez modos, módulos de carga progresiva, edición con Humanizer, validaciones locales y exportación con manifiesto SHA-256.

### Instalación y requisitos

Clona el repositorio directamente en la carpeta de skills del usuario de Codex. En PowerShell:

```powershell
git clone https://github.com/Adrian102022/content-studio-pro.git "$env:USERPROFILE/.agents/skills/content-studio-pro"
```

Para un proyecto concreto, usa `.agents/skills/content-studio-pro` bajo su raíz. Abre Codex e invoca `$content-studio-pro`. Para la CLI usa Python 3.10+. Pillow 9.1+ es opcional para normalizar y verificar imágenes. Generar imágenes requiere una herramienta conectada. Si no existe, el flujo prepara prompts. La investigación actual usa fuentes verificables y la analítica privada requiere archivos aportados o acceso de lectura autorizado.

### Comandos y ejemplos

```powershell
python -B scripts/studio.py plan "Modo Completo"
python -B scripts/studio.py plan "Módulo SEO"
python -B -m unittest discover -s tests -v
python -B scripts/studio.py check examples/ejemplo-sincronizacion --complete
```

En Windows, usa `py -3` o la ruta a un intérprete real si `python` es solo un alias. Prueba: `$content-studio-pro Modo completo. Prepara un video de YouTube sobre sincronizar audio grabado por separado y sus adaptaciones a Shorts, Instagram y TikTok.`

Consulta los [modos](references/modos.md), [comandos y formatos](references/herramientas.md), [flujo de exportación](references/exportacion.md) y el [proyecto de demostración](examples/ejemplo-sincronizacion/LEEME.md).

## English

A Codex skill for researching, producing, and optimizing content for YouTube, Shorts, Instagram, and TikTok. It includes ten modes, on-demand modules, Humanizer editing, a project brand profile, and a local CLI with SHA-256 export manifests.

### Install and run

Clone the repository into the Codex user skills directory on macOS or Linux:

```sh
git clone https://github.com/Adrian102022/content-studio-pro.git ~/.agents/skills/content-studio-pro
```

On Windows, use the PowerShell command above. For project scope, clone into `.agents/skills/content-studio-pro` under the project root. Open Codex and invoke `$content-studio-pro`. The CLI requires Python 3.10+. Pillow 9.1+ is optional for image normalization and verification. Image generation requires an available provider, with prompts as the fallback. Research uses verifiable sources. Private analytics require supplied data or authorized read access.

```sh
python3 -B scripts/studio.py plan "Modo Completo"
python3 -B scripts/studio.py plan "Módulo SEO"
python3 -B -m unittest discover -s tests -v
python3 -B scripts/studio.py check examples/ejemplo-sincronizacion --complete
```

Try `$content-studio-pro in complete mode. Draft a YouTube video on syncing separately recorded audio and adapt it for Shorts, Reels, and TikTok. Write the assets in English.`

See the [mode map](references/modos.md), [CLI reference](references/herramientas.md), [fictional demo](examples/ejemplo-sincronizacion/LEEME.md), and [third-party licensing](docs/CONTENIDO-DE-TERCEROS.md). The detailed module guides are in Spanish.

## Estructura / Repository layout

| Ruta / Path | Contenido / Contents |
| --- | --- |
| `SKILL.md`, `agents/` | Entrada y metadatos / Entrypoint and metadata |
| `references/`, `config/` | Módulos y perfil de marca / Modules and brand profile |
| `scripts/`, `tests/` | CLI y pruebas / CLI and tests |
| `docs/`, `third-party/` | Auditoría, atribuciones y dependencias incluidas / Audit, attribution, and vendored dependencies |
| `examples/` | Proyecto ficticio con miniaturas y metadatos / Fictional project with thumbnails and metadata |
