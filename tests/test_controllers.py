"""Testes dos Controllers e Views: requisições HTTP e HTML renderizado."""
import pytest

from app import create_app


@pytest.fixture
def cliente():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_pagina_inicial_lista_livros(cliente):
    html = cliente.get("/").get_data(as_text=True)
    assert "Dom Casmurro" in html and "R$ 29,90" in html


def test_busca_filtra_resultados(cliente):
    html = cliente.get("/?q=clarice").get_data(as_text=True)
    assert "A Hora da Estrela" in html and "Dom Casmurro" not in html


def test_busca_sem_resultado(cliente):
    assert "Nenhum livro encontrado" in cliente.get("/?q=harry").get_data(as_text=True)


def test_detalhe_mostra_estoque(cliente):
    html = cliente.get("/livros/9788535902775").get_data(as_text=True)
    assert "3 em estoque" in html and "Esgotado" in html


def test_livro_inexistente_retorna_404(cliente):
    resposta = cliente.get("/livros/000")
    assert resposta.status_code == 404
    assert "Livro não encontrado" in resposta.get_data(as_text=True)


def test_detalhe_da_loja(cliente):
    html = cliente.get("/lojas/pinheiros").get_data(as_text=True)
    assert "Rua dos Pinheiros, 500" in html and "Todos os dias, 9h às 21h" in html


def test_loja_inexistente_retorna_404(cliente):
    assert cliente.get("/lojas/centro").status_code == 404


def test_favoritar_coloca_loja_em_primeiro(cliente):
    cliente.post("/lojas/pinheiros/favorita")
    html = cliente.get("/livros/9788501114775").get_data(as_text=True)
    assert html.index("Livraria Pinheiros") < html.index("Livraria Paulista")
    assert "Sua loja favorita" in html


def test_favoritar_loja_inexistente(cliente):
    assert cliente.post("/lojas/centro/favorita").status_code == 404
