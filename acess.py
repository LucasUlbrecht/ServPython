import tkinter as tk
from tkinter import messagebox, ttk
import requests
import sqlite3 as sqlite3

# URL do servidor Flask
SERVER_URL = "https://44b7-2804-14c-7582-4438-d53f-eb4d-681b-129b.ngrok-free.app"

# Função para listar usuários (assumindo que você tem um endpoint no servidor que retorna os usuários)
def listar_usuarios():
    try:
        response = requests.get(f'{SERVER_URL}/users')
        if response.status_code == 200:
            users = response.json().get("users", [])
            return users
        else:
            messagebox.showerror("Erro", "Falha ao obter lista de usuários")
            return []
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao se conectar ao servidor: {e}")
        return []

def listar_produtos(user_id):
    try:
        response = requests.get(f'{SERVER_URL}/products/{user_id}')
        if response.status_code == 200:
            products = response.json().get("products", [])
            return products if products else []
        else:
            messagebox.showerror("Erro", f"Falha ao obter produtos do usuário {user_id}")
            return []
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao se conectar ao servidor: {e}")
        return []


def atualizar_produtos(event):
    try:
        # Verifica se há um usuário selecionado
        selecionados = lista_usuarios.curselection()
        if not selecionados:
            return
        
        # Obtém o ID do usuário selecionado
        user_id = lista_usuarios.get(selecionados)
        products = listar_produtos(user_id)
        
        # Limpa a lista de produtos
        lista_produtos.delete(*lista_produtos.get_children())
        
        # Adiciona os produtos à lista
        for product in products:
            lista_produtos.insert("", "end", values=(product['barcode'], product['product_name']))
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao atualizar produtos: {e}")

# Função principal para a interface gráfica
def iniciar_interface():
    global lista_usuarios, lista_produtos

    # Criação da janela principal
    root = tk.Tk()
    root.title("Gerenciamento de Produtos por Usuário")
    root.geometry("600x400")

    # Título
    label_titulo = tk.Label(root, text="Selecione um usuário para listar os produtos", font=("Arial", 14))
    label_titulo.pack(pady=10)

    # Frame para lista de usuários
    frame_usuarios = tk.Frame(root)
    frame_usuarios.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    # Título da lista de usuários
    label_usuarios = tk.Label(frame_usuarios, text="Usuários", font=("Arial", 12))
    label_usuarios.pack()

    # Lista de usuários (usando Listbox)
    lista_usuarios = tk.Listbox(frame_usuarios, height=15, selectmode=tk.SINGLE)
    lista_usuarios.pack(side=tk.LEFT, fill=tk.Y)

    # Adicionar barra de rolagem para a lista de usuários
    scrollbar_usuarios = tk.Scrollbar(frame_usuarios, orient="vertical")
    scrollbar_usuarios.config(command=lista_usuarios.yview)
    scrollbar_usuarios.pack(side=tk.RIGHT, fill=tk.Y)
    lista_usuarios.config(yscrollcommand=scrollbar_usuarios.set)

    # Frame para lista de produtos
    frame_produtos = tk.Frame(root)
    frame_produtos.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Título da lista de produtos
    label_produtos = tk.Label(frame_produtos, text="Produtos", font=("Arial", 12))
    label_produtos.pack()

    # Tabela de produtos (usando Treeview)
    lista_produtos = ttk.Treeview(frame_produtos, columns=("barcode", "product_name"), show="headings")
    lista_produtos.heading("barcode", text="Código de Barras")
    lista_produtos.heading("product_name", text="Nome do Produto")
    lista_produtos.pack(fill=tk.BOTH, expand=True)

    # Adicionar barra de rolagem para a lista de produtos
    scrollbar_produtos = tk.Scrollbar(frame_produtos, orient="vertical")
    scrollbar_produtos.config(command=lista_produtos.yview)
    scrollbar_produtos.pack(side=tk.RIGHT, fill=tk.Y)
    lista_produtos.config(yscrollcommand=scrollbar_produtos.set)

    # Evento de seleção de usuário
    lista_usuarios.bind('<<ListboxSelect>>', atualizar_produtos)

    # Carregar usuários na lista
    usuarios = listar_usuarios()
    for user in usuarios:
        lista_usuarios.insert(tk.END, user)

    # Iniciar o loop principal do Tkinter
    root.mainloop()

# Executa a interface gráfica
if __name__ == '__main__':
    iniciar_interface()
