from pymongo import MongoClient
from bson import ObjectId

class Database:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["suporte_db"]
        self.colecao = self.db["conteudos"]

    def listar_categorias(self):
        return self.colecao.distinct("hierarquia.0")

    def listar_subcategorias(self, categoria):
        return self.colecao.distinct("hierarquia.1", {"hierarquia.0": categoria})

    def buscar_conteudos(self, categoria, sub):
        return list(self.colecao.find({
            "hierarquia": [categoria, sub],
            "ativo": True
        }))

    def buscar_por_id(self, _id):
        return self.colecao.find_one({"_id": ObjectId(_id)})

    def incrementar_visualizacao(self, _id):
        self.colecao.update_one(
            {"_id": ObjectId(_id)},
            {"$inc": {"visualizacoes": 1}}
        )