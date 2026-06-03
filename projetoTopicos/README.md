# 📡 MHNET – Manual do Atendimento

Sistema de fluxo de atendimento técnico com Flask + MongoDB.

---

## ▶️ Como rodar

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Iniciar o MongoDB
Certifique-se que o MongoDB está rodando em `localhost:27017`.

### 3. Popular o banco de dados
```bash
python seed.py           # adiciona os dados
python seed.py --limpar  # apaga tudo e reimporta do zero
```

### 4. Rodar o servidor
```bash
python run.py
```

Acesse: http://localhost:5000

---

## 📁 Estrutura

```
projetoTopicos/
├── app/
│   ├── __init__.py
│   ├── database.py        # conexão e queries MongoDB
│   ├── routes.py          # rotas Flask
│   └── templates/
│       ├── base.html      # layout base + sidebar de navegação
│       ├── index.html     # página inicial
│       ├── subcategorias.html
│       ├── conteudos.html
│       ├── fluxo.html     # exibe fluxo com tópicos e passos
│       ├── texto.html
│       ├── importar.html  # interface web para importar JSON
│       └── 404.html
├── DADOS2.json            # dados de exemplo para seed
├── seed.py                # script de importação
├── run.py
└── requirements.txt
```

---

## 🗄️ Estrutura do documento no MongoDB

```json
{
  "categoria": "Suporte Técnico",
  "subcategoria": "Sem Conexão",
  "titulo": "📡 Sem Conexão",
  "tipo": "fluxo",
  "descricao": "Descrição resumida do fluxo.",
  "topicos": [
    {
      "titulo": "Nome do tópico",
      "passos": ["Passo 1", "Passo 2"]
    }
  ],
  "material_apoio": {
    "titulo": "🔗 Nome do Material",
    "link": "https://..."
  },
  "visualizacoes": 0
}
```

> `material_apoio` pode ser um **objeto único** ou uma **lista de objetos** (múltiplos links).

---

## 🌐 Rotas

| Rota | Descrição |
|------|-----------|
| `/` | Página inicial |
| `/categoria/<cat>` | Lista subcategorias |
| `/conteudos/<cat>/<sub>` | Lista conteúdos |
| `/abrir/<id>` | Abre um fluxo |
| `/importar` | Interface para importar JSON |
