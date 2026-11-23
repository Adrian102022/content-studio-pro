# Dependencies, licensing and review scope

| Component | Where it runs | Dependency and licensing |
| --- | --- | --- |
| Skill and editorial workflow | Codex | Codex and any authorized tools provided by that session. The repository MIT license covers original project content under its terms. |
| Local scripts and text demo | Python 3.10+ | Python standard library. No runtime package, API key or external service is needed for the text demo. |
| Image normalization and verification | Python with Pillow | Optional Pillow 9.1+ API compatibility. Use a current patched release. Pillow is installed separately under its own license. |
| Vendored YouTube Agent, Redes and Humanizer | Local Python or Markdown | MIT notices and pinned provenance are recorded in [Attributions](ATRIBUCIONES.md). |

Review scope: examined runtime imports, shipped paths, third-party notices, and the demo export boundary. Keep sensitive files outside export sections. The image workflow opens input files with Pillow. Use trusted files and check upstream advisories before selecting a version for unfamiliar inputs. Generators and private analytics depend on the Codex tool environment. [Pillow security advisories](https://github.com/python-pillow/Pillow/security/advisories).
