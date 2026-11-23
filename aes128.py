from hexadec import HexaDec
import numpy as np

class AES128(HexaDec):
    def __init__(self, texto, chave):
        # vou admitir, isso aqui foi o chat kkkkkkk (256 valores n da n po)
        self.S_box = [["63", "7c", "77", "7b", "f2", "6b", "6f", "c5", "30", "01", "67", "2b", "fe", "d7", "ab", "76"],
                    ["ca", "82", "c9", "7d", "fa", "59", "47", "f0", "ad", "d4", "a2", "af", "9c", "a4", "72", "c0"],
                    ["b7", "fd", "93", "26", "36", "3f", "f7", "cc", "34", "a5", "e5", "f1", "71", "d8", "31", "15"],
                    ["04", "c7", "23", "c3", "18", "96", "05", "9a", "07", "12", "80", "e2", "eb", "27", "b2", "75"],
                    ["09", "83", "2c", "1a", "1b", "6e", "5a", "a0", "52", "3b", "d6", "b3", "29", "e3", "2f", "84"],
                    ["53", "d1", "00", "ed", "20", "fc", "b1", "5b", "6a", "cb", "be", "39", "4a", "4c", "58", "cf"],
                    ["d0", "ef", "aa", "fb", "43", "4d", "33", "85", "45", "f9", "02", "7f", "50", "3c", "9f", "a8"],
                    ["51", "a3", "40", "8f", "92", "9d", "38", "f5", "bc", "b6", "da", "21", "10", "ff", "f3", "d2"],
                    ["cd", "0c", "13", "ec", "5f", "97", "44", "17", "c4", "a7", "7e", "3d", "64", "5d", "19", "73"],
                    ["60", "81", "4f", "dc", "22", "2a", "90", "88", "46", "ee", "b8", "14", "de", "5e", "0b", "db"],
                    ["e0", "32", "3a", "0a", "49", "06", "24", "5c", "c2", "d3", "ac", "62", "91", "95", "e4", "79"],
                    ["e7", "c8", "37", "6d", "8d", "d5", "4e", "a9", "6c", "56", "f4", "ea", "65", "7a", "ae", "08"],
                    ["ba", "78", "25", "2e", "1c", "a6", "b4", "c6", "e8", "dd", "74", "1f", "4b", "bd", "8b", "8a"],
                    ["70", "3e", "b5", "66", "48", "03", "f6", "0e", "61", "35", "57", "b9", "86", "c1", "1d", "9e"],
                    ["e1", "f8", "98", "11", "69", "d9", "8e", "94", "9b", "1e", "87", "e9", "ce", "55", "28", "df"],
                    ["8c", "a1", "89", "0d", "bf", "e6", "42", "68", "41", "99", "2d", "0f", "b0", "54", "bb", "16"]]
        
        self.text = self.str2hex(texto)
        self.key = self.str2hex(chave)

        self.start = [texto, chave]
        self.round = 0
        self.keys = [self.str2hex(chave)]
        self.rnd_const = ["01", "02", "04", "08", "10", "20", "40", "80", "1b", "36"]
        self.gera_inv_sbox()
        
        

    def encriptar(self):
        for i in range(10):
            self.change_key(self.keys[i])
            
        self.text = self.add_roundkey(self.text,self.keys[0])
        for i in range(1,10):
            self.text = self.subSbox(self.text)
            self.text = self.shiftRows(self.text)
            self.text = self.mixColumns(self.text)
            self.text = self.add_roundkey(self.text, self.keys[i])
        
        self.text = self.subSbox(self.text)
        self.text = self.shiftRows(self.text)
        self.text = self.add_roundkey(self.text, self.keys[10])  
        
    def decriptar(self):
        self.text = self.add_roundkey(self.text, self.keys[10])
        self.text = self.invShiftRows(self.text)
        self.text = self.invSubBytes(self.text)
        for i in range(9,0,-1):
            self.text = self.add_roundkey(self.text, self.keys[i])
            self.text = self.invMixColumns(self.text)
            self.text = self.invShiftRows(self.text)
            self.text = self.invSubBytes(self.text)
        self.text = self.add_roundkey(self.text, self.keys[0]) 
            
    def shiftRows(self, htex):
        ftexto = []
        
        r0 = []
        r1 = []
        r2 = []
        r3 = []
        
        for i in range(4):
            r0.append(htex[i*4])
            r1.append(htex[((i + 1)%4)*4 + 1])
            r2.append(htex[((i + 2)%4)*4 + 2])
            r3.append(htex[((i + 3)%4)*4 + 3])
            
        for i in range(4):
            ftexto.append(r0[i])
            ftexto.append(r1[i])
            ftexto.append(r2[i])
            ftexto.append(r3[i])
            
        return ftexto
        
    def mixColumns(self, htex):
            ftexto = []
            matriz = [
                [2, 3, 1, 1],
                [1, 2, 3, 1],
                [1, 1, 2, 3],
                [3, 1, 1, 2]
            ]
            for m in range(4):
                coluna = htex[m*4:m*4+4]
                for i in range(4):
                    linha = matriz[i]
                    # comeca em "00" (XOR com 0 nao muda nada) e acumula como LISTA,
                    # porque o hexor trabalha com listas de bytes
                    soma = ["00"]
                    for j in range(4):
                        soma = self.hexor(soma, [self.calcula(coluna[j], linha[j])])
                    ftexto.append(soma[0])
            return ftexto
            
        
                

    def subSbox(self, hdc):
        new_hdc=[]
        for i in range(0, len(hdc)):
            linha = self.hex2dec(hdc[i][0])
            coluna = self.hex2dec(hdc[i][1])
            new_hdc.append(self.S_box[linha][coluna])

        return new_hdc

    def gera_inv_sbox(self):
        self.inv_sbox = {}
        for linha in range(16):
            for coluna in range(16):
                self.inv_sbox[self.S_box[linha][coluna]] = self.dec2hex(linha*16 + coluna)
        return self.inv_sbox

    def invShiftRows(self, htex):
        ftexto = []
        
        r0 = []
        r1 = []
        r2 = []
        r3 = []
        
        for i in range(4):
            r0.append(htex[i*4])
            r1.append(htex[((i + 3)%4)*4 + 1])
            r2.append(htex[((i + 2)%4)*4 + 2])
            r3.append(htex[((i + 1)%4)*4 + 3])
            
        for i in range(4):
            ftexto.append(r0[i])
            ftexto.append(r1[i])
            ftexto.append(r2[i])
            ftexto.append(r3[i])
            
        return ftexto

    def invMixColumns(self, htex):
            ftexto = []
            matriz = [
                [14, 11, 13,  9],
                [9,  14, 11, 13],
                [13, 9,  14, 11],
                [11, 13,  9, 14]
            ]
            for m in range(4):
                coluna = htex[m*4:m*4+4]
                for i in range(4):
                    linha = matriz[i]
                    # comeca em "00" (XOR com 0 nao muda nada) e acumula como LISTA,
                    # porque o hexor trabalha com listas de bytes
                    soma = ["00"]
                    for j in range(4):
                        soma = self.hexor(soma, [self.calcula(coluna[j], linha[j])])
                    ftexto.append(soma[0])
            return ftexto
        
    def invSubBytes(self, hdc):
        

        new_hdc=[]
        for i in range(0, len(hdc)):
            if hdc[i] not in self.inv_sbox:
                raise Exception("Byte invalido (use 2 digitos minusculos): " + str(hdc[i]))
            new_hdc.append(self.inv_sbox[hdc[i]])

        return new_hdc

    def func_g(self, hdc):
        #puxa pra esquerda
        hdc = [hdc[1],hdc[2],hdc[3],hdc[0]]
        #substitui na S_box
        hdc = self.subSbox(hdc)
        #xor com a constante de round
        hdc = self.hexor(hdc, [self.rnd_const[self.round], "00", "00", "00"])

        self.round += 1
        return hdc

    def change_key(self, prev_key):
        w0 = prev_key[0:4]
        w1 = prev_key[4:8]
        w2 = prev_key[8:12]
        w3 = prev_key[12:16]
        w_especial = self.func_g(w3)
        w4 = self.hexor(w0,w_especial)
        w5 = self.hexor(w1, w4)
        w6 = self.hexor(w2, w5)
        w7 = self.hexor(w3, w6)

        new_key = w4+w5+w6+w7
        self.keys.append(new_key)
        
        return new_key

    def change_text(self, htex, hkey):
        sum = self.hexor(htex, hkey)
        subs = self.subSbox(sum)
        arr = np.array([[subs[0:4]],[subs[4:8]],[subs[8:12]],[subs[12:16]]]).T

        shifts=0
        for i in range(0,4):
            active_row = np.copy(arr[i,0])
            #active_row = arr[i,0] da problema de ponteiro
            for j in range(0,4):
                arr[i][0][j] = active_row[(j+shifts)%4]
            shifts+=1
        
        return arr
        
    def add_roundkey(self, htex, hkey):
        return self.hexor(htex, hkey)


a = AES128("Two One Nine Two", "Thats my Kung Fu")


print(a.hex2str(a.text))
a.encriptar()
print(a.text)
a.decriptar()
print(a.hex2str(a.text))
#print(a.keys)
#print(a.hex2str(a.text))

#print(a.change_text(['ee', 'd9', 'fc', 'de', '81', 'f9', '98', 'bb', 'a1', '9f', 'fd', 'd6', 'c3', 'f0', '84', 'a5'],
#                  ['aa', 'cc', '12', '65', '59', '78', '15', '19', '45', '05', '07', '89', '65', '45', '12', '36']))