# Web Scraping de PDFs

Este projeto contém um script Python para extrair e baixar automaticamente arquivos PDF de uma página web, filtrando por textos específicos fornecidos pelo usuário.

## Requisitos

- Python 3.x
- pip (gerenciador de pacotes Python)

## Instalação

1. Clone este repositório:
```bash
git clone <url-do-repositorio>
cd VagaEstagio
```

2. Instale as dependências necessárias usando o arquivo requirements.txt:
```bash
pip install -r requirements.txt
```

## Uso do Script

O script `quesito1.py` permite baixar PDFs de uma página web que correspondam a determinados critérios de texto.

### Sintaxe

```bash
python quesito1.py <url_da_pagina_web> <texto_busca1> [texto_busca2] [texto_busca3] ...
```

### Exemplo

```bash
python quesito1.py https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos "Anexo I" "Anexo II"
```

### Parâmetros

- `url_da_pagina_web`: URL completa da página web onde os PDFs serão procurados
- `texto_busca1`, `texto_busca2`, etc.: Textos para filtrar os links dos PDFs

### Funcionalidades

- O script cria temporariamente uma pasta chamada `arquivos_pdf` para armazenar os downloads
- Baixa apenas PDFs cujos links contenham pelo menos um dos textos de busca fornecidos
- Trata erros de conexão e URLs inválidas
- Evita duplicidade de downloads

## Testes

O projeto inclui testes unitários para verificar o funcionamento correto das funcionalidades principais.

### Executando os Testes

Para executar os testes, utilize o pytest:

```bash
pytest testes/test_quesito1.py -v
```

### Cobertura dos Testes

Os testes cobrem os seguintes cenários:
- Download de PDFs
- Extração de links PDF de uma página web
- Filtragem de PDFs por texto
- Tratamento de erros de conexão
- Casos sem correspondências

## Estrutura do Projeto

```
VagaEstagio/
├── quesito1.py           # Script principal
├── requirements.txt      # Dependências do projeto
└── testes/
    └── test_quesito1.py  # Testes unitários
```

## Dependências Principais

- beautifulsoup4: Para análise de HTML
- requests: Para requisições HTTP
- pytest: Para execução dos testes
- pytest-mock: Para mock de funções nos testes

## Tratamento de Erros

O script inclui tratamento para:
- Erros de conexão com a página web
- URLs inválidas
- Falhas no download de arquivos
- Diretórios inexistentes
- Criação de .zip
