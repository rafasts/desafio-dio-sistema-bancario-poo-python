from abc import ABC, abstractmethod
from datetime import datetime

class ITransacao(ABC):
    def __init__(self, conta, valor):
        self._conta = conta
        self._valor = valor
        self._data_transacao = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    @property
    def conta(self):
        return self._conta

    @property
    def valor(self):
        return self._valor
    
    @property
    def data_transacao(self):
        return self._data_transacao

    @abstractmethod
    def registrar(self, conta):
        pass

    def __str__(self):
        return f'Tipo: {self.__class__.__name__}, Data transação: {self.data_transacao}, Conta: {self._conta}, Valor: {self._valor}'


class Deposito(ITransacao):
    def __init__(self, conta, valor):
        super().__init__(conta, valor)

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Saque(ITransacao):
    def __init__(self, conta, valor):
        super().__init__(conta, valor)

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)        


class Historico:
    def __init__(self):
        self._lista_transacoes = []

    @property
    def lista_transacoes(self):
        return self._lista_transacoes

    def adicionar_transacao(self, transacao):
        self._lista_transacoes.append(transacao)

    def extrato(self):
        print('==================Extrato==================')
        [print(transacao) for transacao in self._lista_transacoes]



# # teste transacoes e historico
# deposito1 = Deposito('0001', 1000)        
# deposito2 = Deposito('0001', 1500)        
# deposito3 = Deposito('0001', 2000)        
# saque1 = Saque('0001', 2000)        

# historico = Historico()
# historico.lista_transacoes.append(deposito1)
# historico.lista_transacoes.append(deposito2)
# historico.lista_transacoes.append(deposito3)
# historico.lista_transacoes.append(saque1)
# historico.extrato()