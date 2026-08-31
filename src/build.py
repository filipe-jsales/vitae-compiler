#!/usr/bin/env python3
"""Compila o currículo: valida dados -> gera .tex -> compila PDF -> exporta
JSON Resume + TXT.

Uso:
    python src/build.py [--data DATA_DIR] [--lang pt en] [--template academico-padrao]
                         [--output-dir OUTPUT_DIR] [--skip-pdf]

O build falha (exit != 0) se a validação de schema falhar ou se nenhum
compilador LaTeX (tectonic ou latexmk) estiver disponível e --skip-pdf não
tiver sido passado.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from markupsafe import Markup

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from labels import LABELS, SUPPORTED_LANGUAGES  # noqa: E402
from validate import DATASETS, validate_all  # noqa: E402
from export_json import export_json_resume, export_txt  # noqa: E402

# Delimitadores compatíveis com sintaxe LaTeX (evita colisão com {}, %, #).
LATEX_JINJA_OPTIONS = dict(
    block_start_string=r"\BLOCK{",
    block_end_string="}",
    variable_start_string=r"\VAR{",
    variable_end_string="}",
    comment_start_string=r"\#{",
    comment_end_string="}",
    line_statement_prefix="%%",
    line_comment_prefix="%#",
    trim_blocks=True,
    autoescape=False,
)

# Caracteres especiais do LaTeX. Todo valor injetado via \VAR{...} passa por
# aqui (ver `finalize` abaixo) para que dados do YAML (títulos, nomes, etc.)
# nunca sejam interpretados como comandos LaTeX — evita tanto builds quebrados
# quanto injeção de comandos via dados de entrada. Valores explicitamente
# marcados com o filtro `safe` (ex.: pedaços de URL dentro de \url{...}) não
# passam por esse escape.
_LATEX_ESCAPE_MAP = {
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
    "\\": r"\textbackslash{}",
}
_LATEX_ESCAPE_RE = re.compile("|".join(re.escape(c) for c in _LATEX_ESCAPE_MAP))


def escape_tex(value):
    if value is None:
        return ""
    if isinstance(value, Markup):
        return value
    text = str(value)
    return _LATEX_ESCAPE_RE.sub(lambda m: _LATEX_ESCAPE_MAP[m.group()], text)


def load_data(data_dir: Path) -> dict:
    data = {}
    for name in DATASETS:
        path = data_dir / f"{name}.yaml"
        if path.exists():
            with path.open("r", encoding="utf-8") as fh:
                data[name] = yaml.safe_load(fh) or ([] if name != "perfil" else {})
        else:
            data[name] = [] if name != "perfil" else {}
    return data


def render_tex(template_dir: Path, build_dir: Path, data: dict, lang: str) -> Path:
    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        undefined=StrictUndefined,
        finalize=escape_tex,
        **LATEX_JINJA_OPTIONS,
    )
    context = {**data, "lang": lang, "labels": LABELS[lang]}

    build_dir.mkdir(parents=True, exist_ok=True)
    (build_dir / "secoes").mkdir(parents=True, exist_ok=True)

    # copia arquivos estáticos do tema (theme.sty)
    for extra in template_dir.glob("*.sty"):
        shutil.copy(extra, build_dir / extra.name)

    main_template = env.get_template("main.tex.j2")
    (build_dir / "main.tex").write_text(main_template.render(**context), encoding="utf-8")

    for section_template_path in (template_dir / "secoes").glob("*.tex.j2"):
        rel = f"secoes/{section_template_path.name}"
        tpl = env.get_template(rel)
        out_name = section_template_path.name[: -len(".j2")]
        (build_dir / "secoes" / out_name).write_text(tpl.render(**context), encoding="utf-8")

    return build_dir / "main.tex"


def find_compiler() -> tuple[str, list[str]] | None:
    if shutil.which("tectonic"):
        return "tectonic", ["tectonic", "main.tex"]
    if shutil.which("latexmk"):
        return "latexmk", ["latexmk", "-pdf", "-interaction=nonstopmode", "main.tex"]
    return None


def compile_pdf(build_dir: Path) -> Path:
    compiler = find_compiler()
    if compiler is None:
        raise RuntimeError(
            "Nenhum compilador LaTeX encontrado (tectonic ou latexmk). "
            "Instale um deles ou rode com --skip-pdf. Veja CONTRIBUTING.md."
        )
    name, cmd = compiler
    print(f"Compilando com {name}...")
    result = subprocess.run(cmd, cwd=build_dir, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        raise RuntimeError(f"Falha na compilação com {name} (exit {result.returncode}).")
    pdf_path = build_dir / "main.pdf"
    if not pdf_path.exists():
        raise RuntimeError(f"{name} retornou sucesso mas main.pdf não foi encontrado.")
    return pdf_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=REPO_ROOT / "data" / "example")
    parser.add_argument("--schema", type=Path, default=REPO_ROOT / "schema")
    parser.add_argument(
        "--lang", nargs="+", default=list(SUPPORTED_LANGUAGES), choices=SUPPORTED_LANGUAGES
    )
    parser.add_argument("--template", default="academico-padrao")
    parser.add_argument("--output-dir", type=Path, default=REPO_ROOT / "output")
    parser.add_argument("--build-dir", type=Path, default=REPO_ROOT / "build")
    parser.add_argument(
        "--skip-pdf",
        action="store_true",
        help="Gera apenas o .tex, JSON e TXT, sem invocar o compilador LaTeX.",
    )
    args = parser.parse_args(argv)

    print("1/4 Validando dados contra os schemas...")
    errors = validate_all(args.data, args.schema)
    if errors:
        print("Validação falhou:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1
    print("    OK.")

    data = load_data(args.data)
    template_dir = REPO_ROOT / "templates" / args.template
    if not template_dir.exists():
        print(f"Template não encontrado: {template_dir}", file=sys.stderr)
        return 1

    args.output_dir.mkdir(parents=True, exist_ok=True)

    print("2/4 Exportando JSON Resume + TXT...")
    export_json_resume(data, args.output_dir / "cv.json")
    export_txt(data, args.output_dir / "cv.txt")
    print("    OK.")

    for lang in args.lang:
        print(f"3/4 Gerando .tex ({lang})...")
        build_dir = args.build_dir / lang
        render_tex(template_dir, build_dir, data, lang)
        print(f"    OK: {build_dir / 'main.tex'}")

        if args.skip_pdf:
            continue

        print(f"4/4 Compilando PDF ({lang})...")
        pdf_path = compile_pdf(build_dir)
        dest = args.output_dir / f"cv-{lang}.pdf"
        shutil.copy(pdf_path, dest)
        print(f"    OK: {dest}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
