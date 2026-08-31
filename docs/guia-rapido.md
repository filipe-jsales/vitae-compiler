# Guia rápido

## Pré-requisitos

- Python 3.10+
- Um compilador LaTeX: [Tectonic](https://tectonic-typesetting.github.io/) (recomendado, não exige instalação TeX completa) ou `latexmk` + distribuição TeX (TeX Live/MiKTeX)

## Instalação

```bash
git clone https://github.com/<seu-usuario>/cv-as-code.git
cd cv-as-code
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
```

## Gerando o currículo de exemplo

```bash
make build
# ou, sem Makefile:
python src/build.py --data data/example
```

Isso gera em `output/`:

- `cv-pt.pdf`, `cv-en.pdf` — o currículo em PDF, em português e inglês
- `cv.json` — export no formato [JSON Resume](https://jsonresume.org/schema/)
- `cv.txt` — export em texto puro

## Adicionando uma nova publicação (sem tocar no `.tex`)

1. Abra `data/example/publicacoes.yaml` (ou `data/publicacoes.yaml`, se você já tiver seus próprios dados).
2. Adicione um novo item à lista, seguindo o schema em `schema/publicacoes.schema.json`:

   ```yaml
   - titulo: "Título do novo artigo"
     autores:
       - "Sobrenome, N."
     ano: 2026
     tipo: "artigo"
     veiculo: "Nome do periódico ou conferência"
     doi: "10.xxxx/xxxxx"
   ```

3. Rode `make validate` para conferir que os dados são válidos.
4. Rode `make build` para regenerar o PDF/JSON/TXT.

O mesmo padrão vale para `projetos.yaml`, `orientacoes.yaml`, `ensino.yaml` e `premios.yaml` — cada um tem seu schema correspondente em `schema/`.

## Usando seus próprios dados (em vez do exemplo)

Copie `data/example/` para `data/` e edite os arquivos:

```bash
cp -r data/example data/meu-cv   # ou data/ diretamente
python src/build.py --data data/meu-cv
```

`data/` está no `.gitignore` apenas quanto a arquivos de saída — os YAML de dados reais **devem** ser versionados, é esse o ponto central do projeto. Avalie se seu currículo contém dados que você não quer em um repositório público (telefone pessoal, endereço) antes de versionar.

## Rodando sem compilador LaTeX instalado

Para gerar apenas `.tex` + `cv.json` + `cv.txt` (útil em ambientes sem Tectonic/latexmk):

```bash
python src/build.py --data data/example --skip-pdf
```

## Verificando ATS-friendliness

```bash
make ats-check
```

Isso extrai o texto do PDF gerado e confere que todo o conteúdo do YAML aparece na camada de texto — ver [docs/ats-optimization.md](ats-optimization.md).
