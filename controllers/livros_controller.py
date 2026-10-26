"""Controller de livros: recebe a ação do usuário, consulta o Model e escolhe a View."""
from flask import Blueprint, abort, current_app, render_template, request, session

from models import NaoEncontrado

livros_bp = Blueprint("livros", __name__)


def _catalogo():
    return current_app.config["CATALOGO"]


@livros_bp.get("/")
def buscar():
    termo = request.args.get("q", "")
    livros = _catalogo().buscar(termo)
    return render_template("livros/busca.html", livros=livros, termo=termo)


@livros_bp.get("/livros/<isbn>")
def detalhe(isbn):
    try:
        livro = _catalogo().obter_livro(isbn)
        lojas = _catalogo().disponibilidade(isbn, session.get("loja_favorita"))
    except NaoEncontrado as erro:
        abort(404, description=str(erro))
    return render_template("livros/detalhe.html", livro=livro, lojas=lojas)
