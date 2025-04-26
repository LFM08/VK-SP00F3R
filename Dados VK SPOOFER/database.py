import sys
from datetime import datetime, timedelta
import requests

# Caminho para os arquivos de banco de dados
DATABASE_FILE = "usuarios.txt"  # Armazena os usuários registrados
KEYS_FILE = "C:/Users/LFM/Documents/Dados VK SPOOFER/chaves.txt"  # Altere conforme necessário
SERVER_URL = "http://127.0.0.1:5000"  # URL do servidor Flask

def inicializar_arquivos():
    """
    Verifica se os arquivos de banco de dados existem.
    Se não existirem, cria-os com conteúdo inicial.
    """
    try:
        # Verifica e cria o arquivo usuarios.txt
        with open(DATABASE_FILE, "a+") as file:
            file.seek(0)  # Move o cursor para o início do arquivo
            if not file.read():  # Se o arquivo estiver vazio
                file.write("")  # Inicializa como vazio

        # Verifica e cria o arquivo chaves.txt
        with open(KEYS_FILE, "a+") as file:
            file.seek(0)  # Move o cursor para o início do arquivo
            if not file.read():  # Se o arquivo estiver vazio
                file.write("")  # Inicializa como vazio
    except Exception as e:
        print(f"Erro ao inicializar arquivos: {e}")
        sys.exit(1)

def carregar_chaves():
    """
    Carrega as chaves válidas do arquivo.
    Retorna um dicionário onde a chave é o código da chave e o valor é o status ("ativa" ou "usada").
    """
    try:
        with open(KEYS_FILE, "r") as file:
            return {line.strip().split(":")[0]: line.strip().split(":")[1] for line in file if line.strip()}
    except FileNotFoundError:
        print("Arquivo de chaves não encontrado. Certifique-se de configurar o arquivo 'chaves.txt'.")
        sys.exit(1)

def salvar_chave(chave, status):
    """
    Atualiza o status de uma chave no arquivo de chaves.
    """
    chaves = carregar_chaves()
    chaves[chave] = status
    try:
        with open(KEYS_FILE, "w") as file:
            for chave, status in chaves.items():
                file.write(f"{chave}:{status}\n")
    except Exception as e:
        print(f"Erro ao salvar chave: {e}")
        sys.exit(1)

def carregar_usuarios():
    """
    Carrega os usuários registrados do banco de dados.
    Retorna um dicionário onde a chave é o nome do usuário e o valor contém os dados do usuário.
    """
    usuarios = {}
    try:
        with open(DATABASE_FILE, "r") as file:
            for line in file:
                # Formato esperado: Nome|Senha|Chave|Data e Hora|IP
                partes = line.strip().split("|")
                if len(partes) == 5:
                    nome, senha, chave, data_hora, ip = partes
                    usuarios[nome] = {
                        "senha": senha,
                        "chave": chave,
                        "data_registro": datetime.strptime(data_hora, "%Y-%m-%d %H:%M:%S"),
                        "ip": ip
                    }
    except FileNotFoundError:
        pass
    return usuarios

def salvar_usuario(nome, senha, chave, ip):
    """
    Salva um novo usuário no banco de dados.
    """
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(DATABASE_FILE, "a") as file:
            file.write(f"{nome}|{senha}|{chave}|{data_hora}|{ip}\n")
    except Exception as e:
        print(f"Erro ao salvar usuário: {e}")
        sys.exit(1)

def verificar_nome_existente(nome):
    """
    Verifica se o nome de usuário já está em uso.
    Retorna True se o nome existir, False caso contrário.
    """
    usuarios = carregar_usuarios()
    return nome in usuarios

def registrar(nome, senha, chave, ip):
    """
    Registra um novo usuário se a chave for válida e o nome não estiver em uso.
    Retorna True se o registro for bem-sucedido, False caso contrário.
    """
    if verificar_nome_existente(nome):
        print("Nome já utilizado.")
        return False  # Nome já existente

    chaves = carregar_chaves()
    if chave not in chaves or chaves[chave] != "ativa":
        print("Chave inválida ou já usada.")
        return False  # Chave inválida ou já usada

    # Marca a chave como usada
    salvar_chave(chave, "usada")

    # Salva o usuário no banco de dados
    salvar_usuario(nome, senha, chave, ip)
    print("Registro realizado com sucesso!")
    return True

