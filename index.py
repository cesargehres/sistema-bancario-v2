def validar_num(min, max, num):
        if (num >= min) and (num <= max):
            return num
        else:
            return False


def validar_int(msg):
    while True:
        num = str(input(msg))
        if num.isdecimal():
            return int(num)
        else:
            print('Erro! Digite um número inteiro.')


def verificar_conta(agencia, nconta, cpf): #Verifica se a conta já existe
    conta_existe = False
    for conta in contas:
        if (agencia in conta['agência']) and (nconta in conta['número de conta']) and (cpf in conta['usuário']):
            conta_existe = True
    return conta_existe


def verificar_usuario(cpf): #Verifica se o usuario existe
    usuario_existe = False
    for usuario in usuarios:
        if cpf in usuario['cpf']:
            usuario_existe = True
    return usuario_existe


def verificar_login(cpf, agencia, conta): #Função de Login
    ncpf = verificar_usuario(cpf)
    if ncpf == False:
        print("CPF não registrado, registre um novo usuário.")
        return False
    else:
        nconta = verificar_conta(agencia, conta, cpf)
        if (nconta != False):
            return conta
        else:
            print('Conta inexistente.')
            return False


def saque(*, valor, conta):#Função para o saque
    saldo = extrato_contas[conta][0]
    saques = int(n_saques[conta])
    if saques >= 3:
        print('Limite de saques diário excedido.')
    elif (float(valor) < 1):
        print('Valor mínimo para saque: R$ 1.00')
    elif (float(valor) > 500):
        print('Valor maximo de saque: R$ 500.00')
    elif (saldo >= float(valor)):
        novo_saldo = float(saldo) - float(valor)
        extrato_contas[conta][0] = novo_saldo
        n_saques[conta] += 1
        extrato_contas[conta].append(str(f'- R$ {float(valor):.2f}'))
        return saldo, extrato(conta)
    elif (saldo < float(valor)):
        print('Saldo insuficiente!.')


def deposito(valor, conta,/):#Função para o depósito
    if (float(valor) < 1):
        print('Valor mínimo para depósito: R$ 1.00')
    else:
        saldo = extrato_contas[conta][0]
        novo_saldo = float(saldo) + float(valor)
        extrato_contas[conta][0] = novo_saldo
        extrato_contas[conta].append(str(f'+ R$ {float(valor):.2f}'))


def extrato(conta, /):#Imprime o extrato
    print('--------- Extrato ----------')
    for c in range(0, len(extrato_contas[conta])):
        if c > 0:
            print(f'{extrato_contas[conta][c]}')
    print(f'Saldo: R$ {extrato_contas[conta][0]:.2f}')


def str_data_nascimento():#Cria uma string com a data de nascimento
    dia = validar_int('Dia: ')
    mes = validar_int('Mes: ')
    ano = validar_int('Ano: ')
    data = f'{str(dia)}/{str(mes)}/{str(ano)}'
    return data


def dicionario_endereco():#Cria um dicionário com o endereço
    logradouro = str(input('Logradouro: ')).title()
    nro = validar_int('Número: ')
    bairro = str(input('Bairro: ')).title()
    endereco = {'logradouro': logradouro, 'nro': str(nro), 'bairro': bairro}
    return endereco


def cadastrar_usuario(cpf): #Cria um dicionario como o novo usuario
    nome = str(input('Nome: ')).title()
    nascimento = str_data_nascimento()
    endereco = dicionario_endereco()
    usuario = {'nome': nome,'cpf': cpf, 'nascimento': nascimento, 'endereço': endereco}
    return usuario


def novo_numero_conta(): #Gera numero de conta formatado com 4 numeros
    numero_conta = str(len(contas) + 1)
    while len(numero_conta) <= 3:
        numero_conta = '0' + numero_conta
    return numero_conta


def cadastrar_conta(cpf): #cadastra nova conta
    novo_extrato(novo_numero_conta())
    novo_nsaques(novo_numero_conta())
    nova_conta = {'agência': '0001', 'número de conta': novo_numero_conta(), 'usuário': cpf}
    return nova_conta


