#!/usr/bin/env python3
"""Valida os arquivos data/*.yaml contra os JSON Schemas em schema/.

Uso:
    python src/validate.py [--data DATA_DIR] [--schema SCHEMA_DIR]

Sai com código != 0 e imprime todos os erros encontrados se qualquer
arquivo estiver ausente, malformado ou não conforme ao schema.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import jsonschema
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

# Mapeia arquivo de dados -> schema. "perfil" é objeto único; os demais são
# listas (podem ser omitidos/vazios sem invalidar o build).
DATASETS = {
    "perfil": {"schema": "perfil.schema.json", "required": True},
    "publicacoes": {"schema": "publicacoes.schema.json", "required": False},
    "projetos": {"schema": "projetos.schema.json", "required": False},
    "orientacoes": {"schema": "orientacoes.schema.json", "required": False},
    "ensino": {"schema": "ensino.schema.json", "required": False},
    "premios": {"schema": "premios.schema.json", "required": False},
}


class ValidationFailure(Exception):
    pass


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def validate_dataset(name: str, data_dir: Path, schema_dir: Path) -> list[str]:
    errors: list[str] = []
    cfg = DATASETS[name]
    data_path = data_dir / f"{name}.yaml"
    schema_path = schema_dir / cfg["schema"]

    if not data_path.exists():
        if cfg["required"]:
            errors.append(f"[{name}] arquivo obrigatório ausente: {data_path}")
        return errors

    try:
        data = load_yaml(data_path)
    except yaml.YAMLError as exc:
        errors.append(f"[{name}] YAML inválido em {data_path}: {exc}")
        return errors

    if data is None:
        data = [] if not cfg["required"] else {}

    schema = load_yaml(schema_path) if schema_path.suffix in (".yaml", ".yml") else None
    if schema is None:
        import json

        schema = json.loads(schema_path.read_text(encoding="utf-8"))

    validator_cls = jsonschema.validators.validator_for(schema)
    validator_cls.check_schema(schema)
    validator = validator_cls(schema)

    for error in sorted(validator.iter_errors(data), key=str):
        location = "/".join(str(p) for p in error.absolute_path) or "<raiz>"
        errors.append(f"[{name}] {data_path.name}::{location}: {error.message}")

    return errors


def validate_all(data_dir: Path, schema_dir: Path) -> list[str]:
    errors: list[str] = []
    for name in DATASETS:
        errors.extend(validate_dataset(name, data_dir, schema_dir))
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data",
        type=Path,
        default=REPO_ROOT / "data" / "example",
        help="Diretório com os arquivos YAML de dados (padrão: data/example)",
    )
    parser.add_argument(
        "--schema",
        type=Path,
        default=REPO_ROOT / "schema",
        help="Diretório com os JSON Schemas (padrão: schema/)",
    )
    args = parser.parse_args(argv)

    errors = validate_all(args.data, args.schema)

    if errors:
        print(f"Validação falhou com {len(errors)} erro(s):\n", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(f"OK: dados em {args.data} válidos contra os schemas em {args.schema}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
