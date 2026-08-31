import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from export_json import to_json_resume, to_plain_text  # noqa: E402

DATA_DIR = REPO_ROOT / "data" / "example"
DATASETS = ["perfil", "publicacoes", "projetos", "orientacoes", "ensino", "premios"]


def load_example_data():
    data = {}
    for name in DATASETS:
        path = DATA_DIR / f"{name}.yaml"
        data[name] = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data


def test_json_resume_has_required_top_level_keys():
    resume = to_json_resume(load_example_data())
    for key in ("basics", "publications", "projects", "skills", "awards"):
        assert key in resume


def test_json_resume_basics_matches_perfil():
    data = load_example_data()
    resume = to_json_resume(data)
    assert resume["basics"]["name"] == data["perfil"]["nome"]
    assert resume["basics"]["email"] == data["perfil"]["email"]


def test_plain_text_contains_name_and_publication_titles():
    data = load_example_data()
    text = to_plain_text(data)
    assert data["perfil"]["nome"] in text
    for pub in data["publicacoes"]:
        assert pub["titulo"] in text
