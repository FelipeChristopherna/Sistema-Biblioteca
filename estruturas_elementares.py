# estruturas_elementares.py
import datetime

class Livro:
    def __init__(self, titulo, autor, isbn, quantidade_exemplares):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn # Usado como identificador único do livro em operações internas
        self.quantidade_exemplares = quantidade_exemplares
        self.fila_espera = Fila() # Cada livro terá sua própria fila de espera

    def __str__(self):
        return f"Título: {self.titulo}, Autor: {self.autor}, ISBN: {self.isbn}, Disponíveis: {self.quantidade_exemplares}"

class Usuario:
    def __init__(self, nome, matricula, curso):
        self.nome = nome
        self.matricula = matricula # Identificador único do usuário
        self.curso = curso

    def __str__(self):
        return f"Nome: {self.nome}, Matrícula: {self.matricula}, Curso: {self.curso}"

class Emprestimo:
    def __init__(self, usuario, livro, data_emprestimo=None, data_devolucao=None):
        self.usuario = usuario
        self.livro = livro
        self.data_emprestimo = data_emprestimo if data_emprestimo else datetime.date.today()
        self.data_devolucao = data_devolucao

    def __str__(self):
        status_devolucao = f"Devolvido em: {self.data_devolucao}" if self.data_devolucao else "Ainda emprestado"
        return (f"Usuário: {self.usuario.nome} (Mat: {self.usuario.matricula})\n"
                f"Livro: {self.livro.titulo} (ISBN: {self.livro.isbn})\n"
                f"Emprestado em: {self.data_emprestimo}\n"
                f"{status_devolucao}\n" + "-"*20)

# As classes Fila, Pilha, NoArvore, ArvoreBinariaBusca, NoLista, ListaEncadeada virão a seguir
# e serão importadas ou definidas aqui.
# Para simplicidade, usaremos collections.deque para Fila e lista Python para Pilha.
from collections import deque

class Fila:
    def __init__(self):
        self._dados = deque()

    def enfileirar(self, item):
        self._dados.append(item)

    def desenfileirar(self):
        if not self.esta_vazia():
            return self._dados.popleft()
        return None

    def esta_vazia(self):
        return len(self._dados) == 0

    def ver_primeiro(self):
        if not self.esta_vazia():
            return self._dados[0]
        return None
    
    def __len__(self):
        return len(self._dados)

class Pilha:
    def __init__(self):
        self._dados = []

    def empilhar(self, item):
        self._dados.append(item)

    def desempilhar(self):
        if not self.esta_vazia():
            return self._dados.pop()
        return None

    def esta_vazia(self):
        return len(self._dados) == 0

    def ver_topo(self):
        if not self.esta_vazia():
            return self._dados[-1]
        return None
    
    def __iter__(self): # Para facilitar a exibição do histórico
        return reversed(self._dados)