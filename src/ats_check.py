#!/usr/bin/env python3
"""Verificação de "ATS-friendliness" do PDF gerado.

Extrai o texto do PDF (via PyMuPDF) e confere se os dados essenciais do
YAML de origem (nome, email, palavras-chave, títulos de publicações)
aparecem na camada de texto extraída. Isso garante que nada "sumiu" na
compilação (texto virou imagem, ordem de leitura quebrada, etc.) e que o
PDF é de fato legível por parsers de ATS/leitores de tela.

Uso:
    python src/ats_check.py --pdf output/cv-pt.pdf --data data/example --lang pt
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import fitz  # PyMuPDF
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def extract_text(pdf_path: Path) -> str:
    doc = fitz.open(pdf_path)
    try:
        return "\n".join(page.get_text() for page in doc)
    finally:
        doc.close()


def load_yaml(path: Path):
    if not path.exists():
        return None
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def collect_expected_strings(data_dir: Path, lang: str) -> list[str]:
    expected: list[str] = []

    perfil = load_yaml(data_dir / "perfil.yaml") or {}
    for key in ("nome", "email"):
        if perfil.get(key):
            expected.append(perfil[key])
    if perfil.get("titulo", {}).get(lang):
        expected.append(perfil["titulo"][lang])
    for kw in perfil.get("palavras_chave", []) or []:
        expected.append(kw)

    publicacoes = load_yaml(data_dir / "publicacoes.yaml") or []
    for p in publicacoes:
        expected.append(p["titulo"])

    projetos = load_yaml(data_dir / "projetos.yaml") or []
    for p in projetos:
        expected.append(p["titulo"])

    orientacoes = load_yaml(data_dir / "orientacoes.yaml") or []
    for o in orientacoes:
        expected.append(o["aluno"])
        expected.append(o["titulo"])

    premios = load_yaml(data_dir / "premios.yaml") or []
    for p in premios:
        expected.append(p["titulo"])

    return expected


def check(pdf_path: Path, data_dir: Path, lang: str) -> list[str]:
    extracted = normalize(extract_text(pdf_path))
    missing = []
    for expected in collect_expected_strings(data_dir, lang):
        if normalize(expected) not in extracted:
            missing.append(expected)
    return missing


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--data", type=Path, default=REPO_ROOT / "data" / "example")
    parser.add_argument("--lang", default="pt")
    args = parser.parse_args(argv)

    if not args.pdf.exists():
        print(f"PDF não encontrado: {args.pdf}", file=sys.stderr)
        return 1

    missing = check(args.pdf, args.data, args.lang)

    if missing:
        print(f"ATS check FALHOU: {len(missing)} item(ns) do YAML não encontrados no texto extraído do PDF:", file=sys.stderr)
        for item in missing:
            print(f"  - {item!r}", file=sys.stderr)
        return 1

    print(f"ATS check OK: todo o conteúdo esperado foi encontrado na camada de texto de {args.pdf}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
