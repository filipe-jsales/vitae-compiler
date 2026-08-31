# Otimização para ATS, parsers acadêmicos e LLMs

O diferencial do `cv-as-code` é gerar um PDF que é ao mesmo tempo apresentável para humanos e **corretamente interpretável por máquina**. Esta página documenta as técnicas usadas e seu status de implementação no MVP.

## 1. Texto real, nunca imagem

Todo o conteúdo é composto como texto LaTeX nativo (`\VAR{...}` injetado pelo Jinja2), nunca como figura ou tabela rasterizada. Isso é garantido "de graça" pelo LaTeX, mas o tema `academico-padrao` evita explicitamente elementos que costumam virar imagem em outros geradores de currículo (ícones bitmap, fundos gráficos complexos).

**Status:** implementado.

## 2. Ordem de leitura linear

O tema usa layout de **uma coluna**, sem `multicols`/tabelas para o corpo do texto. Currículos em duas colunas são a causa mais comum de texto lido fora de ordem por parsers de ATS (o extrator de texto costuma ler da esquerda para a direita, linha a linha, ignorando os limites de coluna).

**Status:** implementado (ver `templates/academico-padrao/theme.sty`).

## 3. PDF taggeado (PDF/UA)

O kernel do LaTeX (2022-11+) suporta tagging experimental via `\DocumentMetadata{tagged=true}`, mas o suporte varia entre engines (pdfLaTeX, XeLaTeX, LuaLaTeX) e entre versões do Tectonic. Para manter o build **reprodutível e estável** no MVP, essa flag está **desabilitada por padrão**.

**Status:** roadmap. Para habilitar experimentalmente, adicione `\DocumentMetadata{tagged=true, lang=pt}` como primeira linha de `templates/academico-padrao/main.tex.j2` e teste a compilação com seu compilador local antes de commitar.

## 4. Metadados embutidos (XMP / Dublin Core)

O template usa o pacote `hyperxmp` para embutir `pdfauthor`, `pdftitle`, `pdfsubject`, `pdfkeywords` e `pdflang` como metadados XMP/Dublin Core no PDF final — muitos parsers de ATS e crawlers leem esses campos antes mesmo de extrair o texto do corpo.

**Status:** implementado (ver `\usepackage[...]{hyperxmp}` em `main.tex.j2`).

**Roadmap:** embutir também um bloco JSON-LD (`schema.org/Person`) como anexo do PDF, para consumo direto por LLMs e crawlers que priorizam dados estruturados explícitos.

## 5. Palavras-chave em texto plano visível

A seção "Palavras-chave"/"Keywords" (`perfil.palavras_chave`) é renderizada como texto simples, em uma seção nomeada de forma convencional — não apenas embutida em metadados ou em formatação gráfica. Parsers de ATS tipicamente extraem skills por seção nomeada.

**Status:** implementado.

## 6. Nomenclatura de seções em padrão reconhecível

Os títulos de seção (`Resumo`/`Summary`, `Publicações`/`Publications`, `Projetos`/`Projects`, `Orientações`/`Advising`, `Ensino`/`Teaching`, `Prêmios`/`Awards`) seguem convenções comuns de currículo, evitando nomes "criativos" que confundiriam parsers baseados em heurísticas de seção. Os rótulos ficam centralizados em `src/labels.py`.

**Status:** implementado.

## 7. Exportação paralela em JSON Resume e TXT

Todo `build` gera, além do PDF:

- `output/cv.json` — no formato aberto [JSON Resume](https://jsonresume.org/schema/), cada vez mais aceito diretamente por plataformas de triagem.
- `output/cv.txt` — texto puro, para sistemas que só aceitam upload de texto.

**Status:** implementado (ver `src/export_json.py`). Limitação atual: o JSON/TXT são exportados no idioma primário (`pt`); exportação multi-idioma do JSON é item de roadmap.

## 8. Validação automatizada de "ATS-friendliness"

`src/ats_check.py` extrai o texto do PDF gerado (via [PyMuPDF](https://pymupdf.readthedocs.io/)) e confere que cada campo relevante do YAML de origem (nome, email, palavras-chave, títulos de publicações/projetos, nomes de orientandos, títulos de prêmios) aparece na camada de texto extraída. Isso pega regressões onde a compilação "engole" conteúdo — por exemplo, um caractere especial mal escapado que quebra um `\item`.

Rodar localmente:

```bash
make ats-check
```

O workflow `.github/workflows/build.yml` roda essa checagem em todo push/PR.

**Status:** implementado.

## Resumo do status

| Técnica | Status |
|---|---|
| Texto real (não imagem) | ✅ Implementado |
| Layout de coluna única / ordem linear | ✅ Implementado |
| Metadados XMP/Dublin Core | ✅ Implementado |
| Palavras-chave em texto plano | ✅ Implementado |
| Nomenclatura de seção padronizada | ✅ Implementado |
| Exportação JSON Resume + TXT | ✅ Implementado |
| Checagem automatizada de extração de texto | ✅ Implementado |
| PDF/UA taggeado | 🔜 Roadmap |
| JSON-LD embutido (schema.org) | 🔜 Roadmap |
| JSON Resume multi-idioma | 🔜 Roadmap |
