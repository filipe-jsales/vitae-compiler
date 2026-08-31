# Mantenedores

Este arquivo lista quem revisa e faz merge de Pull Requests neste repositório.

| Nome | GitHub | Área |
|---|---|---|
| Filipe Sales | [@filipe_sales](https://github.com/filipe_sales) | Mantenedor principal |

## O que um mantenedor faz

- Revisa PRs quanto a correção, aderência ao schema e às diretrizes de ATS-friendliness ([docs/ats-optimization.md](docs/ats-optimization.md)).
- Garante que o CI (`build.yml`, `validate-schema.yml`) está verde antes do merge.
- Decide sobre mudanças breaking no schema (major version bump, ver [docs/schema-reference.md](docs/schema-reference.md)).
- Cria releases (tags `vX.Y.Z`), disparando `release.yml`.

## Tornando-se mantenedor

Colaboradores com histórico consistente de PRs de qualidade e reviews úteis podem ser convidados a se tornar mantenedores. Abra uma issue ou entre em contato com um mantenedor atual se tiver interesse.
