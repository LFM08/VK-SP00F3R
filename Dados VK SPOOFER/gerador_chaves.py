import hashlib
import random
import string
from datetime import datetime

def gerar_prefixo(tamanho=8):
    """
    Gera um prefixo aleatório com letras e números.
    """
    caracteres = string.ascii_uppercase + string.digits
    return ''.join(random.choice(caracteres) for _ in range(tamanho))

def gerar_chave(tipo):
    """
    Gera uma chave única com base no tipo de validade.
    """
    # Gera um prefixo aleatório
    prefixo = gerar_prefixo()
    
    # Define o sufixo com base no tipo de validade
    if tipo == "hora":
        sufixo = "-HORA"
    elif tipo == "diario":
        sufixo = "-DIARIO"
    elif tipo == "semanal":
        sufixo = "-SEMANAL"
    elif tipo == "mensal":
        sufixo = "-MENSAL"
    elif tipo == "lifetime":
        sufixo = "-LIFETIME"
    else:
        raise ValueError("Tipo de chave inválido.")
    
    # Combina o prefixo e o sufixo para formar a chave
    chave = f"{prefixo}{sufixo}"
    return chave

def main():
    print("====================================")
    print("          Gerador de Chaves")
    print("====================================")
    print("[1] Gerar chave de 1 hora")
    print("[2] Gerar chave diária (24h)")
    print("[3] Gerar chave semanal (7 dias)")
    print("[4] Gerar chave mensal (30 dias)")
    print("[5] Gerar chave lifetime (Permanente)")
    print("====================================")
    
    escolha = input("Escolha o tipo de chave (1-5): ")
    
    if escolha == "1":
        tipo = "hora"
    elif escolha == "2":
        tipo = "diario"
    elif escolha == "3":
        tipo = "semanal"
    elif escolha == "4":
        tipo = "mensal"
    elif escolha == "5":
        tipo = "lifetime"
    else:
        print("Opção inválida.")
        return
    
    num_chaves = int(input("Quantas chaves deseja gerar? "))
    
    with open("chaves.txt", "a") as file:
        for _ in range(num_chaves):
            chave = gerar_chave(tipo)
            file.write(f"{chave}:ativa\n")
            print(f"Chave gerada: {chave}")

if __name__ == "__main__":
    main()