from Util import Util
from Transacao import Historico, Saque

class Conta:
    def __init__(self, cliente, valor_deposito_inicial):
        self._numero = Util.get_numero_nova_conta()
        self._agencia = 1

        self._saldo = 0
        if valor_deposito_inicial > 0:
            self.depositar(valor_deposito_inicial)
                
        self._cliente = cliente
        self._historico = Historico()
    
    @classmethod
    def nova_conta_zerada(cls, cliente, limite, limite_saques):
        return cls(cliente, limite, limite_saques, valor_deposito_inicial=0)

    @classmethod
    def nova_conta_com_saldo(cls, cliente, limite, limite_saques, valor_deposito):
        return cls(cliente, limite, limite_saques, valor_deposito_inicial=valor_deposito)

    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia    

    @property
    def saldo(self):
        return self._saldo

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor_saque):
        try:
            if valor_saque <= 0:
                print('Valor de saque deve ser maior que zero.')
                return False

            if valor_saque > self._saldo:
                print('Valor de saque maior que o saldo.')
                return False
                        
            self._saldo -= valor_saque
            return True
        except Exception as e:
            return False

    def depositar(self, valor_deposito):
        try:
            if valor_deposito <= 0:
                print('Deposito falhou, valor deve ser maior que zero!!')
                return False

            self._saldo += valor_deposito
            print('Deposito concluido com sucesso!!')
            return True
                
        except Exception as e:
            return False


class ContaCorrente(Conta):
    def __init__(self, cliente, limite, limite_saques, valor_deposito_inicial):
        super().__init__(cliente, valor_deposito_inicial)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques_realizados = len([transacao for transacao in self.historico.lista_transacoes if transacao.__class__.__name__ == Saque.__name__])

        if valor > self._limite:
            print('A operação falhou, o valor do saque excedeu o limite!!')
            return False
        
        if numero_saques_realizados > self._limite_saques:
            print('A operação falhou, o número de saques excedeu o limite!!')
            return False

        super().sacar(valor)
        return True
    
    def __str__(self):
        return f'Agencia: {self.agencia}, Conta: {self.numero}, Cliente: {self.cliente.nome}, Saldo: {self.saldo}'
