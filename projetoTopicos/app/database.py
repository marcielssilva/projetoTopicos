import os
from pymongo import MongoClient, TEXT
from bson import ObjectId

MONGO_URI = os.environ.get(
    "MONGO_URI",
    "mongodb+srv://lukasilverio94_db_user:7wf153@topidosespeciais.w7givnv.mongodb.net/?retryWrites=true&w=majority&appName=topidosespeciais"
)

class Database:
    def __init__(self):
        self.client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        self.db     = self.client["suporte_db"]
        self.colecao = self.db["conteudos"]
        self._garantir_indices()

    def _garantir_indices(self):
        try:
            idx_existentes = [i["name"] for i in self.colecao.list_indexes()]
            if "busca_texto" not in idx_existentes:
                self.colecao.create_index([
                    ("titulo",         TEXT),
                    ("descricao",      TEXT),
                    ("topicos.titulo", TEXT),
                    ("topicos.passos", TEXT),
                ], name="busca_texto", default_language="portuguese")
        except Exception as e:
            print(f"[AVISO] Índice de texto: {e}")

    # ── categorias e subcategorias ──────────────────────────────────────
    def listar_categorias(self):
        ordem = ["Suporte Técnico", "Financeiro", "Retenção", "Conteúdos N2"]
        todas = self.colecao.distinct("categoria")
        ordenadas = [c for c in ordem if c in todas]
        ordenadas += [c for c in todas if c not in ordem]
        return ordenadas

    def listar_subcategorias(self, categoria):
        ordem_subs = {
            "Suporte Técnico": [
                "Sem Conexão","Lentidão","Via Rádio","Configuração",
                "Telefonia","Mudança de Endereço","Mudança de Ponto Interno",
                "Visita Técnica","Conteúdos Adicionais"
            ],
            "Financeiro": [
                "Renegociação","Solicitações","Bloqueios",
                "Comprovantes","Desbloqueios","Descontos","Aplicação"
            ],
            "Retenção": ["Acionamento","Ações Iniciais","Boas Práticas","Regra de Ouro"],
            "Conteúdos N2": ["Domínio/E-mail/Site","Benefícios","TI/Plantão"],
        }
        todas = self.colecao.distinct("subcategoria", {"categoria": categoria})
        ref = ordem_subs.get(categoria, [])
        ordenadas = [s for s in ref if s in todas]
        ordenadas += [s for s in todas if s not in ref]
        return ordenadas

    # ── busca ───────────────────────────────────────────────────────────
    def buscar_texto(self, query, categoria=None):
        filtro = {"$text": {"$search": query}}
        if categoria:
            filtro["categoria"] = categoria
        return list(self.colecao.find(
            filtro,
            {"score": {"$meta": "textScore"}}
        ).sort([("score", {"$meta": "textScore"})]).limit(30))

    def buscar_conteudos(self, categoria, subcategoria):
        return list(self.colecao.find({
            "categoria":    categoria,
            "subcategoria": subcategoria,
            "ativo":        {"$ne": False}
        }))

    def buscar_por_id(self, _id):
        return self.colecao.find_one({"_id": ObjectId(_id)})

    def incrementar_visualizacao(self, _id):
        self.colecao.update_one(
            {"_id": ObjectId(_id)},
            {"$inc": {"visualizacoes": 1}}
        )

    # ── CRUD admin ──────────────────────────────────────────────────────
    def listar_todos(self):
        return list(self.colecao.find({}).sort([("categoria", 1), ("subcategoria", 1)]))

    def inserir(self, doc: dict):
        doc.setdefault("visualizacoes", 0)
        doc.setdefault("tipo", "fluxo")
        result = self.colecao.insert_one(doc)
        return str(result.inserted_id)

    def atualizar(self, _id: str, doc: dict):
        doc.pop("_id", None)
        self.colecao.update_one({"_id": ObjectId(_id)}, {"$set": doc})

    def deletar(self, _id: str):
        self.colecao.delete_one({"_id": ObjectId(_id)})

    # ── importação ──────────────────────────────────────────────────────
    def importar_json(self, dados: list, limpar=False):
        if limpar:
            self.colecao.drop()
        if dados:
            self.colecao.insert_many(dados)
        return len(dados)
