"""Controller de lojas: horário, endereço e loja favorita."""
from flask import (Blueprint, abort, current_app, flash, redirect,
                   render_template, request, session, url_for)

from models import NaoEncontrado

lojas_bp = Blueprint("lojas", __name__, url_prefix="/lojas")


def _catalogo():
    return current_app.config["CATALOGO"]


@lojas_bp.get("/")
def listar():
    return render_template("lojas/lista.html", lojas=_catalogo().listar_lojas(),
                           favorita=session.get("loja_favorita"))


@lojas_bp.get("/<loja_id>")
def detalhe(loja_id):
    try:
        loja = _catalogo().obter_loja(loja_id)
    except NaoEncontrado as erro:
        abort(404, description=str(erro))
    return render_template("lojas/detalhe.html", loja=loja,
                           favorita=session.get("loja_favorita"))


@lojas_bp.post("/<loja_id>/favorita")
def favoritar(loja_id):
    if not _catalogo().loja_existe(loja_id):
        abort(404, description="Loja não encontrada")
    session["loja_favorita"] = loja_id
    flash(f"{_catalogo().obter_loja(loja_id).nome} agora é sua loja favorita.")
    return redirect(request.form.get("voltar") or url_for("lojas.listar"))
