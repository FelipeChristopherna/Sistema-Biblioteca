# sistema_biblioteca.py
from estruturas_elementares import Livro, Usuario, Emprestimo, Fila, Pilha
from arvore_binaria_busca import ArvoreBinariaBusca
from lista_encadeada import ListaEncadeada
import datetime

class SistemaBiblioteca:
    def __init__(self):
        self.arvore_livros = ArvoreBinariaBusca()
        self.lista_usuarios = ListaEncadeada()
        self.historico_emprestimos = Pilha() # Pilha de objetos Emprestimo

    def cadastrar_livro(self, titulo, autor, isbn, quantidade):
        # Verificar se já existe livro com mesmo ISBN para evitar duplicidade real de item
        livro_existente_isbn = self.arvore_livros.buscar_por_isbn(isbn) # Busca por ISBN pode ser lenta se a árvore é grande
        if livro_existente_isbn:
            print(f"Erro: Livro com ISBN {isbn} ('{livro_existente_isbn.titulo}') já cadastrado.")
            print("Para atualizar a quantidade, use uma função específica (não implementada) ou remova e cadastre novamente.")
            return False
        
        # Verificar se já existe livro com mesmo título (pela chave da ABB)
        livro_existente_titulo = self.arvore_livros.buscar(titulo)
        if livro_existente_titulo:
            # A lógica de inserção da ABB já lida com isso, mas podemos adicionar um aviso aqui
            print(f"Aviso: Já existe um livro com o título '{titulo}'. Verifique o ISBN.")
            # Se o ISBN for diferente, a ABB pode ter problemas se não permitir duplicatas de chave (título)
            # ou não tiver uma forma de distingui-los. A implementação atual da ABB avisa sobre isso.

        novo_livro = Livro(titulo, autor, isbn, quantidade)
        self.arvore_livros.inserir(novo_livro)
        print(f"Livro '{titulo}' cadastrado com sucesso!")
        return True

    def cadastrar_usuario(self, nome, matricula, curso):
        if self.lista_usuarios.buscar_por_matricula(matricula):
            print(f"Erro: Usuário com matrícula {matricula} já cadastrado.")
            return False
        novo_usuario = Usuario(nome, matricula, curso)
        self.lista_usuarios.inserir_no_inicio(novo_usuario) # Ou inserir_no_fim
        print(f"Usuário '{nome}' cadastrado com sucesso!")
        return True

    def realizar_emprestimo(self, matricula_usuario, isbn_livro):
        usuario = self.lista_usuarios.buscar_por_matricula(matricula_usuario)
        if not usuario:
            print(f"Erro: Usuário com matrícula {matricula_usuario} não encontrado.")
            return

        # A busca principal na ABB é por título. Para empréstimo, é melhor usar ISBN.
        # Portanto, precisamos de uma forma de buscar por ISBN na árvore.
        # Adicionei buscar_por_isbn na ABB, que faz uma varredura.
        # Idealmente, se ISBN é o identificador principal, a árvore seria por ISBN.
        # Ou teríamos um dicionário ISBN -> Livro para acesso rápido.
        # Dado o requisito da ABB ser por título, usamos a busca por ISBN na árvore.
        livro = self.arvore_livros.buscar_por_isbn(isbn_livro) 

        if not livro:
            print(f"Erro: Livro com ISBN {isbn_livro} não encontrado.")
            return

        if livro.quantidade_exemplares > 0:
            livro.quantidade_exemplares -= 1
            # Não vamos adicionar ao histórico aqui, apenas na devolução, conforme o requisito.
            # Mas poderíamos ter uma lista de "empréstimos ativos" se necessário.
            print(f"Livro '{livro.titulo}' emprestado para {usuario.nome}.")
            # Opcional: registrar o empréstimo em uma lista de empréstimos ativos
            # emprestimo_ativo = Emprestimo(usuario, livro) # Sem data de devolução ainda
            # self.pilha_historico.empilhar(emprestimo_ativo) # Se o histórico for usado para ativos também
        else:
            livro.fila_espera.enfileirar(usuario)
            print(f"{usuario.nome} adicionado à fila de espera do livro '{livro.titulo}'.")

    def realizar_devolucao(self, matricula_usuario, isbn_livro):
        usuario = self.lista_usuarios.buscar_por_matricula(matricula_usuario)
        if not usuario:
            print(f"Erro: Usuário com matrícula {matricula_usuario} não encontrado (para devolução).")
            return

        livro = self.arvore_livros.buscar_por_isbn(isbn_livro)
        if not livro:
            print(f"Erro: Livro com ISBN {isbn_livro} não encontrado (para devolução).")
            return

        livro.quantidade_exemplares += 1
        # Criar registro de empréstimo concluído para o histórico
        # Precisaríamos da data de empréstimo original. Para simplificar, não a temos aqui.
        # Se tivéssemos empréstimos ativos, pegaríamos de lá.
        # Vamos criar um registro com a data de devolução apenas.
        # Um sistema completo teria uma forma de rastrear o empréstimo original.
        emprestimo_concluido = Emprestimo(usuario, livro, data_devolucao=datetime.date.today())
        self.historico_emprestimos.empilhar(emprestimo_concluido)
        print(f"Livro '{livro.titulo}' devolvido por {usuario.nome}.")

        if not livro.fila_espera.esta_vazia():
            proximo_usuario_na_fila = livro.fila_espera.desenfileirar()
            print(f"Notificando próximo da fila: {proximo_usuario_na_fila.nome} para o livro '{livro.titulo}'.")
            # Realizar o empréstimo automaticamente para o próximo
            if livro.quantidade_exemplares > 0: # Deveria ser, pois acabamos de devolver
                livro.quantidade_exemplares -= 1
                print(f"Livro '{livro.titulo}' emprestado automaticamente para {proximo_usuario_na_fila.nome}.")
                # Opcional: registrar este novo empréstimo como ativo
            else: # Improvável, mas como segurança
                 print(f"Erro inesperado: Livro '{livro.titulo}' sem exemplares após devolução e antes de novo empréstimo da fila.")


    def consultar_livro_por_titulo(self, titulo):
        livro = self.arvore_livros.buscar(titulo)
        if livro:
            print(livro)
            print(f"  ↳ Fila de espera: {len(livro.fila_espera)} pessoa(s).")
        else:
            print(f"Livro com título '{titulo}' não encontrado.")
        return livro

    def consultar_usuario_por_matricula(self, matricula):
        usuario = self.lista_usuarios.buscar_por_matricula(matricula)
        if usuario:
            print(usuario)
        else:
            print(f"Usuário com matrícula {matricula} não encontrado.")
        return usuario

    def exibir_historico_emprestimos(self):
        if self.historico_emprestimos.esta_vazia():
            print("Nenhum empréstimo no histórico.")
            return
        print("\n--- Histórico de Empréstimos (Mais recentes primeiro) ---")
        for emprestimo in self.historico_emprestimos: # Iterando sobre a pilha
            print(emprestimo)
        print("--- Fim do Histórico ---")

    def exibir_fila_espera_livro(self, isbn_livro):
        livro = self.arvore_livros.buscar_por_isbn(isbn_livro)
        if not livro:
            print(f"Livro com ISBN {isbn_livro} não encontrado.")
            return
        
        print(f"\n--- Fila de Espera para o Livro: {livro.titulo} (ISBN: {livro.isbn}) ---")
        if livro.fila_espera.esta_vazia():
            print("Fila de espera vazia.")
        else:
            for i, usuario_na_fila in enumerate(livro.fila_espera._dados): # Acessando _dados para iterar sem remover
                print(f"{i+1}. {usuario_na_fila.nome} (Mat: {usuario_na_fila.matricula})")
        print("--- Fim da Fila de Espera ---")

    def listar_todos_os_livros(self):
        livros = self.arvore_livros.listar_todos_em_ordem()
        if not livros:
            print("Nenhum livro cadastrado.")
            return
        print("\n--- Todos os Livros (Ordenados por Título) ---")
        for livro in livros:
            print(livro)
        print("--- Fim da Lista de Livros ---")

    def listar_todos_os_usuarios(self):
        usuarios = self.lista_usuarios.listar_todos()
        if not usuarios:
            print("Nenhum usuário cadastrado.")
            return
        print("\n--- Todos os Usuários ---")
        for usuario in usuarios:
            print(usuario)
        print("--- Fim da Lista de Usuários ---")