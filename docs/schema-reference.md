# Referência de schema

Cada arquivo em `data/*.yaml` é validado contra um [JSON Schema](https://json-schema.org/) correspondente em `schema/`. O build (`src/validate.py`, chamado por `src/build.py`) falha se um arquivo não for conforme.

| Arquivo de dados | Schema | Obrigatório | Descrição |
|---|---|---|---|
| `perfil.yaml` | `schema/perfil.schema.json` | Sim | Identificação, contato, resumo e palavras-chave |
| `publicacoes.yaml` | `schema/publicacoes.schema.json` | Não | Artigos, capítulos, livros, anais, preprints |
| `projetos.yaml` | `schema/projetos.schema.json` | Não | Projetos de pesquisa/desenvolvimento |
| `orientacoes.yaml` | `schema/orientacoes.schema.json` | Não | Orientações de IC, TCC, mestrado, doutorado, pós-doc |
| `ensino.yaml` | `schema/ensino.schema.json` | Não | Disciplinas/cursos ministrados |
| `premios.yaml` | `schema/premios.schema.json` | Não | Prêmios e distinções |

Arquivos não obrigatórios podem ser omitidos — a seção correspondente simplesmente não aparece no PDF gerado.

## `perfil.schema.json`

Campos obrigatórios: `nome`, `titulo` (`pt`/`en`), `email`, `resumo` (`pt`/`en`).

Campos opcionais: `telefone`, `localizacao`, `orcid`, `lattes_id`, `site`, `github`, `linkedin`, `afiliacao`, `palavras_chave`.

`palavras_chave` é a seção de skills em texto plano — ver [docs/ats-optimization.md](ats-optimization.md) sobre por que isso importa para triagem automatizada.

## `publicacoes.schema.json`

Lista de objetos. Campos obrigatórios por item: `titulo`, `autores` (lista), `ano`, `tipo` (`artigo`, `capitulo`, `livro`, `anais`, `preprint`, `outro`), `veiculo`. Opcionais: `doi`, `url`, `paginas`, `volume`, `qualis`.

## `projetos.schema.json`

Campos obrigatórios: `titulo`, `descricao` (`pt`/`en`), `ano_inicio`. Opcionais: `papel`, `financiamento`, `ano_fim` (null = em andamento), `url`.

## `orientacoes.schema.json`

Campos obrigatórios: `aluno`, `tipo` (`iniciacao_cientifica`, `tcc`, `mestrado`, `doutorado`, `pos_doutorado`), `titulo`, `ano_inicio`, `situacao` (`em_andamento`, `concluida`). Opcionais: `instituicao`, `ano_fim`.

## `ensino.schema.json`

Campos obrigatórios: `disciplina`, `instituicao`, `ano_inicio`, `nivel` (`graduacao`, `pos_graduacao`, `extensao`). Opcionais: `ano_fim`, `carga_horaria`.

## `premios.schema.json`

Campos obrigatórios: `titulo`, `instituicao`, `ano`. Opcional: `descricao`.

## Versionamento do schema

Mudanças nos schemas seguem versionamento semântico independente do resto do projeto:

- **Patch**: correção de descrição/exemplo, sem mudar validação.
- **Minor**: novo campo opcional.
- **Major (breaking)**: novo campo obrigatório, remoção/renomeação de campo, mudança de tipo. PRs desse tipo devem atualizar `data/example/*.yaml`, `CHANGELOG.md` e, se necessário, os templates `.tex.j2` que consomem o campo.
