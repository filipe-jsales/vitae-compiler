#!/usr/bin/env python3
"""Exporta os dados do currículo em formato JSON Resume (cv.json) e texto
plano (cv.txt), para consumo por sistemas de triagem/ATS que preferem dados
estruturados a PDF.

Especificação do JSON Resume: https://jsonresume.org/schema/

Por simplicidade, o MVP exporta no idioma "pt" como idioma primário do
JSON/TXT (o PDF é gerado nos dois idiomas). Exportação multi-idioma do JSON
é um item de roadmap — ver docs/guia-rapido.md.
"""
from __future__ import annotations

import json
from pathlib import Path

PRIMARY_LANG = "pt"


def _basics(perfil: dict) -> dict:
    profiles = []
    if perfil.get("github"):
        profiles.append({"network": "GitHub", "username": perfil["github"], "url": f"https://github.com/{perfil['github']}"})
    if perfil.get("linkedin"):
        profiles.append({"network": "LinkedIn", "username": perfil["linkedin"], "url": f"https://linkedin.com/in/{perfil['linkedin']}"})
    if perfil.get("orcid"):
        profiles.append({"network": "ORCID", "username": perfil["orcid"], "url": f"https://orcid.org/{perfil['orcid']}"})

    return {
        "name": perfil.get("nome", ""),
        "label": perfil.get("titulo", {}).get(PRIMARY_LANG, ""),
        "email": perfil.get("email", ""),
        "phone": perfil.get("telefone", ""),
        "url": perfil.get("site", ""),
        "summary": perfil.get("resumo", {}).get(PRIMARY_LANG, ""),
        "location": {"address": perfil.get("localizacao", "")},
        "profiles": profiles,
    }


def _publications(publicacoes: list) -> list:
    return [
        {
            "name": p["titulo"],
            "publisher": p.get("veiculo", ""),
            "releaseDate": str(p.get("ano", "")),
            "url": p.get("url") or (f"https://doi.org/{p['doi']}" if p.get("doi") else ""),
            "summary": ", ".join(p.get("autores", [])),
        }
        for p in publicacoes
    ]


def _projects(projetos: list) -> list:
    return [
        {
            "name": p["titulo"],
            "description": p.get("descricao", {}).get(PRIMARY_LANG, ""),
            "startDate": str(p.get("ano_inicio", "")),
            "endDate": str(p.get("ano_fim") or ""),
            "url": p.get("url", ""),
            "roles": [p["papel"]] if p.get("papel") else [],
        }
        for p in projetos
    ]


def _education_from_orientacoes(orientacoes: list) -> list:
    # JSON Resume não tem um bloco nativo de "orientações"; mapeamos para
    # "education" com campo "studyType" descrevendo o tipo de orientação,
    # que é a aproximação mais próxima no schema padrão.
    return [
        {
            "institution": o.get("instituicao", ""),
            "studyType": o["tipo"],
            "area": o["titulo"],
            "startDate": str(o.get("ano_inicio", "")),
            "endDate": str(o.get("ano_fim") or ""),
        }
        for o in orientacoes
    ]


def _skills(perfil: dict) -> list:
    return [{"name": kw} for kw in perfil.get("palavras_chave", [])]


def _awards(premios: list) -> list:
    return [
        {
            "title": p["titulo"],
            "date": str(p.get("ano", "")),
            "awarder": p.get("instituicao", ""),
            "summary": p.get("descricao", ""),
        }
        for p in premios
    ]


def to_json_resume(data: dict) -> dict:
    return {
        "$schema": "https://raw.githubusercontent.com/jsonresume/resume-schema/master/schema.json",
        "basics": _basics(data.get("perfil", {})),
        "publications": _publications(data.get("publicacoes", []) or []),
        "projects": _projects(data.get("projetos", []) or []),
        "education": _education_from_orientacoes(data.get("orientacoes", []) or []),
        "skills": _skills(data.get("perfil", {})),
        "awards": _awards(data.get("premios", []) or []),
        "meta": {
            "generator": "cv-as-code",
            "language": PRIMARY_LANG,
        },
    }


def export_json_resume(data: dict, output_path: Path) -> None:
    resume = to_json_resume(data)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(resume, ensure_ascii=False, indent=2), encoding="utf-8")


def to_plain_text(data: dict) -> str:
    perfil = data.get("perfil", {})
    lines = [
        perfil.get("nome", ""),
        perfil.get("titulo", {}).get(PRIMARY_LANG, ""),
        "",
        f"Email: {perfil.get('email', '')}",
    ]
    if perfil.get("telefone"):
        lines.append(f"Telefone: {perfil['telefone']}")
    if perfil.get("localizacao"):
        lines.append(f"Localização: {perfil['localizacao']}")
    if perfil.get("orcid"):
        lines.append(f"ORCID: {perfil['orcid']}")
    if perfil.get("lattes_id"):
        lines.append(f"Lattes: {perfil['lattes_id']}")

    lines += ["", "RESUMO", perfil.get("resumo", {}).get(PRIMARY_LANG, "")]

    lines += ["", "PALAVRAS-CHAVE", ", ".join(perfil.get("palavras_chave", []))]

    publicacoes = data.get("publicacoes", []) or []
    if publicacoes:
        lines += ["", "PUBLICAÇÕES"]
        for p in sorted(publicacoes, key=lambda x: x["ano"], reverse=True):
            lines.append(f"- {', '.join(p['autores'])} ({p['ano']}). {p['titulo']}. {p['veiculo']}.")

    projetos = data.get("projetos", []) or []
    if projetos:
        lines += ["", "PROJETOS"]
        for p in sorted(projetos, key=lambda x: x["ano_inicio"], reverse=True):
            fim = p.get("ano_fim") or "atual"
            lines.append(f"- {p['titulo']} ({p['ano_inicio']}-{fim}): {p['descricao'][PRIMARY_LANG]}")

    orientacoes = data.get("orientacoes", []) or []
    if orientacoes:
        lines += ["", "ORIENTAÇÕES"]
        for o in sorted(orientacoes, key=lambda x: x["ano_inicio"], reverse=True):
            lines.append(f"- {o['aluno']} ({o['tipo']}): {o['titulo']}")

    ensino = data.get("ensino", []) or []
    if ensino:
        lines += ["", "ENSINO"]
        for e in sorted(ensino, key=lambda x: x["ano_inicio"], reverse=True):
            lines.append(f"- {e['disciplina']} - {e['instituicao']}")

    premios = data.get("premios", []) or []
    if premios:
        lines += ["", "PRÊMIOS"]
        for p in sorted(premios, key=lambda x: x["ano"], reverse=True):
            lines.append(f"- {p['titulo']} - {p['instituicao']} ({p['ano']})")

    return "\n".join(lines) + "\n"


def export_txt(data: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(to_plain_text(data), encoding="utf-8")


if __name__ == "__main__":
    import argparse

    import yaml

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path(__file__).resolve().parent.parent / "data" / "example")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent.parent / "output")
    args = parser.parse_args()

    datasets = ["perfil", "publicacoes", "projetos", "orientacoes", "ensino", "premios"]
    loaded = {}
    for name in datasets:
        path = args.data / f"{name}.yaml"
        loaded[name] = yaml.safe_load(path.read_text(encoding="utf-8")) if path.exists() else ([] if name != "perfil" else {})

    export_json_resume(loaded, args.output_dir / "cv.json")
    export_txt(loaded, args.output_dir / "cv.txt")
    print(f"Exportado: {args.output_dir / 'cv.json'} e {args.output_dir / 'cv.txt'}")
