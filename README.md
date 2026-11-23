# AES-128 em Python

Implementação do AES-128 (FIPS-197) em Python. Encripta e decripta **um bloco de 16 bytes**
com uma chave de 16 bytes. As contas em hexa, binário e GF(2⁸) são feitas passo a passo no
código, sem usar bibliotecas de criptografia.

## Arquivos

| Arquivo | O que tem |
|---------|-----------|
| `hexadec.py` | Classe `HexaDec`: conversões entre texto, hexa, binário e decimal, XOR em hexa e multiplicação em GF(2⁸) |
| `aes128.py` | Classe `AES128` (herda de `HexaDec`): rodadas, S-box, expansão da chave, encriptação e decriptação |

## Requisitos

- Python 3
- numpy (usado apenas na função `change_text`)

```bash
pip install numpy
```

## Como executar

Os dois arquivos precisam estar na mesma pasta.

```bash
python aes128.py
```

O final do `aes128.py` tem um exemplo que encripta `Two One Nine Two` com a chave
`Thats my Kung Fu`, decripta de volta e mostra o resultado de `change_text`:

```
Two One Nine Two
['29', 'c3', '50', '5f', '57', '14', '20', 'f6', '40', '22', '99', 'b3', '1a', '02', 'd7', '3a']
Two One Nine Two
[[['1b' '61' '69' '24']]

 [['0c' 'b8' 'd5' '59']]

 [['2d' '90' '28' '5d']]

 [['dc' 'ea' '3a' 'cf']]]
```

A segunda linha é o texto cifrado (`29c3505f571420f6402299b31a02d73a` em hexa).

## Como usar no código

```python
from aes128 import AES128

a = AES128("Two One Nine Two", "Thats my Kung Fu")

a.encriptar()
print(a.text)                # texto cifrado, lista de 16 bytes em hexa

a.decriptar()
print(a.hex2str(a.text))     # Two One Nine Two
```

Obs.: o exemplo no final do `aes128.py` roda sempre que o arquivo é importado.

## Como funciona

O texto e a chave são convertidos em listas de 16 bytes, cada byte uma string de 2 dígitos
hexa (`"0a"`, `"ff"`). O estado é lido **por colunas**: os bytes 0, 1, 2 e 3 formam a
coluna 0, e assim por diante.

```
Encriptar                          Decriptar
─────────                          ─────────
AddRoundKey (chave 0)              AddRoundKey (chave 10)
9 rodadas:                         InvShiftRows
    SubBytes                       InvSubBytes
    ShiftRows                      9 rodadas:
    MixColumns                         AddRoundKey
    AddRoundKey                        InvMixColumns
rodada final:                          InvShiftRows
    SubBytes                           InvSubBytes
    ShiftRows                      AddRoundKey (chave 0)
    AddRoundKey (chave 10)
```

- **Expansão da chave:** `encriptar` gera as 10 chaves seguintes a partir da chave original
  (`change_key`, que usa `func_g` e as constantes de round) e as guarda em `keys`.
- **MixColumns / InvMixColumns:** multiplicam cada coluna por uma matriz em GF(2⁸), usando
  `calcula` e `dobra` de `HexaDec`.
- **Decriptação:** usa as chaves geradas na encriptação e a S-box inversa (`gera_inv_sbox`).

## Métodos

### `HexaDec` (`hexadec.py`)

| Método | O que faz |
|--------|-----------|
| `str2hex(string, flag=False)` | Texto → lista de bytes em hexa (UTF-8). Com `flag=True` mantém o `0x` |
| `hex2str(hdc)` | Lista de bytes em hexa → texto |
| `hex2bi(hdc)` / `bi2hex(bi)` | Bytes em hexa ↔ strings de 8 bits |
| `hex2dec(hdc)` | Um dígito hexa (0-f) → decimal |
| `dec2hex(dcm)` | Decimal (0 a 255) → byte em hexa com 2 dígitos |
| `lista2matriz(lista)` / `matriz2lista(matriz)` | Lista de 16 bytes ↔ matriz 4x4 (por colunas) |
| `hexor(num1, num2)` | XOR byte a byte entre duas listas de mesmo tamanho |
| `dobra(numero)` | Multiplica um byte por 2 em GF(2⁸) |
| `calcula(numero, opera)` | Multiplica um byte por `opera` (1 a 255) em GF(2⁸) |

### `AES128` (`aes128.py`)

| Método | O que faz |
|--------|-----------|
| `encriptar()` | Encripta `self.text` |
| `decriptar()` | Decripta `self.text` |
| `subSbox(hdc)` / `invSubBytes(hdc)` | Substituição pela S-box e pela S-box inversa |
| `shiftRows(htex)` / `invShiftRows(htex)` | Rotação das linhas do estado (esquerda / direita) |
| `mixColumns(htex)` / `invMixColumns(htex)` | Mistura das colunas e sua inversa |
| `add_roundkey(htex, hkey)` | XOR do estado com a chave da rodada |
| `gera_inv_sbox()` | Monta a S-box inversa |
| `func_g(hdc)` | Função g da expansão da chave |
| `change_key(prev_key)` | Gera a próxima chave de rodada |
| `change_text(htex, hkey)` | Faz AddRoundKey, SubBytes e ShiftRows e devolve a matriz 4x4 (numpy) |

## Cuidados ao usar

- Texto e chave precisam ter **exatamente 16 bytes**. Acentos e símbolos contam como 2 ou mais
  bytes (`"coração"` tem 9 bytes, não 7). Com outro tamanho, o código dá erro.
- Chame `encriptar()` **antes** de `decriptar()`: é a `encriptar` que gera as chaves de rodada.
- Cada objeto `AES128` encripta uma vez. Para encriptar de novo, crie outro objeto.
- Só trabalha com um bloco, sem modo de operação (ECB, CBC...) nem padding, e só com AES-128.
- Feito para estudar o algoritmo: é lento e não deve ser usado para proteger dados reais.

## Referências

- [FIPS-197: Advanced Encryption Standard (AES)](https://csrc.nist.gov/publications/detail/fips/197/final)