"""Reproduce checks and export a package from the versioned sample."""
from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import tempfile

import studio


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, help="New output directory to keep")
    parser.add_argument("--complete", action="store_true", help="Include and verify PNGs (requires Pillow)")
    args = parser.parse_args()
    sample = studio.ROOT / "examples/ejemplo-sincronizacion"

    try:
        with tempfile.TemporaryDirectory(prefix="content-studio-demo-") as directory:
            root = Path(directory)
            stage = sample
            if not args.complete:
                stage = root / "sample"
                shutil.copytree(
                    sample, stage,
                    ignore=shutil.ignore_patterns("*.png", "*.jpg", "*.jpeg", studio.MANIFEST),
                )
                (stage / "diseno/direccion.md").unlink()
                (stage / "titulos/finalistas.md").unlink()
                (stage / "control/estado.json").unlink()
                (stage / "control/checklist.md").unlink()
                (stage / "LEEME.md").write_text(
                    "# Demo de texto / Text demo\n\n"
                    "[Guion / Script](guiones/youtube.md) · [Títulos / Titles](titulos/titulos.json) · "
                    "[SEO](seo/publicacion.md) · [Shorts](shorts/01.md)\n",
                    encoding="utf-8",
                )
            studio.check(stage, args.complete)
            ranked = studio.titles(stage / "titulos/titulos.json")
            print("CONTENT STUDIO PRO | Local demo")
            print(f"Title candidates: {len(ranked['ranking'])}")
            print("Finalists: " + ", ".join(
                f"{item['id']} ({item['total']}/{ranked['escala_maxima']})"
                for item in ranked["finalistas"]
            ))
            output = args.out if args.out else root / "package"
            studio.export(stage, output, args.complete)
            result = studio.check(output, args.complete)
            print(f"Exported files: {result['archivos']}")
            print(f"Manifest verified: {'yes' if result['manifiesto_verificado'] else 'no'}")
            print("Image files: 3 (verified PNGs)" if args.complete else "Image files: excluded (text demo)")
            if args.out:
                print(f"Saved to: {output.resolve()}")
    except (OSError, ValueError, SyntaxError, OverflowError) as exc:
        parser.exit(2, f"Demo error: {exc}\n")


if __name__ == "__main__":
    main()
