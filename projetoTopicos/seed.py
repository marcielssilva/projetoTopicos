"""
Popula o MongoDB Atlas com os dados do DADOS2.json.

Uso:
    python seed.py              # adiciona sem apagar
    python seed.py --limpar     # apaga tudo e reimporta
"""
import json, sys
from dotenv import load_dotenv
load_dotenv()

from app.database import Database

def main():
    limpar = "--limpar" in sys.argv
    with open("DADOS2.json", "r", encoding="utf-8") as f:
        dados = json.load(f)
    db = Database()
    if limpar:
        print("⚠️  Limpando coleção no Atlas...")
    qtd = db.importar_json(dados, limpar=limpar)
    print(f"✅ {qtd} documento(s) importado(s) para o Atlas!")

if __name__ == "__main__":
    main()
