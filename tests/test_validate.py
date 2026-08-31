import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from validate import validate_all  # noqa: E402


def test_example_data_is_valid():
    errors = validate_all(REPO_ROOT / "data" / "example", REPO_ROOT / "schema")
    assert errors == []


def test_missing_required_field_fails(tmp_path):
    (tmp_path / "perfil.yaml").write_text(
        "nome: 'Sem Email'\n"
        "titulo:\n  pt: 'X'\n  en: 'X'\n"
        "resumo:\n  pt: 'x'\n  en: 'x'\n"
        "palavras_chave: ['x']\n",
        encoding="utf-8",
    )
    errors = validate_all(tmp_path, REPO_ROOT / "schema")
    assert any("email" in e for e in errors)


def test_invalid_publication_year_type_fails(tmp_path):
    (tmp_path / "perfil.yaml").write_text(
        "nome: 'N'\nemail: 'n@example.com'\n"
        "titulo:\n  pt: 'X'\n  en: 'X'\n"
        "resumo:\n  pt: 'x'\n  en: 'x'\n"
        "palavras_chave: ['x']\n",
        encoding="utf-8",
    )
    (tmp_path / "publicacoes.yaml").write_text(
        "- titulo: 'T'\n  autores: ['A']\n  ano: 'não é um número'\n  tipo: 'artigo'\n  veiculo: 'V'\n",
        encoding="utf-8",
    )
    errors = validate_all(tmp_path, REPO_ROOT / "schema")
    assert any("publicacoes" in e for e in errors)
