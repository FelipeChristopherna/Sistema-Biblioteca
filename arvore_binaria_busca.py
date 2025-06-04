# arvore_binaria_busca.py
# from estruturas_elementares import Livro # Se Livro estiver em outro arquivo

class NoArvore:
    def __init__(self, livro):
        self.livro = livro # O dado do nó é um objeto Livro
        self.esquerda = None
        self.direita = None
        # A chave de comparação para a ABB será o título do livro
        self.chave = livro.titulo.lower() # Normalizar para lower case para busca case-insensitive

class ArvoreBinariaBusca:
    def __init__(self):
        self.raiz = None

    def inserir(self, livro):
        if self.raiz is None:
            self.raiz = NoArvore(livro)
        else:
            self._inserir_recursivo(self.raiz, livro)

    def _inserir_recursivo(self, no_atual, livro):
        chave_livro = livro.titulo.lower()
        if chave_livro < no_atual.chave:
            if no_atual.esquerda is None:
                no_atual.esquerda = NoArvore(livro)
            else:
                self._inserir_recursivo(no_atual.esquerda, livro)
        elif chave_livro > no_atual.chave:
            if no_atual.direita is None:
                no_atual.direita = NoArvore(livro)
            else:
                self._inserir_recursivo(no_atual.direita, livro)
        else:
            print(f"Aviso: Livro com título '{livro.titulo}' já existe. Pode ser uma edição diferente ou um erro.")

            if no_atual.livro.isbn == livro.isbn:
                no_atual.livro.quantidade_exemplares = livro.quantidade_exemplares
            else:
                print(f"  ↳ Não inserido: Título igual, ISBN diferente. Considere títulos mais específicos ou usar ISBN como chave primária da árvore.")


    def buscar(self, titulo):
        titulo_busca = titulo.lower()
        return self._buscar_recursivo(self.raiz, titulo_busca)

    def _buscar_recursivo(self, no_atual, titulo_busca):
        if no_atual is None or no_atual.chave == titulo_busca:
            return no_atual.livro if no_atual else None
        
        if titulo_busca < no_atual.chave:
            return self._buscar_recursivo(no_atual.esquerda, titulo_busca)
        else:
            return self._buscar_recursivo(no_atual.direita, titulo_busca)

    def buscar_por_isbn(self, isbn): # Busca auxiliar por ISBN (não usa a estrutura da ABB diretamente)
        return self._buscar_isbn_recursivo(self.raiz, isbn)

    def _buscar_isbn_recursivo(self, no_atual, isbn):
        if no_atual is None:
            return None
        if no_atual.livro.isbn == isbn:
            return no_atual.livro
        
        # Procura em ambas as subárvores, pois a árvore não é ordenada por ISBN
        encontrado_esquerda = self._buscar_isbn_recursivo(no_atual.esquerda, isbn)
        if encontrado_esquerda:
            return encontrado_esquerda
        return self._buscar_isbn_recursivo(no_atual.direita, isbn)

    def listar_todos_em_ordem(self):
        livros = []
        self._listar_todos_em_ordem_recursivo(self.raiz, livros)
        return livros

    def _listar_todos_em_ordem_recursivo(self, no_atual, livros):
        if no_atual:
            self._listar_todos_em_ordem_recursivo(no_atual.esquerda, livros)
            livros.append(no_atual.livro)
            self._listar_todos_em_ordem_recursivo(no_atual.direita, livros)