# Contribuindo com o cv-as-code

Obrigado por considerar contribuir! Este documento cobre ambiente de desenvolvimento, convenções e o processo de review.

## Ambiente de desenvolvimento

Requisitos:

- Python 3.10+
- Um compilador LaTeX: [Tectonic](https://tectonic-typesetting.github.io/) (recomendado) ou `latexmk` + TeX Live/MiKTeX

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
pre-commit install
```

## Convenção de commits

Este projeto usa [Conventional Commits](https://www.conventionalcommits.org/), já que o CI e o `CHANGELOG.md` dependem de mensagens padronizadas:

- `feat: ...` — nova funcionalidade
- `fix: ...` — correção de bug
- `docs: ...` — documentação
- `chore: ...` — manutenção (deps, CI, etc.)
- `refactor: ...` — mudança de código sem alterar comportamento
- `test: ...` — testes

Mudanças que quebram o schema de dados (campo obrigatório novo, remoção/renomeação, mudança de tipo) devem usar `feat!:` ou incluir `BREAKING CHANGE:` no corpo do commit.

## Rodando testes e validação localmente antes do PR

```bash
make validate        # valida data/example contra os schemas
make build            # gera o PDF + JSON + TXT completos
make build-skip-pdf   # gera .tex + JSON + TXT sem precisar de LaTeX instalado
make ats-check        # confere que o texto extraído do PDF bate com o YAML
make test             # roda a suíte pytest
```

Ou individualmente:

```bash
python src/validate.py --data data/example
python src/build.py --data data/example --skip-pdf
pytest -q
```

## Propondo um novo template/tema

Templates ficam em `templates/<nome-do-tema>/`, seguindo a mesma estrutura do tema `academico-padrao` (`main.tex.j2`, `secoes/*.tex.j2`, `theme.sty`). Um novo tema deve:

1. Consumir o mesmo conjunto de dados (`perfil`, `publicacoes`, `projetos`, `orientacoes`, `ensino`, `premios`) sem exigir mudanças no schema.
2. Manter os princípios de ATS-friendliness descritos em [docs/ats-optimization.md](docs/ats-optimization.md) (texto real, ordem de leitura linear, seções nomeadas de forma convencional).
3. Compilar com `python src/build.py --template <nome-do-tema>`.

## Processo de review e branch strategy

- Trunk-based: branches curtas a partir de `main`, PRs pequenos e focados.
- Todo PR precisa passar no CI (`build.yml`, `validate-schema.yml`) antes de merge.
- Pelo menos uma aprovação de um mantenedor (ver seção de governança no README/[MAINTAINERS.md](MAINTAINERS.md)).
- Squash merge preferido, com a mensagem final seguindo Conventional Commits.

## Código de conduta

Ao contribuir, você concorda em seguir o [Código de Conduta](CODE_OF_CONDUCT.md) do projeto.
