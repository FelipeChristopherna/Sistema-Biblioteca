import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from sistema_biblioteca import SistemaBiblioteca

class BibliotecaApp:
    def __init__(self, root):
        self.sistema = SistemaBiblioteca()
        self.root = root
        self.root.title("Sistema de Biblioteca")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Tema bonito
        style = tb.Style("superhero")  # Experimente outros temas: flatly, cyborg, morph, etc

        # Notebook (abas)
        self.notebook = tb.Notebook(self.root, bootstyle="primary")
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Abas
        self.frame_livros = tb.Frame(self.notebook)
        self.frame_usuarios = tb.Frame(self.notebook)
        self.frame_emprestimos = tb.Frame(self.notebook)
        self.frame_historico = tb.Frame(self.notebook)

        self.notebook.add(self.frame_livros, text="Livros")
        self.notebook.add(self.frame_usuarios, text="Usuários")
        self.notebook.add(self.frame_emprestimos, text="Empréstimos")
        self.notebook.add(self.frame_historico, text="Histórico")

        self.criar_aba_livros()
        self.criar_aba_usuarios()
        # ... continue para as outras abas

    def criar_aba_livros(self):
        # Exemplo de campos para cadastro de livro
        tb.Label(self.frame_livros, text="Cadastro de Livro", font=("Segoe UI", 16, "bold")).pack(pady=10)
        # ... Adicione campos, botões e listagem de livros aqui

    def criar_aba_usuarios(self):
        tb.Label(self.frame_usuarios, text="Cadastro de Usuário", font=("Segoe UI", 16, "bold")).pack(pady=10)
        # ... Adicione campos, botões e listagem de usuários aqui

if __name__ == "__main__":
    root = tb.Window(themename="superhero")
    app = BibliotecaApp(root)
    root.mainloop()