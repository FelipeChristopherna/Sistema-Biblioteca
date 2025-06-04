# lista_encadeada.py
# from estruturas_elementares import Usuario # Se Usuario estiver em outro arquivo

class NoLista:
    def __init__(self, usuario):
        self.usuario = usuario # O dado do nó é um objeto Usuario
        self.proximo = None

class ListaEncadeada:
    def __init__(self):
        self.cabeca = None

    def esta_vazia(self):
        return self.cabeca is None

    def inserir_no_inicio(self, usuario):
        novo_no = NoLista(usuario)
        novo_no.proximo = self.cabeca
        self.cabeca = novo_no

    def buscar_por_matricula(self, matricula):
        atual = self.cabeca
        while atual is not None:
            if atual.usuario.matricula == matricula:
                return atual.usuario
            atual = atual.proximo
        return None

    def listar_todos(self):
        usuarios = []
        atual = self.cabeca
        while atual is not None:
            usuarios.append(atual.usuario)
            atual = atual.proximo
        return usuarios