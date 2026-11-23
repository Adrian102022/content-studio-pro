# Contributing / Contribuir

Both English and Spanish are welcome. Start with an issue that includes the intended workflow, the expected outcome and an example anyone can reproduce. Use fictional or redistributable inputs. For security issues follow [SECURITY.md](SECURITY.md).

- Work from a fork. Keep each pull request focused on one change and link the issue where one exists.
- Verify `python -B -m unittest discover -s tests -v` and `python -B scripts/demo.py`. For image changes also run the complete demo with Pillow.
- For prompt or routing changes include a before/after example, the Codex surface and whether the agent had access to the referenced files. Keep mode-specific instructions in the corresponding reference.
- For vendored code include the pinned revision, original license and any local changes. For dependencies explain the need and which workflow uses them.
- When posting logs, redact local paths, credentials, account IDs and creator data.

**Para tu primera contribución.** Prueba la demo en macOS o Linux y documenta diferencias, añade un ejemplo breve de otro modo con datos sintéticos o mejora una guía de instalación. Abre un issue si necesitas coordinar algo. Mantén el respeto hacia autores, usuarios y revisores.
