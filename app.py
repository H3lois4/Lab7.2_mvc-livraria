"""Ponto de entrada: monta a aplicação ligando Model, View e Controller."""
from flask import Flask, render_template

from controllers import livros_bp, lojas_bp
from models import criar_catalogo_exemplo


def create_app(catalogo=None):
    app = Flask(__name__, template_folder="views", static_folder="static")
    app.config["SECRET_KEY"] = "troque-esta-chave"
    app.config["CATALOGO"] = catalogo or criar_catalogo_exemplo()

    app.register_blueprint(livros_bp)
    app.register_blueprint(lojas_bp)

    @app.errorhandler(404)
    def nao_encontrado(erro):
        return render_template("erro.html", mensagem=erro.description), 404

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000, debug=True)
