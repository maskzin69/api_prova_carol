from flask import Flask, request, jsonify

app = Flask(__name__)


livros = []
contador_id = 1



@app.route("/livros", methods=["GET"])
def listar_livros():
    return jsonify(livros), 200



@app.route("/livros/<int:id>", methods=["GET"])
def buscar_livro(id):
    for livro in livros:
        if livro["id"] == id:
            return jsonify(livro), 200

    return {"erro": "Livro não encontrado"}, 404



@app.route("/livros", methods=["POST"])
def cadastrar_livro():
    global contador_id

    dados = request.get_json()


    if not dados.get("titulo") or not dados.get("autor"):
        return {"erro": "Título e autor são obrigatórios"}, 400


    if dados.get("ano", 0) < 0:
        return {"erro": "Ano inválido"}, 400


    for l in livros:
        if l["titulo"].lower() == dados["titulo"].lower():
            return {"erro": "Livro já cadastrado"}, 400

    novo_livro = {
        "id": contador_id,
        "titulo": dados["titulo"],
        "autor": dados["autor"],
        "ano": dados["ano"]
    }

    livros.append(novo_livro)
    contador_id += 1


    return {
        "mensagem": "Livro cadastrado com sucesso",
        "livro": novo_livro
    }, 201



@app.route("/livros/<int:id>", methods=["PUT"])
def atualizar_livro(id):

    dados = request.get_json()

    for livro in livros:
        if livro["id"] == id:

            if not dados.get("titulo") or not dados.get("autor"):
                return {"erro": "Título e autor são obrigatórios"}, 400

            if dados["ano"] < 0:
                return {"erro": "Ano inválido"}, 400

            livro["titulo"] = dados["titulo"]
            livro["autor"] = dados["autor"]
            livro["ano"] = dados["ano"]

            return {
                "mensagem": "Livro atualizado com sucesso",
                "livro": livro
            }, 200

    return {"erro": "Livro não encontrado"}, 404



@app.route("/livros/<int:id>", methods=["PATCH"])
def atualizar_parcial(id):

    dados = request.get_json()

    for livro in livros:
        if livro["id"] == id:

            if "titulo" in dados:
                livro["titulo"] = dados["titulo"]

            if "autor" in dados:
                livro["autor"] = dados["autor"]

            if "ano" in dados:
                if dados["ano"] < 0:
                    return {"erro": "Ano inválido"}, 400
                livro["ano"] = dados["ano"]

            return {
                "mensagem": "Livro atualizado parcialmente",
                "livro": livro
            }, 200

    return {"erro": "Livro não encontrado"}, 404



@app.route("/livros/<int:id>", methods=["DELETE"])
def deletar_livro(id):

    for livro in livros:
        if livro["id"] == id:
            livros.remove(livro)

            return {
                "mensagem": "Livro removido com sucesso"
            }, 200

    return {"erro": "Livro não encontrado"}, 404


if __name__ == "__main__":
    app.run(debug=True)

    import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)