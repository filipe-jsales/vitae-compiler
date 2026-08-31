import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from build import load_data, render_tex  # noqa: E402

DATA_DIR = REPO_ROOT / "data" / "example"
TEMPLATE_DIR = REPO_ROOT / "templates" / "academico-padrao"


def test_render_tex_produces_main_and_sections(tmp_path):
    data = load_data(DATA_DIR)
    tex_path = render_tex(TEMPLATE_DIR, tmp_path, data, "pt")

    assert tex_path.exists()
    content = tex_path.read_text(encoding="utf-8")
    assert r"\documentclass" in content

    for section in ("cabecalho", "publicacoes", "projetos", "orientacoes", "ensino", "premios"):
        assert (tmp_path / "secoes" / f"{section}.tex").exists()

    cabecalho = (tmp_path / "secoes" / "cabecalho.tex").read_text(encoding="utf-8")
    assert data["perfil"]["nome"] in cabecalho


def test_render_tex_both_languages_no_jinja_errors(tmp_path):
    data = load_data(DATA_DIR)
    for lang in ("pt", "en"):
        render_tex(TEMPLATE_DIR, tmp_path / lang, data, lang)
        assert (tmp_path / lang / "main.tex").exists()
