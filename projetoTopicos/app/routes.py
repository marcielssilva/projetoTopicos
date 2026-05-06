from flask import Blueprint, render_template, redirect, url_for
from .database import Database

main = Blueprint("main", __name__)
db = Database()


@main.route("/")
def index():
    categorias = db.listar_categorias()
    return render_template("index.html", categorias=categorias)


@main.route("/categoria/<categoria>")
def subcategorias(categoria):
    subs = db.listar_subcategorias(categoria)

    # segurança: se não existir
    if not subs:
        return "Categoria não encontrada", 404

    return render_template("subcategorias.html", categoria=categoria, subs=subs)


@main.route("/conteudos/<categoria>/<sub>")
def conteudos(categoria, sub):
    dados = db.buscar_conteudos(categoria, sub)

    # 🔴 se não tiver nada
    if not dados:
        return "Conteúdo não encontrado", 404

    # 🔥 comportamento igual ao site
    if len(dados) == 1:
        return redirect(url_for("main.abrir", id=str(dados[0]["_id"])))

    return render_template(
        "conteudos.html",
        categoria=categoria,
        sub=sub,
        dados=dados
    )


@main.route("/abrir/<id>")
def abrir(id):
    item = db.buscar_por_id(id)

    # 🔴 segurança
    if not item:
        return "Conteúdo não encontrado", 404

    db.incrementar_visualizacao(id)

    # 🔥 fluxo principal
    if item["tipo"] == "fluxo":
        return render_template("fluxo.html", item=item)

    elif item["tipo"] == "link":
        return redirect(item["conteudo_link"])

    elif item["tipo"] == "texto":
        return render_template("texto.html", item=item)

    return "Tipo não suportado", 400