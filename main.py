class Endereco:

    def __init__(self, rua, numero, bairro, cidade, estado, cep):
        self.rua = rua
        self.numero = numero
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.cep = cep

    def formatado(self):
        return (f"{self.rua}, {self.numero} - {self.bairro}, "
                f"{self.cidade}/{self.estado} - CEP {self.cep}")

    def __str__(self):
        return self.formatado()


class SalaDeAula:

    def __init__(self, numero, capacidade, escola):
        self.numero = numero
        self.capacidade = capacidade
        self._escola = escola

    def descricao(self):
        return (f"Sala {self.numero} (capacidade: {self.capacidade}) "
                f"- {self._escola.nome}")

    def __str__(self):
        return self.descricao()


class Escola:

    def __init__(self, nome, cnpj):
        self.nome = nome
        self.cnpj = cnpj
        self._salas = []
        self._professores = []

    def adicionar_sala(self, numero, capacidade):
        sala = SalaDeAula(numero, capacidade, self)
        self._salas.append(sala)
        return sala

    def listar_salas(self):
        return list(self._salas)

    def fechar(self):
        self._salas.clear()
        for professor in list(self._professores):
            professor.deixar_de_lecionar_em(self)
        print(f"Escola '{self.nome}' fechada. Salas removidas.")

    def adicionar_professor(self, professor):
        if professor not in self._professores:
            self._professores.append(professor)
        if self not in professor.escolas:
            professor.escolas.append(self)

    def listar_professores(self):
        return list(self._professores)

    def __str__(self):
        return f"{self.nome} ({len(self._salas)} salas, {len(self._professores)} professores)"


class Professor:

    def __init__(self, nome, registro, disciplina):
        self.nome = nome
        self.registro = registro
        self.disciplina = disciplina
        self.escolas = []

    def lecionar_em(self, escola):
        escola.adicionar_professor(self)

    def deixar_de_lecionar_em(self, escola):
        if escola in self.escolas:
            self.escolas.remove(escola)
        if self in escola._professores:
            escola._professores.remove(self)

    def __str__(self):
        nomes = ", ".join(e.nome for e in self.escolas) or "nenhuma escola"
        return f"Prof. {self.nome} ({self.disciplina}) - leciona em: {nomes}"


class Aluno:

    def __init__(self, nome, matricula, endereco):
        self.nome = nome
        self.matricula = matricula
        self.endereco = endereco

    def alterar_endereco(self, novo_endereco):
        self.endereco = novo_endereco

    def __str__(self):
        return f"{self.nome} (mat. {self.matricula}) - {self.endereco}"


if __name__ == "__main__":
    print("=== COMPOSIÇÃO: Escola e SalaDeAula ===")
    escola_a = Escola("Escola Municipal Centro", "12.345.678/0001-90")
    escola_a.adicionar_sala(101, 30)
    escola_a.adicionar_sala(102, 25)
    for sala in escola_a.listar_salas():
        print(" ", sala)

    print("\n=== ASSOCIAÇÃO N:N: Professor e Escola ===")
    escola_b = Escola("Colégio Estadual Norte", "98.765.432/0001-10")
    prof = Professor("Marina Souza", "P-001", "Matemática")
    prof.lecionar_em(escola_a)
    prof.lecionar_em(escola_b)
    print(" ", prof)
    print(" ", escola_a)

    print("\n=== AGREGAÇÃO: Aluno e Endereco ===")
    end = Endereco("Rua das Flores", 45, "Centro",
                   "Parnaíba", "PI", "64200-000")
    aluno = Aluno("João Lima", "2026001", end)
    print(" ", aluno)

    del aluno
    print("  Aluno removido. Endereço ainda existe:", end)
    outro = Aluno("Ana Lima", "2026002", end)
    print(" ", outro)

    print("\n=== Fechando a escola ===")
    escola_a.fechar()
    print("  Salas restantes:", len(escola_a.listar_salas()))
    print(" ", prof)
