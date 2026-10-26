"""Model: dados e regras de negócio do MVP. Não conhece Flask nem HTML."""
import unicodedata


class NaoEncontrado(Exception):
    pass


def _normalizar(texto):
    sem_acentos = unicodedata.normalize("NFKD", texto or "")
    return "".join(c for c in sem_acentos if not unicodedata.combining(c)).casefold().strip()


class Catalogo:
    def __init__(self):
        self._livros = {}
        self._lojas = {}

    # ----- cadastro -----
    def adicionar_loja(self, loja):
        self._lojas[loja.id] = loja

    def adicionar_livro(self, livro):
        self._livros[livro.isbn] = livro

    # ----- lojas (horário e endereço) -----
    def listar_lojas(self):
        return sorted(self._lojas.values(), key=lambda loja: loja.nome)

    def obter_loja(self, loja_id):
        loja = self._lojas.get(loja_id)
        if loja is None:
            raise NaoEncontrado("Loja não encontrada")
        return loja

    def loja_existe(self, loja_id):
        return loja_id in self._lojas

    # ----- livros (busca, estoque e preço) -----
    def buscar(self, termo=""):
        """Busca por trecho do título ou do autor, ignorando maiúsculas e acentos."""
        termo = _normalizar(termo)
        encontrados = [
            livro for livro in self._livros.values()
            if termo in _normalizar(livro.titulo) or termo in _normalizar(livro.autor)
        ]
        return sorted(encontrados, key=lambda livro: _normalizar(livro.titulo))

    def obter_livro(self, isbn):
        livro = self._livros.get(isbn)
        if livro is None:
            raise NaoEncontrado("Livro não encontrado")
        return livro

    def disponibilidade(self, isbn, loja_favorita=None):
        """Lojas que trabalham com o livro: a favorita primeiro, depois ordem alfabética."""
        livro = self.obter_livro(isbn)
        lojas = [self._lojas[loja_id] for loja_id in livro.estoque if loja_id in self._lojas]
        lojas.sort(key=lambda loja: (loja.id != loja_favorita, loja.nome))
        return [
            {
                "loja": loja,
                "quantidade": livro.estoque[loja.id],
                "disponivel": livro.disponivel_em(loja.id),
                "favorita": loja.id == loja_favorita,
            }
            for loja in lojas
        ]
