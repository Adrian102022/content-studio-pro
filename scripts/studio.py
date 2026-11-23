"""Local routing, validation and export for CONTENT STUDIO PRO."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import sys
import tempfile
import unicodedata


ROOT = Path(__file__).resolve().parents[1]


def load_json(path):
    with path.open(encoding="utf-8-sig") as stream:
        return json.load(stream)


CONFIG = load_json(ROOT / "config/studio.json")
PROFILE = CONFIG["defaults"]["profile"]
TEMPLATE = ROOT / "config/marca.plantilla.json"
MANIFEST = "manifiesto.json"
IMAGE_EXTENSIONS = {".png": "PNG", ".jpg": "JPEG", ".jpeg": "JPEG"}


def json_text(value):
    return json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def nonblank(value):
    return isinstance(value, str) and bool(value.strip())


def normalized(value):
    letters = unicodedata.normalize("NFKD", value.casefold())
    return " ".join("".join(c for c in letters if not unicodedata.combining(c)).split())


def route(name, module_only=False):
    name = normalized(name)
    prefix, _, remainder = name.partition(" ")
    if prefix in {"modo", "modulo"} and remainder:
        name = remainder
        module_only = module_only or prefix == "modulo"
    modes, modules = CONFIG["modes"], CONFIG["modules"]
    if name in modes and not module_only:
        selection = modes[name]
        kind = "modo"
    else:
        require(name in modules, f"Ruta desconocida: {name}")
        selection = [name]
        kind = "modulo"
    references = dict.fromkeys(f"references/{modules[item]}.md" for item in selection)
    return {"id": name, "tipo": kind, "modulos": selection, "referencias": list(references)}


def profile(path, complete=False):
    data = load_json(path)
    template = load_json(TEMPLATE)
    require(isinstance(data, dict) and type(data.get("version")) is int
            and data["version"] == template["version"], "Versión de perfil inválida")
    for key, value in template.items():
        require(isinstance(data.get(key), type(value)), f"Tipo inválido o campo ausente: {key}")
        if isinstance(value, list):
            require(all(nonblank(item) for item in data[key]), f"Se esperaba una lista de textos: {key}")
    require(nonblank(data["idioma"]), "Indica el idioma del proyecto")
    require(all(isinstance(color, str) and re.fullmatch(r"#[0-9a-fA-F]{6}", color)
                for color in data["colores"].values()), "La paleta debe usar colores #RRGGBB")
    require(all(nonblank(value) for value in data["cta"].values()), "Las acciones CTA deben ser textos")
    if complete:
        for key in ("nombre", "publico", "nicho"):
            require(nonblank(data[key]), f"Completa el campo de marca: {key}")
    return {"perfil": path.name, "nombre": data["nombre"], "version": data["version"]}


def init_project(path):
    path.mkdir(parents=True, exist_ok=False)
    for directory in CONFIG["sections"]:
        (path / directory).mkdir()
    shutil.copyfile(TEMPLATE, path / PROFILE)
    return {"proyecto": str(path), "perfil": PROFILE}


def titles(path):
    candidates = load_json(path)
    counts, weights = CONFIG["counts"], CONFIG["title_weights"]
    require(isinstance(candidates, list) and len(candidates) == counts["titles"],
            f"Se esperan {counts['titles']} títulos")
    ids, names, ranked = set(), set(), []
    for row in candidates:
        require(isinstance(row, dict) and all(nonblank(row.get(key))
                for key in ("id", "titulo", "motivo")), "Cada título necesita id, titulo y motivo")
        clean_id = normalized(row["id"])
        name = re.sub(r"\W+", " ", normalized(row["titulo"])).strip()
        require(name and clean_id not in ids and name not in names, f"Título o ID repetido: {row['id']}")
        ids.add(clean_id)
        names.add(name)
        for key in weights:
            require(type(row.get(key)) is int and 0 <= row[key] <= 5,
                    f"{row['id']}: {key} debe ser un entero de 0 a 5")
        require(len(row["titulo"]) <= 100 and "\n" not in row["titulo"] and "\r" not in row["titulo"],
                f"{row['id']}: título de una sola línea, máximo 100 caracteres")
        ranked.append({**row, "total": sum(row[key] * weight for key, weight in weights.items())})
    ranked.sort(key=lambda row: (-row["total"], -row["fidelidad"], -row["claridad"]))
    finalists = [row for row in ranked if row["fidelidad"] >= 4][:counts["finalists"]]
    require(len(finalists) == counts["finalists"], "Faltan finalistas con fidelidad de 4 o 5")
    return {"escala_maxima": sum(weights.values()) * 5, "finalistas": finalists, "ranking": ranked}


def timestamp(seconds):
    minutes, second = divmod(seconds, 60)
    hours, minute = divmod(minutes, 60)
    tail = f"{minute:02d}:{second:02d}"
    return f"{hours}:{tail}" if hours else tail


def chapters(path):
    data = load_json(path)
    require(isinstance(data, dict) and nonblank(data.get("fuente")), "Indica la fuente temporal")
    duration, rows = data.get("duracion_s"), data.get("capitulos")
    require(type(duration) is int and duration >= 30, "Se requiere una duración comprobada de al menos 30 s")
    require(isinstance(rows, list) and len(rows) >= 3, "Se requieren al menos tres capítulos")
    previous, lines = -10, []
    for row in rows:
        require(isinstance(row, dict) and type(row.get("segundo")) is int
                and nonblank(row.get("titulo")), "Capítulo inválido")
        second, title = row["segundo"], row["titulo"].strip()
        require(lines or second == 0, "El primer capítulo debe comenzar en 00:00")
        require(second >= previous + 10 and second <= duration - 10,
                f"Intervalo corto, desordenado o fuera de duración: {second} s")
        require(len(title.splitlines()) == 1, "Cada título de capítulo debe ocupar una sola línea")
        lines.append(f"{timestamp(second)} {title}")
        previous = second
    return "\n".join(lines) + "\n"


def metrics(path):
    rows, seen = [], set()
    fields = ("segmento", "impresiones", "vistas_desde_impresiones")
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        require(reader.fieldnames == list(fields), f"CSV esperado: {','.join(fields)}")
        for row in reader:
            values = [row.get(field) for field in fields]
            require(None not in row and all(nonblank(value) for value in values),
                    f"Fila incompleta: {reader.line_num}")
            segment = values[0].strip()
            require(segment.casefold() not in seen, f"Segmento repetido: {segment}")
            seen.add(segment.casefold())
            require(all(re.fullmatch(r"[0-9]+", value.strip()) for value in values[1:]),
                    f"Usa conteos enteros no negativos: {segment}")
            impressions, views = map(int, values[1:])
            require(views <= impressions, f"Las vistas de impresiones exceden las impresiones: {segment}")
            rows.append(metric_row(segment, impressions, views))
    require(rows, "El CSV no contiene filas")
    total = metric_row("agregado", sum(r["impresiones"] for r in rows),
                       sum(r["vistas_desde_impresiones"] for r in rows))
    return {"segmentos": rows, "agregado_si_son_disjuntos": total}


def metric_row(segment, impressions, views):
    return {"segmento": segment, "impresiones": impressions, "vistas_desde_impresiones": views,
            "ctr_pct": round(100 * views / impressions, 6) if impressions else None}


def pillow():
    try:
        from PIL import Image, ImageOps
    except ImportError as exc:
        raise ValueError("Se necesita Pillow para normalizar o verificar imágenes") from exc
    return Image, ImageOps


def inspect_image(path, format_id):
    image, _ = pillow()
    spec = CONFIG["formats"][format_id]
    with image.open(path) as asset:
        require(asset.format == IMAGE_EXTENSIONS[path.suffix.lower()], f"Formato y extensión difieren: {path}")
        require(asset.size == (spec["width"], spec["height"]), f"Dimensiones incorrectas: {path}")
        require(getattr(asset, "n_frames", 1) == 1, f"El archivo debe ser estático: {path}")
        asset.verify()
    with image.open(path) as asset:
        asset.load()
    if "max_bytes" in spec:
        require(path.stat().st_size <= spec["max_bytes"], f"Archivo excede el peso configurado: {path}")


def resize_image(source, destination, format_id):
    image, ops = pillow()
    image_type = IMAGE_EXTENSIONS.get(destination.suffix.lower())
    require(image_type, "Usa extensión PNG, JPG o JPEG")
    require(not os.path.lexists(destination), f"La salida ya existe: {destination}")
    spec = CONFIG["formats"][format_id]
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=destination.parent) as temporary:
        result = Path(temporary) / destination.name
        with image.open(source) as original:
            require(getattr(original, "n_frames", 1) == 1, "Selecciona una imagen estática")
            oriented = ops.exif_transpose(original).convert("RGB")
            fitted = ops.fit(oriented, (spec["width"], spec["height"]), image.Resampling.LANCZOS)
            options = {"quality": 92, "optimize": True} if image_type == "JPEG" else {"optimize": True}
            fitted.save(result, format=image_type, **options)
        inspect_image(result, format_id)
        output = destination.open("xb")
        try:
            with output, result.open("rb") as stream:
                shutil.copyfileobj(stream, output)
        except BaseException:
            destination.unlink()
            raise
    return {"archivo": str(destination), "ancho": spec["width"], "alto": spec["height"]}


def image_category(name):
    for prefix, category in (("youtube-", "youtube"), ("reel-", "vertical"),
                             ("tiktok-", "vertical"), ("carrusel-", "carrusel")):
        if name.startswith(f"diseno/{prefix}"):
            return category
    return None


def safe_entry(path):
    meta = path.lstat()
    reparse = getattr(meta, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    require(not reparse and (stat.S_ISREG(meta.st_mode) or stat.S_ISDIR(meta.st_mode)),
            f"Ruta de exportación no regular: {path}")
    return stat.S_ISDIR(meta.st_mode)


def collect_section(path):
    if safe_entry(path):
        for child in sorted(path.iterdir()):
            yield from collect_section(child)
    elif path.suffix.lower() in CONFIG["extensions"]:
        yield path


def package_files(root):
    require(safe_entry(root), "El proyecto debe ser un directorio")
    files = {}
    for name in (PROFILE, "LEEME.md"):
        path = root / name
        if os.path.lexists(path):
            require(not safe_entry(path), f"Se esperaba un archivo: {path}")
            files[name] = path
    for name in CONFIG["sections"]:
        section = root / name
        if os.path.lexists(section):
            require(safe_entry(section), f"Se esperaba una carpeta: {section}")
            files.update((p.relative_to(root).as_posix(), p) for p in collect_section(section))
    return files


def validate_complete(files):
    counts = CONFIG["counts"]
    expected = CONFIG["complete_files"] + [f"shorts/{i:02}.md" for i in range(1, counts["shorts"] + 1)]
    missing = sorted(set(expected) - files.keys())
    require(not missing, "Faltan entregables: " + ", ".join(missing))
    profile(files[PROFILE], complete=True)
    ranked = titles(files["titulos/titulos.json"])
    final_text = files["titulos/finalistas.md"].read_text(encoding="utf-8-sig")
    require(all(row["titulo"] in final_text for row in ranked["finalistas"]),
            "El documento de finalistas debe incluir los tres títulos seleccionados")
    status = load_json(files["control/estado.json"])
    require(isinstance(status, dict), "Se esperaba un objeto para control/estado.json")
    for key, states in (("miniaturas", {"lista", "parcial", "pendiente"}), ("capitulos", {"lista", "pendiente"})):
        item = status.get(key)
        require(isinstance(item, dict) and isinstance(item.get("estado"), str)
                and item["estado"] in states and nonblank(item.get("detalle")), f"Estado inválido: {key}")

    variants = {f"diseno/youtube-{i:02}" for i in range(1, counts["thumbnails"] + 1)}
    asset_names = [name for name in files if image_category(name) == "youtube"
                   and Path(name).suffix.lower() in IMAGE_EXTENSIONS]
    stems = [name.rsplit(".", 1)[0] for name in asset_names]
    require(len(set(stems)) == len(stems) and set(stems) <= variants, "Miniaturas duplicadas o mal nombradas")
    actual = "lista" if len(stems) == len(variants) else "parcial" if stems else "pendiente"
    require(status["miniaturas"]["estado"] == actual, "El estado de miniaturas difiere de los archivos")
    require(actual == "lista" or "diseno/prompts.md" in files, "Faltan prompts de miniaturas pendientes")

    source, rendered = "seo/capitulos.json", "seo/capitulos.txt"
    if status["capitulos"]["estado"] == "lista":
        require(source in files and rendered in files, "Faltan capítulos en JSON y TXT")
        require(chapters(files[source]) == files[rendered].read_text(encoding="utf-8-sig"),
                "El TXT de capítulos difiere del generado por su JSON")
    else:
        require(source not in files and rendered not in files, "Retira capítulos sin verificar del paquete")


def file_digest(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def inspect_project(root, complete):
    files = package_files(root)
    require(len(files) > 1 or PROFILE not in files, "Aún no hay entregables")
    require(files, "Carpeta sin archivos exportables")
    for name, path in files.items():
        require(path.stat().st_size > 0, f"Archivo vacío: {name}")
        category = image_category(name)
        if category and path.suffix.lower() in IMAGE_EXTENSIONS:
            inspect_image(path, category)
    if PROFILE in files and not complete:
        profile(files[PROFILE])
    if complete:
        validate_complete(files)
    entries = [{"ruta": name, "bytes": path.stat().st_size, "sha256": file_digest(path)}
               for name, path in sorted(files.items())]
    return files, entries


def check(root, complete):
    _, entries = inspect_project(root, complete)
    manifest = root / MANIFEST
    if os.path.lexists(manifest):
        require(not safe_entry(manifest), "Manifiesto no regular")
        data = load_json(manifest)
        require(isinstance(data, dict) and data.get("archivos") == entries,
                "El manifiesto difiere de los archivos; exporta una versión nueva")
    return {"valido": True, "archivos": len(entries), "manifiesto_verificado": manifest.is_file()}


def export(source, destination, complete):
    files, _ = inspect_project(source, complete)
    destination = destination.absolute()
    require(not os.path.lexists(destination), f"La salida ya existe: {destination}")
    require(not destination.resolve().is_relative_to(source.resolve()),
            "La salida debe quedar fuera del proyecto de trabajo")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=destination.parent, prefix=".studio-") as temporary:
        stage = Path(temporary) / "paquete"
        stage.mkdir()
        for name, path in files.items():
            target = stage / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)
        _, entries = inspect_project(stage, complete)
        (stage / MANIFEST).write_text(json_text({"version": 1, "completo": complete, "archivos": entries}),
                                      encoding="utf-8", newline="\n")
        lock = destination.with_name(destination.name + ".export-lock")
        with lock.open("x", encoding="utf-8"):
            pass
        try:
            require(not os.path.lexists(destination), f"La salida ya existe: {destination}")
            stage.rename(destination)
        finally:
            lock.unlink()
    return {"exportado": str(destination), "archivos": len(entries), "manifiesto": MANIFEST}


def parser():
    cli = argparse.ArgumentParser(description=__doc__)
    commands = cli.add_subparsers(dest="command", required=True)
    plan = commands.add_parser("plan", help="Resuelve las referencias del modo o módulo")
    plan.add_argument("name")
    plan.add_argument("--module", action="store_true", dest="module_only")
    plan.set_defaults(action=lambda args: route(args.name, args.module_only))

    for name, function in (("init", init_project), ("profile", profile), ("titles", titles),
                           ("metrics", metrics)):
        command = commands.add_parser(name)
        command.add_argument("path", type=Path)
        command.set_defaults(action=lambda args, fn=function: fn(args.path))

    chapter = commands.add_parser("chapters")
    chapter.add_argument("path", type=Path)
    chapter.add_argument("--out", type=Path)
    chapter.set_defaults(action=write_chapters)

    image = commands.add_parser("image")
    image.add_argument("source", type=Path)
    image.add_argument("destination", type=Path)
    image.add_argument("--format", choices=CONFIG["formats"], required=True)
    image.set_defaults(action=lambda args: resize_image(args.source, args.destination, args.format))

    verify = commands.add_parser("check")
    verify.add_argument("source", type=Path)
    verify.add_argument("--complete", action="store_true")
    verify.set_defaults(action=lambda args: check(args.source, args.complete))
    bundle = commands.add_parser("export")
    bundle.add_argument("source", type=Path)
    bundle.add_argument("destination", type=Path)
    bundle.add_argument("--complete", action="store_true")
    bundle.set_defaults(action=lambda args: export(args.source, args.destination, args.complete))
    return cli


def write_chapters(args):
    result = chapters(args.path)
    if args.out is None:
        return result
    with args.out.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(result)
    return {"archivo": str(args.out)}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    args = parser().parse_args()
    try:
        output = args.action(args)
    except (OSError, ValueError, SyntaxError, OverflowError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    sys.stdout.write(output if isinstance(output, str) else json_text(output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
