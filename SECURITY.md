# Política de Segurança

## Versões suportadas

Este projeto está em fase de MVP (versão `0.x`). Apenas a última versão publicada em `main` recebe correções de segurança.

## Reportando uma vulnerabilidade

Se você encontrar uma vulnerabilidade de segurança (por exemplo, um vetor de injeção via dados YAML que permita execução de comandos durante o build, ou um `.tex` gerado que possa levar à execução de código arbitrário via compilador LaTeX), por favor **não abra uma issue pública**.

Em vez disso, reporte de forma privada usando o recurso [GitHub Security Advisories](../../security/advisories/new) deste repositório, ou entre em contato diretamente com um dos mantenedores listados em [MAINTAINERS.md](MAINTAINERS.md).

Inclua:

- Descrição da vulnerabilidade e impacto potencial
- Passos para reproduzir
- Versão/commit afetado

Você pode esperar uma resposta inicial em até 7 dias.

## Escopo

Como o build envolve compilação LaTeX (execução de código de terceiros sobre dados fornecidos pelo usuário), preste atenção especial a:

- Dados YAML que possam injetar comandos LaTeX não escapados nos arquivos `.tex` gerados
- Dependências Python com vulnerabilidades conhecidas (monitoradas via Dependabot)
- Ações do GitHub de terceiros usadas nos workflows de CI
