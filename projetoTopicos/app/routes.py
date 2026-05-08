import json
from functools import wraps
from flask import (Blueprint, render_template, redirect, url_for,
                   jsonify, request, session, flash)
from .database import Database

main = Blueprint("main", __name__)
db   = Database()

# ── senha admin (em produção use variável de ambiente) ──────────────────
ADMIN_USER     = "admin"
ADMIN_PASSWORD = "mhnet2025"

# ── decorator de proteção ───────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin_logado"):
            return redirect(url_for("main.admin_login"))
        return f(*args, **kwargs)
    return decorated

# ════════════════════════════════════════════════════════════════════════
# PÚBLICO
# ════════════════════════════════════════════════════════════════════════

@main.route("/")
def index():
    categorias = db.listar_categorias()
    return render_template("index.html", categorias=categorias)

@main.route("/categoria/<categoria>")
def subcategorias(categoria):
    subs = db.listar_subcategorias(categoria)
    if not subs:
        return render_template("404.html", msg="Categoria não encontrada"), 404
    return render_template("subcategorias.html", categoria=categoria, subs=subs)

@main.route("/conteudos/<categoria>/<sub>")
def conteudos(categoria, sub):
    dados = db.buscar_conteudos(categoria, sub)
    if not dados:
        return render_template("404.html", msg="Conteúdo não encontrado"), 404
    if len(dados) == 1:
        return redirect(url_for("main.abrir", id=str(dados[0]["_id"])))
    return render_template("conteudos.html", categoria=categoria, sub=sub, dados=dados)

@main.route("/abrir/<id>")
def abrir(id):
    item = db.buscar_por_id(id)
    if not item:
        return render_template("404.html", msg="Conteúdo não encontrado"), 404
    db.incrementar_visualizacao(id)
    tipo = item.get("tipo", "fluxo")
    if tipo == "fluxo":
        return render_template("fluxo.html", item=item)
    elif tipo == "link":
        return redirect(item.get("conteudo_link", "/"))
    elif tipo == "texto":
        return render_template("texto.html", item=item)
    return render_template("404.html", msg="Tipo não suportado"), 400

# ── Pesquisa ────────────────────────────────────────────────────────────
@main.route("/busca")
def busca():
    query     = request.args.get("q", "").strip()
    categoria = request.args.get("cat", "").strip()
    resultados = []
    categorias = db.listar_categorias()
    if query:
        resultados = db.buscar_texto(query, categoria if categoria else None)
    return render_template("busca.html",
        query=query,
        categoria=categoria,
        categorias=categorias,
        resultados=resultados
    )

# ── Importação ──────────────────────────────────────────────────────────
@main.route("/importar", methods=["GET", "POST"])
def importar():
    if request.method == "POST":
        dados = request.get_json(silent=True)
        if not dados:
            return jsonify({"erro": "JSON inválido"}), 400
        limpar = request.args.get("limpar", "false").lower() == "true"
        qtd = db.importar_json(dados, limpar=limpar)
        return jsonify({"importados": qtd})
    return render_template("importar.html")

# ════════════════════════════════════════════════════════════════════════
# ADMIN
# ════════════════════════════════════════════════════════════════════════

@main.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    erro = None
    if request.method == "POST":
        usuario = request.form.get("usuario", "")
        senha   = request.form.get("senha", "")
        if usuario == ADMIN_USER and senha == ADMIN_PASSWORD:
            session["admin_logado"] = True
            return redirect(url_for("main.admin_dashboard"))
        erro = "Usuário ou senha incorretos."
    return render_template("admin/login.html", erro=erro)

@main.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("main.admin_login"))

@main.route("/admin")
@login_required
def admin_dashboard():
    conteudos = db.listar_todos()
    categorias = db.listar_categorias()
    return render_template("admin/dashboard.html",
        conteudos=conteudos, categorias=categorias)

@main.route("/admin/novo", methods=["GET", "POST"])
@login_required
def admin_novo():
    categorias_fixas = ["Suporte Técnico", "Financeiro", "Retenção", "Conteúdos N2"]
    if request.method == "POST":
        doc = _form_para_doc(request.form)
        db.inserir(doc)
        flash("✅ Conteúdo criado com sucesso!", "success")
        return redirect(url_for("main.admin_dashboard"))
    return render_template("admin/form.html",
        item=None, categorias=categorias_fixas, acao="Novo")

@main.route("/admin/editar/<id>", methods=["GET", "POST"])
@login_required
def admin_editar(id):
    categorias_fixas = ["Suporte Técnico", "Financeiro", "Retenção", "Conteúdos N2"]
    item = db.buscar_por_id(id)
    if not item:
        return render_template("404.html", msg="Conteúdo não encontrado"), 404
    if request.method == "POST":
        doc = _form_para_doc(request.form)
        db.atualizar(id, doc)
        flash("✅ Conteúdo atualizado com sucesso!", "success")
        return redirect(url_for("main.admin_dashboard"))
    return render_template("admin/form.html",
        item=item, categorias=categorias_fixas, acao="Editar")

@main.route("/admin/deletar/<id>", methods=["POST"])
@login_required
def admin_deletar(id):
    db.deletar(id)
    flash("🗑️ Conteúdo removido.", "info")
    return redirect(url_for("main.admin_dashboard"))

# ── helper: converte form → documento MongoDB ───────────────────────────
def _form_para_doc(form):
    # Tópicos: campos topico_titulo_N e topico_passos_N
    topicos = []
    i = 0
    while f"topico_titulo_{i}" in form:
        titulo = form.get(f"topico_titulo_{i}", "").strip()
        passos_raw = form.get(f"topico_passos_{i}", "")
        passos = [p.strip() for p in passos_raw.split("\n") if p.strip()]
        if titulo:
            topicos.append({"titulo": titulo, "passos": passos})
        i += 1

    # Material de apoio
    apoio_titulos = form.getlist("apoio_titulo")
    apoio_links   = form.getlist("apoio_link")
    materiais = []
    for t, l in zip(apoio_titulos, apoio_links):
        if t.strip() and l.strip():
            materiais.append({"titulo": t.strip(), "link": l.strip()})

    material_apoio = None
    if len(materiais) == 1:
        material_apoio = materiais[0]
    elif len(materiais) > 1:
        material_apoio = materiais

    doc = {
        "categoria":    form.get("categoria", "").strip(),
        "subcategoria": form.get("subcategoria", "").strip(),
        "titulo":       form.get("titulo", "").strip(),
        "tipo":         form.get("tipo", "fluxo").strip(),
        "descricao":    form.get("descricao", "").strip(),
        "topicos":      topicos,
    }
    if material_apoio:
        doc["material_apoio"] = material_apoio

    return doc
