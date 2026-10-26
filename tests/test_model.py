"""Testes do Model: regras de negócio, sem Flask."""
import pytest

from models import NaoEncontrado, criar_catalogo_exemplo

DOM_CASMURRO = "9788535902775"
HORA_ESTRELA = "9788501114775"


@pytest.fixture
def catalogo():
    return criar_catalogo_exemplo()


def test_busca_por_titulo_ignora_acentos(catalogo):
    assert [l.titulo for l in catalogo.buscar("memorias postumas")] == ["Memórias Póstumas de Brás Cubas"]


def test_busca_por_autor(catalogo):
    assert [l.titulo for l in catalogo.buscar("MACHADO")] == ["Dom Casmurro", "Memórias Póstumas de Brás Cubas"]


def test_busca_vazia_retorna_tudo_ordenado(catalogo):
    titulos = [l.titulo for l in catalogo.buscar("")]
    assert len(titulos) == 4 and titulos == sorted(titulos)


def test_disponibilidade_por_loja(catalogo):
    itens = {i["loja"].id: i for i in catalogo.disponibilidade(DOM_CASMURRO)}
    assert itens["paulista"]["disponivel"] and itens["paulista"]["quantidade"] == 3
    assert not itens["pinheiros"]["disponivel"]


def test_preco_formatado(catalogo):
    assert catalogo.obter_livro(DOM_CASMURRO).preco_formatado == "R$ 29,90"


def test_sem_favorita_ordem_alfabetica(catalogo):
    assert catalogo.disponibilidade(HORA_ESTRELA)[0]["loja"].id == "paulista"


def test_favorita_aparece_primeiro(catalogo):
    itens = catalogo.disponibilidade(HORA_ESTRELA, loja_favorita="pinheiros")
    assert itens[0]["loja"].id == "pinheiros" and itens[0]["favorita"]


def test_horario_e_endereco(catalogo):
    loja = catalogo.obter_loja("paulista")
    assert loja.endereco == "Av. Paulista, 1000 – São Paulo"
    assert loja.horario == "Seg a sáb, 10h às 22h; dom, 12h às 20h"


def test_loja_inexistente(catalogo):
    with pytest.raises(NaoEncontrado, match="Loja não encontrada"):
        catalogo.obter_loja("centro")


def test_livro_inexistente(catalogo):
    with pytest.raises(NaoEncontrado, match="Livro não encontrado"):
        catalogo.disponibilidade("000")
