from Transacao import Deposito, Saque
from Cliente import PessoaFisica
from Conta import ContaCorrente
import textwrap

class  StartContaBancaria():

    def __init__(self):
        self.clientes = []
        self.contas = []

    def exibir_menu(self):
        menu = """\n
        ================ MENU ================
        [d]\tDepositar
        [s]\tSacar
        [e]\tExtrato
        [nc]\tNova conta
        [lc]\tListar contas
        [nu]\tNovo Cliente
        [q]\tSair
        => """
        return input(textwrap.dedent(menu))
       

    def filtrar_cliente(self, cpf):
        clientes_filtrados = [cliente for cliente in self.clientes if cliente.cpf == cpf]
        return clientes_filtrados[0] if clientes_filtrados else None


    def recuperar_conta_cliente(self, cpf):
        cliente = self.filtrar_cliente(cpf)

        if not cliente.contas:
            print("\n@@@ Cliente não possui conta! @@@")
            return

        # FIXME: não permite cliente escolher a conta
        return cliente.contas[0]


    def depositar(self, cpf, valor):
        # cpf = input("Informe o CPF do cliente: ")
        cliente = self.filtrar_cliente(cpf)

        if not cliente:
            print("\n@@@ Cliente não encontrado! @@@")
            return
        
        conta = self.recuperar_conta_cliente(cpf)
        
        if not conta:
            return        

        # valor = float(input("Informe o valor do depósito: "))
        transacao = Deposito(conta, valor)

        cliente.realizar_transacao(conta, transacao)


    def sacar(self, cpf, valor):
        # cpf = input("Informe o CPF do cliente: ")
        cliente = self.filtrar_cliente(cpf)

        if not cliente:
            print("\n@@@ Cliente não encontrado! @@@")
            return

        conta = self.recuperar_conta_cliente(cpf)

        if not conta:
            return

        # valor = float(input("Informe o valor do saque: "))
        transacao = Saque(conta, valor)

        cliente.realizar_transacao(conta, transacao)


    def exibir_extrato(self, cpf):
        cliente = self.filtrar_cliente(cpf)

        if not cliente:
            print("\n@@@ Cliente não encontrado! @@@")
            return

        conta = self.recuperar_conta_cliente(cpf)

        if not conta:
            return

        print("\n================ EXTRATO ================")
        transacoes = conta.historico.lista_transacoes

        extrato = ""
        if not transacoes:
            extrato = "Não foram realizadas movimentações."
        else:
            for transacao in transacoes:
                extrato += f"\n{transacao.__class__.__name__}:\n\tR$ {transacao.valor:.2f}"

        print(extrato)
        print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
        print("==========================================")


    def criar_cliente(self, cpf, nome, data_nascimento, endereco):
        
        cliente = self.filtrar_cliente(cpf)

        if cliente:
            print("\n@@@ Já existe cliente com esse CPF! @@@")
            return

        cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

        self.clientes.append(cliente)

        print(f'Cliente {nome} criado com sucesso!')


    def criar_conta(self, cpf, saldo=0):
        cliente = self.filtrar_cliente(cpf)

        if not cliente:
            print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
            return

        conta = {}
        if saldo == 0:
            conta = ContaCorrente.nova_conta_zerada(cliente=cliente, limite=1000, limite_saques=5)
        else:
            conta = ContaCorrente.nova_conta_com_saldo(cliente=cliente, limite=1000, limite_saques=5, valor_deposito=saldo )
        
        self.contas.append(conta)
        cliente.adicionar_conta(conta)

        print("\n=== Conta criada com sucesso! ===")


    def listar_contas(self):
        for conta in self.contas:
            print("=" * 100)
            print(textwrap.dedent(str(conta)))    
   
   
    def start(self):
        while True:
            opcao = self.exibir_menu()

            if opcao == "d":
                cpf = input("Informe o CPF do cliente: ")
                valor = float(input("Informe o valor do saque: "))
                self.depositar(cpf, valor)

            elif opcao == "s":
                cpf = input("Informe o CPF do cliente: ")
                valor = float(input("Informe o valor do saque: "))
                self.sacar(cpf, valor)

            elif opcao == "e":
                cpf = input("Informe o CPF do cliente: ")
                self.exibir_extrato(cpf)

            elif opcao == "nu":
                cpf = input("Informe o CPF (somente número): ")
                nome = input("Informe o nome completo: ")
                data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
                endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
                self.criar_cliente(cpf, nome, data_nascimento, endereco)

            elif opcao == "nc":
                cpf = input("Informe o CPF (somente número): ")
                conta = self.criar_conta(cpf=cpf)
                self.contas.append(conta)

            elif opcao == "lc":
                self.listar_contas()

            elif opcao == "q":
                break

            else:
                print("Operação inválida, por favor selecione novamente a operação desejada.")        


    def start_teste(self):
        # teste criando cliente 01
        cpf = "000.000.000-00"
        nome = "Rafael Thomaz"
        data_nascimento = "1983-11-14"
        endereco = "Santa Luzia - MG"
        self.criar_cliente(cpf, nome, data_nascimento, endereco)

        # teste criando cliente 02
        cpf = "111.111.111-11"
        nome = "Mariana Thomaz"
        data_nascimento = "1989-12-25"
        endereco = "Santa Luzia - MG"
        self.criar_cliente(cpf, nome, data_nascimento, endereco)

        # teste filtrar cliente 01
        cpf = "000.000.000-00"
        cliente_01 = self.filtrar_cliente(cpf)
        if cliente_01:
            print(f"cliente {cliente_01.nome} encontrado!!!", cliente_01)
        else:
            print("cliente 01 nao encontrado!")

        # teste filtrar cliente 02
        cpf = "111.111.111-11"
        cliente_02 = self.filtrar_cliente(cpf)
        if cliente_02:
            print(f"cliente {cliente_02.nome} encontrado!!!", cliente_02)
        else:
            print("cliente 01 nao encontrado!")

        # teste filtrar cliente nao cadastrado
        cpf = "111.111.111-00"
        cliente_nao_cadastrado = self.filtrar_cliente(cpf)
        print("cliente nao cadastrado!!", cliente_nao_cadastrado)


        # teste criar conta usuario 01
        cpf = "000.000.000-00"
        self.criar_conta(cpf)
        print("cliente_01", cliente_01)

        # teste criar conta usuario 02
        cpf = "111.111.111-11"
        self.criar_conta(cpf, 1000)
        print("cliente_02", cliente_02)

        # teste recuperar conta cliente
        cpf = "000.000.000-00"
        conta_cliente_01 = self.recuperar_conta_cliente(cpf)
        print("cliente_01 - conta", conta_cliente_01)

        # teste recuperar conta cliente
        cpf = "111.111.111-11"
        conta_cliente_02 = self.recuperar_conta_cliente(cpf)
        print("cliente_02 - conta", conta_cliente_02)

        # teste listar contas
        self.listar_contas()

        # teste depositar cliente 01
        cpf = "000.000.000-00"
        self.depositar(cpf, 100)
        self.depositar(cpf, 150)
        self.sacar(cpf, 200)
        self.depositar(cpf, 250)
        self.sacar(cpf, 100)
        self.exibir_extrato(cpf=cpf)
       

def __main__():
    conta_bancaria = StartContaBancaria()
    conta_bancaria.start()
    # conta_bancaria.start_teste()


__main__()    