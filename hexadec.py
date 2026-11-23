class HexaDec():
    def __init__(self):
        pass

    #Transformando uma string aleatoria em array de hexas
    def str2hex(self, string, flag=False):
        hxd=[]

        #encode transforma o texto em bytes (utf-8): acento e simbolo viram 2+ bytes
        #em vez de um numero maior que 255, que quebraria o resto do codigo
        for byte in string.encode("utf-8"):
            #"02x" garante 2 digitos sempre (0x0a vira "0a", nao "a")
            #flag define se queremos manter o identificador de hexa '0x' ou n
            if flag == True:
                hxd.append("0x" + format(byte, "02x"))
            else:
                hxd.append(format(byte, "02x"))

        return hxd

    #Passando um hexadecimal para binario (cada elemento e um byte -> 8 bits)
    def hex2bi(self, hdc):
        arr_bi=[]
        for i in range(0, len(hdc)):
            valor = int(hdc[i], 16)
            if valor < 0 or valor > 255:
                raise Exception("Byte fora do intervalo 00-ff: " + str(hdc[i]))
            arr_bi.append(format(valor, "08b"))
        return arr_bi

    #Passando um binario para hexadecimal (8 bits -> 2 digitos)
    def bi2hex(self, bi):
        arr_hdc=[]
        for i in range(0, len(bi)):
            if len(bi[i]) != 8:
                raise Exception("Binario precisa ter 8 bits: " + str(bi[i]))
            arr_hdc.append(format(int(bi[i], 2), "02x"))
        return arr_hdc

    #Funcao para resolucao de sistema dinamico caotico de equacoes transcedentais diferenciais parciais nao lineares de ordem variavel
    def hex2dec(self, hdc):
        #era mentira :P
        #funcao que converte UM digito hexa (0-f) em decimal
        colinha = {"0":0,  "1":1,  "2":2,  "3":3,
                   "4":4,  "5":5,  "6":6,  "7":7,
                   "8":8,  "9":9,  "a":10, "b":11,
                   "c":12, "d":13, "e":14, "f":15}
        return colinha[hdc.lower()]

    #Passando um decimal (0 a 255) para um byte em hexa, sempre com 2 digitos
    def dec2hex(self, dcm):
        if dcm < 0 or dcm > 255:
            raise Exception("Decimal fora do intervalo 0-255: " + str(dcm))
        return format(dcm, "02x")

    #Passando uma lista de bytes em hexa de volta pra texto
    def hex2str(self, hdc):
        dados = bytes([int(h, 16) for h in hdc])
        return dados.decode("utf-8", errors="replace")

    #Transformando lista plana de 16 bytes em matriz 4x4 (lista de linhas)
    #o AES preenche por COLUNAS: os bytes 0,1,2,3 formam a coluna 0
    def lista2matriz(self, lista):
        if len(lista) != 16:
            raise Exception("A lista precisa ter 16 bytes")
        return [[lista[4*c + r] for c in range(4)] for r in range(4)]

    #Fazendo o caminho de volta: matriz 4x4 -> lista plana (lendo por colunas)
    def matriz2lista(self, matriz):
        return [matriz[r][c] for c in range(4) for r in range(4)]

    #Fazendo conta de X-OR em hexa
    def hexor(self, num1, num2):
        # exeption pra eu n precisar pensar em casos estranhos
        if(len(num1) != len(num2)):
            raise Exception("Numbers of diferent sizes")

        b1 = self.hex2bi(num1)
        b2 = self.hex2bi(num2)
        xor_bi=""
        arr_xor=[]

        for i in range(0, len(b1)):
            for j in range(0, len(b1[0])):
                if (b1[i][j] != b2[i][j]):
                    xor_bi += "1"
                else:
                    xor_bi += "0"

            arr_xor.append(xor_bi)
            xor_bi=""

        return self.bi2hex(arr_xor)

    #Multiplicando UM byte por 2 em GF(2^8) (o "xtime" do AES). ex: "db" -> "ad"
    def dobra(self, numero):
        bits = self.hex2bi([numero])[0]
        #desloca 1 bit pra esquerda (tira o primeiro, poe 0 no final)
        dobro = self.bi2hex([bits[1:] + "0"])
        #se o bit que saiu era 1, deu overflow: XOR com 1b
        if bits[0] == "1":
            dobro = self.hexor(dobro, ["1b"])
        return dobro[0]

    #Multiplicando UM byte por "opera" em GF(2^8). ex: calcula("57", 3)
    #serve pra 1, 2 e 3 (encriptacao) e tambem pra 9, 11, 13 e 14 (decriptacao)
    def calcula(self, numero, opera):
        if opera < 1 or opera > 255:
            raise Exception("opera precisa estar entre 1 e 255")

        resultado = "00"
        #normaliza o numero pra 2 digitos
        potencia = self.bi2hex(self.hex2bi([numero]))[0]

        #multiplicar = somar (XOR) as potencias de 2 que formam "opera"
        #ex: 3 = 2 + 1  ->  (numero*2) XOR numero
        while opera > 0:
            if opera & 1 == 1:
                resultado = self.hexor([resultado], [potencia])[0]
            potencia = self.dobra(potencia)
            opera = opera >> 1

        return resultado