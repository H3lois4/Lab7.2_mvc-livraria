"""Entidades do domínio da livraria."""
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Loja:
    id: str
    nome: str
    endereco: str
    horario: str


@dataclass
class Livro:
    isbn: str
    titulo: str
    autor: str
    preco: float
    estoque: dict = field(default_factory=dict)  # {loja_id: quantidade}

    @property
    def preco_formatado(self):
        """Preço no formato brasileiro, ex.: R$ 1.089,00."""
        texto = f"{self.preco:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return f"R$ {texto}"

    def disponivel_em(self, loja_id):
        return self.estoque.get(loja_id, 0) > 0
