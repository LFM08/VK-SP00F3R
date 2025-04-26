from flask import Flask, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# Caminhos dos arquivos centralizados
CAMINHO_CHAVES = "C:/Users/LFM/Documents/Dados VK SPOOFER/chaves.txt"  # Altere conforme necessário
CAMINHO_USUARIOS = "C:/Users/LFM/Documents/Dados VK SPOOFER/usuarios.txt"  # Altere conforme necessário

# Função para carregar chaves válidas
def carregar_chaves():
    """
    Carrega as chaves válidas do arquivo.
    Retorna um dicionário onde a chave é o código da chave e o valor é o status ("ativa" ou "usada").
    """
    try:
        with open(CAMINHO_CHAVES, "r") as file:
            return {line.strip().split(":")[0]: line.strip().split(":")[1] for line in file if line.strip()}
    except FileNotFoundError:
        print("Arquivo de chaves não encontrado. Criando um novo.")
        open(CAMINHO_CHAVES, "w").close()  # Cria o arquivo vazio
        return {}

# Função para salvar chaves no arquivo centralizado
def salvar_chave(chave, status):
    """
    Atualiza o status de uma chave no arquivo de chaves.
    """
    chaves = carregar_chaves()
    chaves[chave] = status
    try:
        with open(CAMINHO_CHAVES, "w") as file:
            for chave, status in chaves.items():
                file.write(f"{chave}:{status}\n")
    except Exception as e:
        print(f"Erro ao salvar chave: {e}")
        sys.exit(1)

# Função para carregar usuários registrados
def carregar_usuarios():
    """
    Carrega os usuários registrados do arquivo usuarios.txt.
    Retorna uma lista de dicionários com os dados dos usuários.
    """
    usuarios_registrados = []
    try:
        with open(CAMINHO_USUARIOS, "r") as file:
            for linha in file:
                partes = linha.strip().split("|")
                if len(partes) == 5:
                    nome, senha, chave, data_registro, ip = partes
                    usuarios_registrados.append({
                        "nome": nome,
                        "senha": senha,
                        "chave": chave,
                        "data_registro": data_registro,
                        "ip": ip,
                    })
    except FileNotFoundError:
        print("Arquivo de usuários não encontrado. Criando um novo.")
        open(CAMINHO_USUARIOS, "w").close()  # Cria o arquivo vazio
        return usuarios_registrados
    return usuarios_registrados

# Função para salvar usuários no arquivo centralizado
def salvar_usuario(nome, senha, chave, ip):
    """
    Salva um novo usuário no arquivo usuarios.txt.
    """
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(CAMINHO_USUARIOS, "a") as file:
            file.write(f"{nome}|{senha}|{chave}|{data_hora}|{ip}\n")
    except Exception as e:
        print(f"Erro ao salvar usuário: {e}")
        sys.exit(1)

@app.route('/validar_chave', methods=['POST'])
def validar_chave():
    dados = request.json
    chave = dados.get("chave")

    chaves = carregar_chaves()
    if chave in chaves and chaves[chave] == "ativa":
        return jsonify({"status": "valida"}), 200
    else:
        return jsonify({"status": "invalida", "mensagem": "Chave inválida ou já usada."}), 400

@app.route('/registrar', methods=['POST'])
def registrar():
    dados = request.json
    nome = dados.get("nome")
    senha = dados.get("senha")
    chave = dados.get("chave")
    ip = dados.get("ip")

    # Verifica se o nome já existe
    usuarios = carregar_usuarios()
    if any(usuario["nome"] == nome for usuario in usuarios):
        return jsonify({"status": "erro", "mensagem": "Nome já utilizado."}), 400

    # Verifica se a chave é válida
    chaves = carregar_chaves()
    if chave not in chaves or chaves[chave] != "ativa":
        return jsonify({"status": "erro", "mensagem": "Chave inválida ou já usada."}), 400

    # Marca a chave como usada
    salvar_chave(chave, "usada")

    # Salva o usuário no banco de dados
    salvar_usuario(nome, senha, chave, ip)

    return jsonify({"status": "sucesso", "mensagem": "Registro realizado com sucesso!"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)