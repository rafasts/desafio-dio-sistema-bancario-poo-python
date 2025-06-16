class Util:
    conta = 0

    @staticmethod
    def get_numero_nova_conta():
        Util.conta += 1
        return Util.conta
    
# # # teste classe estatica
# print(Util.get_numero_nova_conta())
# print(Util.get_numero_nova_conta())
# print(Util.get_numero_nova_conta())
# print(Util.get_numero_nova_conta())