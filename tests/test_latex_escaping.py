import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from build import escape_tex, load_data, render_tex  # noqa: E402

TEMPLATE_DIR = REPO_ROOT / "templates" / "academico-padrao"


def test_escape_tex_handles_special_characters():
    assert escape_tex("100% & #1_test {a} ~x ^y \\z") == (
        r"100\% \& \#1\_test \{a\} \textasciitilde{}x "
        r"\textasciicircum{}y \textbackslash{}z"
    )


def test_special_characters_in_yaml_survive_into_tex(tmp_path):
    data = load_data(REPO_ROOT / "data" / "example")
    data["perfil"]["nome"] = "Zé & Cia (50% R&D) #1_special"
    render_tex(TEMPLATE_DIR, tmp_path, data, "pt")

    cabecalho = (tmp_path / "secoes" / "cabecalho.tex").read_text(encoding="utf-8")
    assert r"\&" in cabecalho
    assert r"\%" in cabecalho
    assert r"\#" in cabecalho
    assert r"\_" in cabecalho
    # o caractere cru nunca deve aparecer desacompanhado do escape
    assert "50%" not in cabecalho
