# Livraria MVP – Arquitetura MVC

MVP do aplicativo da livraria (consultar estoque, ver preço, ver horário e endereço
da loja e escolher loja favorita), organizado no padrão Model-View-Controller com Flask.

## Como o MVC está organizado

| Camada | Pasta | Responsabilidade |
|---|---|---|
| **Model** | `models/` | Entidades (`Livro`, `Loja`) e regras de negócio (`Catalogo`). Não conhece Flask nem HTML. |
| **View** | `views/` e `static/` | Templates Jinja que exibem os dados. Não têm regra de negócio. |
| **Controller** | `controllers/` | Recebe a ação do usuário (rota HTTP), consulta o Model e escolhe a View. |

`app.py` apenas monta a aplicação, ligando as três camadas.

### Fluxo de uma requisição

1. O usuário age na **View** (busca um livro ou clica em "Definir como favorita").
2. O **Controller** recebe a ação e chama o **Model** (`catalogo.disponibilidade(...)`).
3. O **Model** devolve os dados.
4. O **Controller** envia os dados para a **View**, que é atualizada na tela.

## Como rodar

```bash
pip install -r requirements.txt
pytest -v        # testes do Model e dos Controllers
python app.py    # http://localhost:5000
```
