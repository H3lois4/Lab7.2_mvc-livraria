"""Dados iniciais do MVP (substituível por um banco de dados)."""
from .catalogo import Catalogo
from .entidades import Livro, Loja


def criar_catalogo_exemplo():
    catalogo = Catalogo()
    catalogo.adicionar_loja(Loja("paulista", "Livraria Paulista",
                                 "Av. Paulista, 1000 – São Paulo",
                                 "Seg a sáb, 10h às 22h; dom, 12h às 20h"))
    catalogo.adicionar_loja(Loja("pinheiros", "Livraria Pinheiros",
                                 "Rua dos Pinheiros, 500 – São Paulo",
                                 "Todos os dias, 9h às 21h"))
    for livro in [
        Livro("9788535902775", "Dom Casmurro", "Machado de Assis", 29.90,
              {"paulista": 3, "pinheiros": 0}),
        Livro("9788571641149", "Memórias Póstumas de Brás Cubas", "Machado de Assis", 34.50,
              {"paulista": 0}),
        Livro("9788535914641", "Grande Sertão: Veredas", "João Guimarães Rosa", 89.00,
              {"pinheiros": 2}),
        Livro("9788501114775", "A Hora da Estrela", "Clarice Lispector", 39.90,
              {"paulista": 1, "pinheiros": 5}),
    ]:
        catalogo.adicionar_livro(livro)
    return catalogo
