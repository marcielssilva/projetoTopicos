# 📡 MHNET — Manual do Atendimento

> Sistema web de fluxos de atendimento técnico desenvolvido para a disciplina de **Tópicos Especiais**.  
> Construído com Flask, MongoDB Atlas e hospedado no Render.

---

## 🖥️ Demonstração

🔗 **[Acesse o sistema online](https://mhnet-atendimento.onrender.com)**  
🔐 **Painel Admin:** `/admin` → usuário `admin`

---

## 📋 Sobre o Projeto

O **MHNET Manual do Atendimento** é uma aplicação que centraliza todos os fluxos e procedimentos de atendimento ao cliente de um provedor de internet, organizados por setor:

| Setor | Conteúdos |
|---|---|
| 🛠️ Suporte Técnico | Sem Conexão, Lentidão, Via Rádio, Configuração, Telefonia, Mudanças, Visita Técnica |
| 💰 Financeiro | Renegociação, Bloqueios, Comprovantes, Desbloqueios, Descontos, Aplicação |
| 🤝 Retenção | Acionamento, Ações Iniciais, Boas Práticas, Regra de Ouro |
| ⭐ Conteúdos N2 | Domínio/E-mail/Site, Benefícios, TI/Plantão |

---

## 🚀 Tecnologias

- **Python 3** + **Flask** — backend e rotas
- **MongoDB Atlas** — banco de dados NoSQL em nuvem
- **Gunicorn** — servidor WSGI para produção
- **Render** — hospedagem do servidor web
- **HTML/CSS/JS** puro — frontend sem frameworks

---

## 📁 Estrutura do Projeto

```
projetoTopicos/
├── app/
│   ├── __init__.py          # Factory da aplicação Flask
│   ├── database.py          # Conexão e queries MongoDB
│   ├── routes.py            # Todas as rotas (público + admin)
│   └── templates/
│       ├── base.html        # Layout base com sidebar e busca
│       ├── index.html       # Página inicial
│       ├── subcategorias.html
│       ├── conteudos.html
│       ├── fluxo.html       # Exibe fluxo com tópicos e passos
│       ├── busca.html       # Pesquisa full-text
│       ├── texto.html
│       ├── importar.html
│       ├── 404.html
│       └── admin/
│           ├── login.html   # Tela de login protegida
│           ├── dashboard.html  # Painel de gestão
│           └── form.html    # Criar / editar conteúdo
├── DADOS2.json              # Dados iniciais para seed
├── seed.py                  # Script de importação para o Atlas
├── run.py                   # Entry point da aplicação
├── requirements.txt
├── render.yaml              # Configuração de deploy no Render
├── .env.example             # Modelo de variáveis de ambiente
└── .gitignore
```

---

## ⚙️ Como Rodar Localmente

### Pré-requisitos
- Python 3.10+
- Conta no [MongoDB Atlas](https://www.mongodb.com/atlas) com cluster criado
- IP liberado no Atlas (Network Access)

### 1. Clonar o repositório
```bash
git clone https://github.com/marcielssilva/projetoTopicos.git
cd projetoTopicos/projetoTopicos
```

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Configurar variáveis de ambiente
```bash
cp .env.example .env
```
Edite o `.env` com sua URI do Atlas se necessário.

### 4. Popular o banco de dados
```bash
python seed.py --limpar
```

### 5. Rodar
```bash
python run.py
```

Acesse: [http://localhost:5000](http://localhost:5000)

---

## 🌐 Deploy no Render

1. Faça o push para o GitHub
2. Acesse [render.com](https://render.com) → **New → Web Service**
3. Conecte o repositório
4. Configure:
   - **Root Directory:** `projetoTopicos`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn run:app`
5. Adicione as variáveis de ambiente:
   - `MONGO_URI` — sua URI do Atlas
   - `SECRET_KEY` — chave secreta Flask
6. Clique em **Deploy**

---

## 🗄️ Modelo de Documento (MongoDB)

```json
{
  "categoria": "Suporte Técnico",
  "subcategoria": "Sem Conexão",
  "titulo": "📡 Sem Conexão",
  "tipo": "fluxo",
  "descricao": "Fluxo completo para clientes sem conexão.",
  "topicos": [
    {
      "titulo": "Validação inicial",
      "passos": [
        "Confirmar se o cliente está sem conexão total",
        "Verificar faturas em dia"
      ]
    }
  ],
  "material_apoio": {
    "titulo": "🔗 Material de Apoio",
    "link": "https://..."
  },
  "visualizacoes": 0
}
```

> `material_apoio` aceita um **objeto único** ou uma **lista de objetos**.

---

## 🔐 Painel Administrativo

Acesse `/admin` para gerenciar conteúdos:

- ✅ Login com usuário e senha
- 📊 Dashboard com estatísticas por categoria
- ➕ Criar novos fluxos com tópicos dinâmicos
- ✏️ Editar conteúdos existentes
- 🗑️ Remover com confirmação
- 🔍 Filtro e busca em tempo real na tabela

---

## 🔍 Rotas da Aplicação

| Rota | Descrição |
|---|---|
| `/` | Página inicial |
| `/categoria/<cat>` | Lista subcategorias |
| `/conteudos/<cat>/<sub>` | Lista conteúdos |
| `/abrir/<id>` | Abre um fluxo |
| `/busca?q=termo&cat=categoria` | Pesquisa full-text |
| `/admin` | Dashboard admin (requer login) |
| `/admin/novo` | Criar novo conteúdo |
| `/admin/editar/<id>` | Editar conteúdo |
| `/admin/deletar/<id>` | Remover conteúdo |
| `/importar` | Importar JSON via interface web |

---

## 👨‍💻 Desenvolvido por

**Marciel Silva** — Tópicos Especiais  

---

> 📌 Este projeto foi desenvolvido com fins acadêmicos e práticos, simulando um sistema real de atendimento técnico.