def novo_nsaques(conta): #Cria dicionario para o numero limite de saques
    n_saques[conta] = 0



def novo_extrato(conta):
    extrato_contas[conta] = [float(0)]


#Programa principal

usuarios = [ #usuários registrados no banco
    {'nome': 'César Augusto Gehres', 'nascimento': '05/03/2000', 'cpf': '03268525067',
     'endereço': {'logradouro': 'Silvio Pinto', 'nro': '223', 'bairro': 'Rincão Comprido'}},
    {'nome': 'Elenita Édina da Silva', 'nascimento': '05/06/1975', 'cpf': '12345678910',
     'endereço': {'logradouro': 'Silvio Pinto', 'nro': '223', 'bairro': 'Rincão Comprido'}}
]

contas = [ #contas dos usuários registrados
    {'agência': '0001', 'número de conta': '0001', 'usuário': '03268525067'},
    {'agência': '0001', 'número de conta': '0002', 'usuário': '12345678910'}
]

extrato_contas = { #variavel para armazenar o saldo e o historico de movimentações da conta
    '0001': [float(100.00), str('+ R$ 100.00')], '0002': [float(5000.00), str('+ R$ 10000.00'), str('-5000.00')]
}

n_saques = {'0001': 0, '0002': 0}

menu_login_str = """----------------------------
[1] Login
[2] Cadastrar novo usuário
[3] Cadastrar nova conta bancária
[4] Sair
----------------------------"""

menu_str = """----------------------------
[1] Saque
[2] Depósito
[3] Extrato
[4] Sair
----------------------------"""

#Programa principal
while True:
    print(menu_login_str) #Tela de Login e registrar usuario.
    op = validar_int('Selecione uma operação: ') #Chama função para validar se é numero inteiro.
    if validar_num(1, 4, op) == False:#chama função para validar se é uma escolha válida.
        print('Erro! Selecione uma opção válida.')

    if op == 1: #Login
        sair = False
        while sair != True:
            cpf = str(input('CPF: '))
            agencia = str(input('Agencia: '))
            conta = str(input("Conta: "))
            login = verificar_login(cpf, agencia, conta) #Chama função login para achar a conta e validala.

            if login == False:
                break

            else: #Se a conta existe, então podera movimentar a conta
                while True:
                    print(menu_str)
                    op = validar_int('Selecione uma operação: ')  # Chama função para validar se é numero inteiro.
                    if validar_num(1, 4, op) == False:  # chama função para validar se é uma escolha válida.
                        print('Erro! Selecione uma opção válida.')

                    if op == 1: #Saque
                        valor = str(input('Valor: '))
                        saque(valor=valor, conta=conta) #Chama função saque
                        print(extrato_contas)


                    elif op == 2: #Depósito
                        valor = str(input('Valor:'))
                        deposito(valor, conta)
                        print(extrato_contas)
                    elif op == 3: #Extrato
                        extrato(conta)
                    elif op == 4: #Sair
                        sair = True
                        break
    elif op == 2: #Registrar novo usuário.
        cpf = str(input('Digite seu CPF: '))
        if verificar_usuario(cpf) == True:
            print('Esse usuario já está registrado.')
            continue
        else:    #cadastra novo usuario e nova conta
            novo_usuario = cadastrar_usuario(cpf)
            numero_conta = novo_numero_conta()
            usuarios.append(novo_usuario)
            nova_conta = cadastrar_conta(cpf)
            contas.append(nova_conta)
            print('Usuário criado com sucesso!')
            print('Nova conta criada com sucesso!')
            print(f'Agencia: 0001\nNúmero da conta: {numero_conta}')
    elif op == 3:
        cpf = str(validar_int('CPF: '))
        verificar = verificar_usuario(cpf)
        if verificar == True:
            print('Nova conta criada com sucesso!')
            nova_conta = cadastrar_conta(cpf)
            contas.append(nova_conta)
            print('Nova conta criada com sucesso!')
            print(f'Agencia: 0001\nNúmero da conta: {novo_numero_conta()}')
            print(contas)
        else:
            print('Usuário inexistente.')
    elif op == 4:
        break
