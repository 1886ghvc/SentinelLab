# SentinelLab

Laboratório de estudos de cibersegurança com Python.

## Analisador de autenticação SSH

Analisa um arquivo de log e apresenta:

- Total de linhas não vazias.
- Falhas de autenticação por senha.
- Autenticações bem-sucedidas por senha.
- Contagem de falhas por IP.

## Como executar

Na pasta do projeto:

```bash
source .venv/bin/activate
python src/sentinellab/analyzer.py examples/auth.sample
```

O arquivo examples/auth.sample está incluído no repositório.
Nosso exemplo de estudo contém 3 linhas: 2 falhas e 1 sucesso.

## Limitações

Esta versão reconhece as mensagens "Failed password" e
"Accepted password". A contagem de falhas, isoladamente,
não confirma um ataque.

## Teste do aviso

Os arquivos em examples contêm dados fictícios.

```bash
python src/sentinellab/analyzer.py examples/teste-alerta.sample
```

Resultado esperado: 5 falhas, 0 sucessos e um aviso para o IP
192.0.2.10. O limite considera o arquivo inteiro, sem janela de tempo.
