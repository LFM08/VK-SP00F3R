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
    if tipo == "diario":
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
    print("Gerador de Chaves de Acesso")
    print("1. Diário (24h)")
    print("2. Semanal (7 dias)")
    print("3. Mensal (30 dias)")
    print("4. Lifetime (Permanente)")
    
    escolha = input("Escolha o tipo de chave (1-4): ")
    
    if escolha == "1":
        tipo = "diario"
    elif escolha == "2":
        tipo = "semanal"
    elif escolha == "3":
        tipo = "mensal"
    elif escolha == "4":
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