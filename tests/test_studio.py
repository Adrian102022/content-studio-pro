import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
import studio


class StudioTests(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory(prefix="CSP pruebas ")
        self.addCleanup(self.workspace.cleanup)
        self.root = Path(self.workspace.name)

    def file(self, name, contents):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(contents, encoding="utf-8")
        return path

    def test_progressive_routes(self):
        self.assertEqual(len(studio.CONFIG["modes"]), 10)
        for key in studio.CONFIG["modes"]:
            with self.subTest(key=key):
                refs = studio.route(key)["referencias"]
                self.assertEqual(len(refs), len(set(refs)))
                self.assertTrue(all((ROOT / ref).is_file() for ref in refs))
        for key in studio.CONFIG["modules"]:
            self.assertEqual(len(studio.route(key, module_only=True)["referencias"]), 1)
        self.assertEqual(studio.route("Módulo SEO")["referencias"], ["references/seo.md"])
        self.assertNotIn("references/diseno.md", studio.route("Modo Humanizer")["referencias"])
        with self.assertRaises(ValueError):
            studio.route("inexistente")

    def test_profile_and_init_no_overwrite(self):
        path = self.root / "Proyecto ñ"
        studio.init_project(path)
        self.assertEqual(studio.profile(path / studio.PROFILE)["version"], 1)
        with self.assertRaises(FileExistsError):
            studio.init_project(path)
        profile = studio.load_json(path / studio.PROFILE)
        profile["colores"] = {"primario": "amarillo"}
        with self.assertRaises(ValueError):
            studio.profile(self.file("mala.json", json.dumps(profile)))

    def candidates(self):
        items = [dict(id=f"T{i}", titulo=f"Prueba de título {i}", fidelidad=4, claridad=4,
                      curiosidad=4, seo=4, motivo="Se muestra en el guion") for i in range(10)]
        items[0].update(fidelidad=3, claridad=5, curiosidad=5, seo=5)
        items[4].update(fidelidad=5)
        return items

    def test_titles_fidelity_and_tie_break(self):
        items = self.candidates()
        path = self.file("titulos.json", json.dumps(items))
        ranked = studio.titles(path)
        self.assertEqual([x["id"] for x in ranked["finalistas"]], ["T4", "T1", "T2"])
        items[-1]["titulo"] = "Prueba de titulo 1?"
        with self.assertRaisesRegex(ValueError, "repetido"):
            studio.titles(self.file("titulos.json", json.dumps(items)))

    def test_chapters_order_and_final_segment(self):
        data = {"fuente": "Fixture sintético", "duracion_s": 40, "capitulos": [
            {"segundo": 0, "titulo": "Inicio"},
            {"segundo": 12, "titulo": "Edición"},
            {"segundo": 30, "titulo": "Cierre"},
        ]}
        self.assertEqual(studio.chapters(self.file("tiempos.json", json.dumps(data))),
                         "00:00 Inicio\n00:12 Edición\n00:30 Cierre\n")
        for bad in (5, 31, 45):
            data["capitulos"][2]["segundo"] = bad
            with self.assertRaisesRegex(ValueError, "Intervalo"):
                studio.chapters(self.file("tiempos.json", json.dumps(data)))

    def test_ctr_uses_denominator_and_preserves_zero(self):
        prefix = "segmento,impresiones,vistas_desde_impresiones\n"
        path = self.file("métricas.csv", prefix + "Búsqueda,200,8\nSugeridos,50,7\nOtros,0,0\n")
        result = studio.metrics(path)
        self.assertEqual(result["agregado_si_son_disjuntos"]["ctr_pct"], 6)
        self.assertIsNone(result["segmentos"][2]["ctr_pct"])
        with self.assertRaisesRegex(ValueError, "exceden"):
            studio.metrics(self.file("inválido.csv", prefix + "Otros,1,2\n"))

    def stage_complete(self):
        path = self.root / "stage"
        studio.init_project(path)
        for filename in studio.CONFIG["complete_files"]:
            self.file(f"stage/{filename}", "Archivo de la prueba\n")
        values = studio.load_json(studio.TEMPLATE)
        values.update(nombre="Prueba", publico="Adultos", nicho="Edición")
        self.file("stage/marca.json", json.dumps(values))
        titles = self.file("stage/titulos/titulos.json", json.dumps(self.candidates()))
        selected = "\n".join(r["titulo"] for r in studio.titles(titles)["finalistas"])
        self.file("stage/titulos/finalistas.md", selected)
        for i in range(1, 4):
            self.file(f"stage/shorts/{i:02}.md", f"Guion de prueba {i}")
        self.file("stage/diseno/prompts.md", "Prompts de prueba")
        status = {"miniaturas": {"estado": "pendiente", "detalle": "Prueba de fallback"},
                  "capitulos": {"estado": "pendiente", "detalle": "Sin tiempos"}}
        self.file("stage/control/estado.json", json.dumps(status))
        return path

    def test_complete_export_and_manifest(self):
        src = self.stage_complete()
        output = self.root / "Entrega á"
        self.file("stage/solo-lectura/original.md", "Entrada excluida")
        studio.export(src, output, True)
        self.assertTrue(studio.check(output, True)["manifiesto_verificado"])
        self.assertFalse((output / "solo-lectura").exists())
        with self.assertRaisesRegex(ValueError, "ya existe"):
            studio.export(src, output, True)
        (output / "shorts/02.md").write_text("Cambio local", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "manifiesto"):
            studio.check(output, True)

    def test_complete_failures_are_not_exported(self):
        src = self.stage_complete()
        output = self.root / "paquete"
        (src / "diseno/prompts.md").unlink()
        with self.assertRaisesRegex(ValueError, "Faltan prompts"):
            studio.export(src, output, True)
        self.assertFalse(output.exists())
        self.file("stage/diseno/prompts.md", "Recuperado")
        self.file("stage/seo/capitulos.txt", "00:00 Sin fuente")
        with self.assertRaisesRegex(ValueError, "sin verificar"):
            studio.check(src, True)

    def test_partial_export_from_cli(self):
        self.file("stage/seo/Copy breve.md", "¿Listo?")
        cmd = [sys.executable, "-B", str(SCRIPTS / "studio.py"), "export",
               str(self.root / "stage"), str(self.root / "salida")]
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", check=True)
        self.assertEqual(json.loads(result.stdout)["archivos"], 1)
        self.assertEqual((self.root / "salida/seo/Copy breve.md").read_text(encoding="utf-8"), "¿Listo?")

    @unittest.skipUnless(importlib.util.find_spec("PIL"), "Prueba de imagen requiere Pillow")
    def test_image_dimensions_and_decoding(self):
        from PIL import Image
        source = self.root / "foto original.png"
        Image.new("RGB", (300, 200), "#123d3c").save(source)
        for name, category in (("youtube-01.png", "youtube"), ("reel-01.jpg", "vertical"),
                               ("carrusel-01.png", "carrusel")):
            with self.subTest(category=category):
                output = self.root / "diseno" / name
                result = studio.resize_image(source, output, category)
                self.assertEqual(result["ancho"], studio.CONFIG["formats"][category]["width"])
                studio.inspect_image(output, category)
                with self.assertRaisesRegex(ValueError, "ya existe"):
                    studio.resize_image(source, output, category)
        fake = self.file("falsa.png", "texto sin imagen")
        with self.assertRaises(OSError):
            studio.inspect_image(fake, "youtube")


class OriginalYoutubeTests(unittest.TestCase):
    def test_six_original_cli_entry_points(self):
        youtube = ROOT / "third-party/youtube"
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            transcript = root / "captions.srt"
            transcript.write_text("\n\n".join(
                f"{i}\n00:00:{start:02},000 --> 00:00:{start+3:02},000\n{line}"
                for i, (start, line) in enumerate(
                    [(0, "How you sync sound"), (3, "Record a clap"),
                     (12, "Move the external track"), (15, "Find the waveform"),
                     (24, "Verify the picture and sound"), (39, "Last step")], 1)), encoding="utf-8")
            retention = root / "retention.csv"
            retention.write_text("position_pct,retention_pct\n0,100\n5,98\n10,94\n20,92\n40,85\n60,80\n80,78\n100,70\n",
                                 encoding="utf-8")
            swipe = root / "swipe.json"
            swipe.write_text(json.dumps([
                {"title": f"How to sync microphone {i}", "channel": "Fixture",
                 "views": views, "url": f"https://example.test/video{i}"}
                for i, views in enumerate((900, 1000, 1000, 3000), 1)
            ]), encoding="utf-8")
            fixtures = {
                "yt-script/hookscore.py": ["--hook", "How you save 20 minutes today"],
                "yt-package/title.py": ["--title", "How to sync external sound", "--thumb", "ONE CLAP"],
                "yt-edit/deadair.py": [str(transcript), "--json"],
                "yt-chapters/chapters.py": [str(transcript), "--target", "3", "--json"],
                "yt-retention/retention.py": [str(retention), "--duration", "40", "--json"],
                "yt-viral/swipe.py": [str(swipe), "--min", "2.0", "--json"],
            }
            for relative, arguments in fixtures.items():
                with self.subTest(relative=relative):
                    output = subprocess.run([sys.executable, "-B", "-X", "utf8", str(youtube / relative), *arguments],
                                            capture_output=True, text=True, encoding="utf-8")
                    self.assertEqual(output.returncode, 0, output.stderr + output.stdout)
                    self.assertTrue(output.stdout.strip())
                    if relative.startswith("yt-viral"):
                        self.assertEqual(json.loads(output.stdout)["outliers"][0]["multiple"], 3)
                    elif relative.startswith("yt-chapters"):
                        self.assertTrue(json.loads(output.stdout)["valid"])
                    elif relative.startswith("yt-retention"):
                        self.assertEqual(json.loads(output.stdout)["points"], 8)


if __name__ == "__main__":
    unittest.main()
