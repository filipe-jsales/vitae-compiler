# examples/

Este diretório é o destino sugerido para um PDF de exemplo (`output-exemplo.pdf`) gerado a partir de `data/example/`, para ser referenciado no README/screenshots.

Nenhum compilador LaTeX estava disponível no ambiente usado para montar este MVP, então o PDF não foi gerado automaticamente aqui. Para gerar e publicar o exemplo:

```bash
make build
cp output/cv-pt.pdf examples/output-exemplo.pdf
```

O workflow `.github/workflows/build.yml` já compila e publica `cv-pt.pdf`/`cv-en.pdf` como artefato de CI a cada push — é a fonte de verdade para verificar que o build funciona, independentemente deste diretório.
