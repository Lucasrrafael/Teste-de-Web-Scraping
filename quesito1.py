"""
Uso:
    python quesito1.py https://exemplo.com "Anexo X" "Anexo Y"

Exemplo:
    python quesito1.py https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos "Anexo I" "Anexo II"

Autor: Lucas Rafael Dias e Dias
Data: 24/03/2025
"""

import requests
from bs4 import BeautifulSoup # type: ignore
import os
import sys
import zipfile
import shutil
from urllib.parse import urljoin


def baixar_pdf(url, pasta_saida="arquivos_pdf"):
    
    try:
        
        response = requests.get(url, stream=True)
        response.raise_for_status()  

        
        nome_arquivo_local = url.split("/")[-1]

        
        if not nome_arquivo_local.lower().endswith(".pdf"):
            nome_arquivo_local += ".pdf"

        
        os.makedirs(pasta_saida, exist_ok=True)
        caminho_arquivo = os.path.join(pasta_saida, nome_arquivo_local)

        
        with open(caminho_arquivo, "wb") as arquivo:
            for bloco in response.iter_content(chunk_size=1024):
                if bloco:
                    arquivo.write(bloco)

        print(f"Arquivo baixado: {nome_arquivo_local}")
    except Exception as erro:
        print(f"Erro ao baixar {url}: {erro}")


def extrair_e_baixar_pdfs(url_pagina, textos_busca):
    
    try:
        
        response = requests.get(url_pagina)
        response.raise_for_status()
    except requests.RequestException as erro:
        print(f"Erro ao acessar a página {url_pagina}: {erro}")
        return

    
    sopa = BeautifulSoup(response.text, "html.parser")

    
    links = sopa.find_all("a", href=True)
    links_correspondentes = []

    
    for link in links:
        href = link["href"]
        texto_link = link.get_text().lower()

        
        url_completa = urljoin(url_pagina, href)

        
        if href.lower().endswith(".pdf"):
            for texto_busca in textos_busca:
                if texto_busca.lower() in texto_link:
                    links_correspondentes.append(url_completa)
                    break  

    
    if not links_correspondentes:
        print("Nenhum PDF correspondente encontrado.")
        return

    
    print(
        f"Foram encontrados {len(links_correspondentes)} PDF(s) correspondente(s)."
    )
    for link_pdf in links_correspondentes:
        baixar_pdf(link_pdf)


if __name__ == "__main__":
    
    if len(sys.argv) < 3:
        print(
            "Comando inválido. Uso: python quesito1.py <url_da_pagina_web> <texto_busca1> [texto_busca2] [texto_busca3] ..."
        )
        sys.exit(1)

    
    url_pagina_web = sys.argv[1]  
    textos_busca = sys.argv[2:]  

    
    extrair_e_baixar_pdfs(url_pagina_web, textos_busca)

    
    if not os.path.exists("arquivos_pdf"):
        print("Erro: O arquivo PDF não foi baixado corretamente.")
    else:
        print("Arquivo PDF baixado com sucesso.")
    
    
    if os.path.exists("arquivos_pdf"):
        with zipfile.ZipFile("arquivos_pdf.zip", "w") as zipf:
            for file in os.listdir("arquivos_pdf"):
                zipf.write(os.path.join("arquivos_pdf", file), file)
        print("Arquivos PDF compactados com sucesso.")
    else:
        print("Erro: O arquivo PDF não foi baixado corretamente.")
    
    
    if os.path.exists("arquivos_pdf"):
        shutil.rmtree("arquivos_pdf")
        print("Pasta de arquivos PDF excluída com sucesso.")
    else:
        print("Erro: A pasta de arquivos PDF não foi encontrada.")