def login(nome, senha, ip_atual):
    """
    Verifica se o login é válido comparando a senha original e o IP registrado.
    """
    usuarios = carregar_usuarios()
    if nome in usuarios and usuarios[nome]["senha"] == senha:
        ip_registrado = usuarios[nome]["ip"]
        if ip_atual == ip_registrado:
            print("Login bem-sucedido!")
            return True  # Login bem-sucedido
        else:
            print("IP não autorizado.")
            return False  # IP diferente
    print("Nome ou senha inválidos.")
    return False  # Nome ou senha inválidos

def calcular_tempo_restante(chave, data_registro):
    """
    Calcula o tempo restante da chave com base no sufixo (-HORA, -DIARIO, etc.).
    Retorna uma mensagem indicando o tempo restante ou se a chave expirou.
    """
    if chave.endswith("-HORA"):
        duracao = timedelta(hours=1)
    elif chave.endswith("-DIARIO"):
        duracao = timedelta(days=1)
    elif chave.endswith("-SEMANAL"):
        duracao = timedelta(days=7)
    elif chave.endswith("-MENSAL"):
        duracao = timedelta(days=30)
    elif chave.endswith("-LIFETIME"):
        return "Lifetime (Sem expiração)"
    else:
        return "Tipo de chave inválido."

    data_expiracao = data_registro + duracao
    agora = datetime.now()

    if agora > data_expiracao:
        return "Chave expirada."

    tempo_restante = data_expiracao - agora
    dias = tempo_restante.days
    horas = tempo_restante.seconds // 3600
    minutos = (tempo_restante.seconds % 3600) // 60

    return f"Faltam {dias} dias, {horas} horas e {minutos} minutos."

def consultar_tempo_key():
    """
    Consulta o tempo restante da chave do usuário logado.
    """
    nome_logado = sys.argv[2]
    usuarios = carregar_usuarios()

    if nome_logado not in usuarios:
        print("Usuário não encontrado.")
        sys.exit(1)

    chave = usuarios[nome_logado]["chave"]
    data_registro = usuarios[nome_logado]["data_registro"]
    tempo_restante = calcular_tempo_restante(chave, data_registro)
    print(tempo_restante)

def validar_chave_no_servidor(chave):
    """
    Valida a chave no servidor Flask.
    Retorna True se a chave for válida, False caso contrário.
    """
    try:
        response = requests.post(f"{SERVER_URL}/validar_chave", json={"chave": chave})
        if response.status_code == 200:
            return response.json().get("status") == "valida"
        else:
            print(f"Erro ao validar chave: {response.json().get('mensagem')}")
            return False
    except Exception as e:
        print(f"Falha ao conectar ao servidor: {e}")
        return False

def main():
    inicializar_arquivos()

    if len(sys.argv) < 2:
        print("Erro: Argumentos insuficientes.")
        sys.exit(1)

    comando = sys.argv[1]

    if comando == "login":
        nome = sys.argv[2]
        senha = sys.argv[3]
        ip_atual = sys.argv[4]
        if login(nome, senha, ip_atual):
            sys.exit(0)  # Login bem-sucedido
        else:
            sys.exit(1)  # Falha

    elif comando == "registrar":
        nome = sys.argv[2]
        senha = sys.argv[3]
        chave = sys.argv[4]
        ip = sys.argv[5]

        # Adiciona validação centralizada no servidor
        if not validar_chave_no_servidor(chave):
            print("Chave inválida ou já usada.")
            sys.exit(1)

        if registrar(nome, senha, chave, ip):
            sys.exit(0)  # Sucesso
        else:
            sys.exit(1)  # Falha

    elif comando == "consultar_tempo_key":
        consultar_tempo_key()

if __name__ == "__main__":
    main()