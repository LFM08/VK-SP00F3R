import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess  # Para executar o arquivo .bat
import socket  # Para obter o IP do computador
import webbrowser  # Para abrir o Discord

# Função para limpar o terminal
def limpar_terminal():
    terminal.delete(1.0, tk.END)

# Função para executar o arquivo .bat (Spoofer Global)
def spoofer_global():
    try:
        # Substitua 'caminho/do/seu/arquivo.bat' pelo caminho real do seu arquivo .bat
        caminho_arquivo_bat = r"caminho/do/seu/arquivo.bat"
        
        # Executa o arquivo .bat usando o subprocess
        subprocess.run([caminho_arquivo_bat], check=True, shell=True)
        limpar_terminal()
        terminal.insert(tk.END, "Spoofer Global ativado com sucesso!\n")
    except FileNotFoundError:
        messagebox.showerror("Erro", "Arquivo .bat não encontrado!\nVerifique o caminho especificado.")
    except subprocess.CalledProcessError:
        messagebox.showerror("Erro", "Ocorreu um erro ao executar o arquivo .bat.")

# Função para abrir o link do Discord
def abrir_discord():
    # Link da sua loja no Discord
    link_discord = "https://discord.gg/qkCyG6bhbB"
    webbrowser.open(link_discord)

# Obter o IP do computador
def get_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except:
        return "IP não encontrado"

# Configuração da janela principal
root = tk.Tk()
root.title("PAINEL MULTI")
root.geometry("800x600")  # Tamanho da janela
root.configure(bg="#1a1a1a")  # Fundo escuro

# Estilo personalizado
style = {
    "bg_button": "#ff0000",  # Vermelho (para o botão Spoofer Global)
    "fg_button": "white",
    "bg_button_discord": "#007bff",  # Azul (para o botão Discord)
    "bg_frame": "#1a1a1a",  # Preto escuro
    "fg_text": "white",
    "font_button": ("Arial", 16, "bold"),
    "font_label": ("Arial", 18, "bold"),
}

# Frame para o título
titulo_frame = tk.Frame(root, bg=style["bg_frame"])
titulo_frame.pack(pady=10, fill=tk.X)

# Título do painel
titulo_label = tk.Label(titulo_frame, text="PAINEL MULTI", font=style["font_label"], fg=style["fg_text"], bg=style["bg_frame"], bd=2, relief=tk.RAISED)
titulo_label.pack(side=tk.LEFT, padx=10)

# Botões de controle (fechar e minimizar)
botao_minimizar = tk.Button(titulo_frame, text="-", font=("Arial", 12), fg="white", bg="red", width=3, command=lambda: root.iconify())
botao_minimizar.pack(side=tk.RIGHT, padx=5)

botao_fechar = tk.Button(titulo_frame, text="X", font=("Arial", 12), fg="white", bg="red", width=3, command=root.destroy)
botao_fechar.pack(side=tk.RIGHT, padx=5)

# Frame para os botões
botoes_frame = tk.Frame(root, bg=style["bg_frame"])
botoes_frame.pack(expand=True)  # Centraliza verticalmente

# Botão Spoofer Global (centralizado)
botao_spoofer_global = tk.Button(botoes_frame, text="SPOOFER GLOBAL", font=style["font_button"], fg=style["fg_button"], bg=style["bg_button"], bd=2, relief=tk.RAISED, command=spoofer_global)
botao_spoofer_global.pack(pady=20)

# Botão Discord (abaixo do botão Spoofer Global)
botao_discord = tk.Button(botoes_frame, text="Discord", font=style["font_button"], fg="white", bg=style["bg_button_discord"], bd=2, relief=tk.RAISED, command=abrir_discord)
botao_discord.pack(pady=10)

# Frame para a área de terminal
terminal_frame = tk.Frame(root, bg=style["bg_frame"])
terminal_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Área de terminal (scrollable)
terminal = scrolledtext.ScrolledText(terminal_frame, wrap=tk.WORD, font=("Consolas", 12), fg=style["fg_text"], bg=style["bg_frame"], insertbackground="white", borderwidth=2, relief=tk.SUNKEN)
terminal.pack(fill=tk.BOTH, expand=True)

# Rodapé
rodape_frame = tk.Frame(root, bg=style["bg_frame"])
rodape_frame.pack(side=tk.BOTTOM, fill=tk.X)

# Informações no rodapé
status_label = tk.Label(rodape_frame, text=f"STATUS: BYPASS | PAINEL ATUALIZADO | SPOOFER FREE | ROCKSTAR | IP: {get_ip()}", font=("Arial", 10), fg=style["fg_text"], bg=style["bg_frame"])
status_label.pack(side=tk.LEFT, padx=10, pady=5)

# Inicia o loop da interface gráfica
root.mainloop()