# cv-as-code

[![Build](https://github.com/OWNER/cv-as-code/actions/workflows/build.yml/badge.svg)](https://github.com/OWNER/cv-as-code/actions/workflows/build.yml)
[![Validate Schema](https://github.com/OWNER/cv-as-code/actions/workflows/validate-schema.yml/badge.svg)](https://github.com/OWNER/cv-as-code/actions/workflows/validate-schema.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](CHANGELOG.md)

> Substitua `OWNER` nos badges acima pelo namespace real do repositório após o primeiro push.

**Currículo acadêmico como dado versionado: YAML no Git entra, PDF (e JSON, e TXT) compilado sai — legível por humanos e por máquinas.**

## Por que isso existe

Manter um currículo acadêmico atualizado (Lattes, CV internacional, site pessoal) é manual, repetitivo e propenso a inconsistência. E PDFs "bonitos" feitos em Word/Canva costumam ser **ilegíveis para parsers automáticos** — texto em imagem, colunas lidas fora de ordem, sem estrutura semântica — o que hoje prejudica candidatos em processos seletivos e editais que usam triagem por IA.

`cv-as-code` trata o currículo como **dado estruturado versionado**: você edita YAML, o CI valida, compila e publica o PDF — e o PDF resultante é desenhado para ser bem lido tanto por bancas/recrutadores humanos quanto por ATS, parsers Lattes/CNPq e LLMs.

## Quickstart

```bash
git clone https://github.com/OWNER/cv-as-code.git
cd cv-as-code
pip install -r requirements-dev.txt   # requer também tectonic ou latexmk instalado
make build
```

Pronto: `output/cv-pt.pdf`, `output/cv-en.pdf`, `output/cv.json` (JSON Resume) e `output/cv.txt` gerados a partir dos dados de exemplo em `data/example/`.

Para usar seus próprios dados, edite os arquivos em `data/example/` (ou copie a pasta) e rode `make build` de novo. Veja o [guia rápido](docs/guia-rapido.md) para o passo a passo completo, incluindo como rodar sem compilador LaTeX instalado (`--skip-pdf`).

## Estrutura de dados

Um currículo é um conjunto de arquivos YAML em `data/`, cada um validado por um [JSON Schema](schema/) próprio. Exemplo mínimo de `perfil.yaml`:

```yaml
nome: "Maria da Silva"
titulo:
  pt: "Pesquisadora em Ciência da Computação"
  en: "Computer Science Researcher"
email: "maria.silva@example.edu"
resumo:
  pt: "Pesquisadora com foco em processamento de linguagem natural..."
  en: "Researcher focused on natural language processing..."
palavras_chave:
  - "Processamento de Linguagem Natural"
  - "Python"
```

Publicações, projetos, orientações, ensino e prêmios seguem o mesmo padrão em arquivos separados. Veja [docs/schema-reference.md](docs/schema-reference.md) para a referência completa de campos.

## Como funciona a otimização para ATS/IA

O tema padrão gera PDF em coluna única, com texto real selecionável, metadados XMP embutidos (`hyperxmp`), seções com nomenclatura padronizada e uma seção dedicada de palavras-chave — além de exportar em paralelo `cv.json` (formato [JSON Resume](https://jsonresume.org/schema/)) e `cv.txt`. Um script de CI (`src/ats_check.py`) extrai o texto do PDF gerado e confere que nada do YAML original "sumiu" na compilação.

Detalhes completos em [docs/ats-optimization.md](docs/ats-optimization.md).

## Roadmap

- [x] MVP: 1 tema, PT-BR + EN, validação de schema, build reprodutível, CI, export JSON Resume + TXT
- [ ] PDF/UA taggeado por padrão
- [ ] JSON-LD (`schema.org/Person`) embutido no PDF
- [ ] Importação automática via ORCID / DOI (CrossRef) / Lattes
- [ ] Múltiplos temas visuais
- [ ] Interface web para gerar o YAML sem editar texto
- [ ] Assinatura digital / QR code de verificação de autenticidade

## Como contribuir

Contribuições são bem-vindas — veja [CONTRIBUTING.md](CONTRIBUTING.md) para ambiente de desenvolvimento, convenção de commits e processo de review. Este projeto segue o [Código de Conduta](CODE_OF_CONDUCT.md).

## Licença

[MIT](LICENSE)
