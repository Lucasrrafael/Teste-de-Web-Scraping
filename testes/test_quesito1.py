import pytest
from quesito1 import baixar_pdf, extrair_e_baixar_pdfs
import os
import requests

# Testa a função baixar_pdf usando mock
def test_baixar_pdf(mocker):
    url_teste = "http://exemplo.com/arquivo.pdf"
    pasta_saida = "teste_pdfs"

    # Mock para requests.get
    mock_response = mocker.Mock()
    mock_response.iter_content = mocker.Mock(return_value=[b"dado1", b"dado2"])
    mock_response.raise_for_status = mocker.Mock()

    mock_get = mocker.patch("quesito1.requests.get", return_value=mock_response)

    # Mock para os.makedirs
    mock_makedirs = mocker.patch("quesito1.os.makedirs")

    # Mock para a função open
    mock_open = mocker.mock_open()
    mocker.patch("builtins.open", mock_open)

    baixar_pdf(url_teste, pasta_saida)

    # Verifica se requests.get foi chamado corretamente
    mock_get.assert_called_with(url_teste, stream=True)
    mock_response.raise_for_status.assert_called_once()

    # Verifica se diretório foi criado corretamente
    mock_makedirs.assert_called_once_with(pasta_saida, exist_ok=True)

    # Verifica se o arquivo foi aberto corretamente
    mock_open.assert_called_once_with(os.path.join(pasta_saida, "arquivo.pdf"), "wb")

    # Verifica se os dados foram escritos corretamente no arquivo
    handle = mock_open()
    handle.write.assert_any_call(b'dado1')
    handle.write.assert_any_call(b'dado2')


# Testa extrair_e_baixar_pdfs com links contendo texto correspondente
def test_extrair_e_baixar_pdfs_com_correspondencias(mocker):
    url_pagina = "http://exemplo.com"
    textos_busca = ["relatório", "2023"]

    html_mock = """
    <html>
        <body>
            <a href="relatorio_anual_2023.pdf">Relatório Anual 2023</a>
            <a href="resumo_financeiro.pdf">Resumo Financeiro</a>
            <a href="outro_documento.pdf">Outro Documento</a>
        </body>
    </html>
    """

    mock_response = mocker.Mock()
    mock_response.text = html_mock
    mock_response.raise_for_status = mocker.Mock()

    mocker.patch("quesito1.requests.get", return_value=mock_response)

    mock_baixar_pdf = mocker.patch("quesito1.baixar_pdf")

    extrair_e_baixar_pdfs(url_pagina, textos_busca)

    # Verifica se baixar_pdf foi chamado para o PDF correto
    mock_baixar_pdf.assert_called_once_with("http://exemplo.com/relatorio_anual_2023.pdf")


# Testa extrair_e_baixar_pdfs sem links correspondentes
def test_extrair_e_baixar_pdfs_sem_correspondencias(mocker, capsys):
    url_pagina = "http://exemplo.com"
    textos_busca = ["inexistente"]

    html_mock = """
    <html>
        <body>
            <a href="relatorio_anual_2023.pdf">Relatório Anual 2023</a>
            <a href="resumo_financeiro.pdf">Resumo Financeiro</a>
        </body>
    </html>
    """

    mock_response = mocker.Mock()
    mock_response.text = html_mock
    mock_response.raise_for_status = mocker.Mock()

    mocker.patch("quesito1.requests.get", return_value=mock_response)

    mock_baixar_pdf = mocker.patch("quesito1.baixar_pdf")

    extrair_e_baixar_pdfs(url_pagina, textos_busca)

    # Verifica que baixar_pdf não foi chamado
    mock_baixar_pdf.assert_not_called()

    # Verifica a mensagem impressa
    captured = capsys.readouterr()
    assert "Nenhum PDF correspondente encontrado." in captured.out


# Testa tratamento de erro ao acessar a página
def test_extrair_e_baixar_pdfs_erro_requisicao(mocker, capsys):
    url_pagina = "http://exemplo.com"
    textos_busca = ["relatório"]

    # Mocka requests.get para lançar RequestException, que é o tratado no código original
    mocker.patch(
        "quesito1.requests.get",
        side_effect=requests.RequestException("Erro de conexão")
    )

    extrair_e_baixar_pdfs(url_pagina, textos_busca)

    captured = capsys.readouterr()
    assert "Erro ao acessar a página http://exemplo.com: Erro de conexão" in captured.out