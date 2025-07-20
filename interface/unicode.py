lower_caracteres_especiais = "áéíóúãâêîôûàèìòùäëïöüåæç"
upper_caracteres_especiais = "ÁÉÍÓÚÃÂÊÎÔÛÀÈÌÒÙÄËÏÖÜÅÆÇ"
caracteres = lower_caracteres_especiais + upper_caracteres_especiais

# Armazena os binários de cada caractere
binary_caracteres = []

print("Caracteres e seus binários em UTF-8:\n")

for c in caracteres:
    utf8_bytes = c.encode('utf-8')  # Codifica corretamente
    binarios = ' '.join(f"{byte:08b}" for byte in utf8_bytes)
    binary_caracteres.append(binarios)
    print(f"{c} = {binarios}")

def binario_para_string(binario, encoding='utf-8'):
    """
    Recebe uma string binária com bytes separados por espaço (ex: '11000011 10100111')
    e retorna o caractere correspondente.
    """
    try:
        byte_list = [int(b, 2) for b in binario.strip().split()]
        return bytes(byte_list).decode(encoding)
    except Exception as e:
        print(f"[Erro] Falha ao converter: {e}")
        return None


converted_caracteres = []

print("\nConversão de volta:\n")
for b in binary_caracteres:
    caractere = binario_para_string(b)
    print(f"{b} = {caractere}")
    converted_caracteres.append(caractere)

binary_caracteres.sort()
converted_caracteres.sort()



print("\nListas ordenadas:\n")
for i in range(len(binary_caracteres)):
    print(f"{converted_caracteres[i]} = {binary_caracteres[i]}")



upper_strings = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
lower_strings = "abcdefghijklmnopqrstuvwxyz"
main_strings = upper_strings + lower_strings

binary_main_strings = []
count = 0
for character in main_strings:
    utf8_bytes = character.encode('utf-8')  # Codifica corretamente
    binarios = ' '.join(f"{byte:08b}" for byte in utf8_bytes)
    binary_main_strings.append(binarios)
    print(f"{character} = {binarios}, {65+count}")
    count+=1

print(f"First position = {main_strings[0]} = {binary_main_strings[0]}\n")

def binario_para_caractere(binario):
    """
    Recebe string binária tipo '11000011 10101001' e retorna o caractere.
    """
    bytes_list = [int(b, 2) for b in binario.strip().split()]
    return bytes(bytes_list).decode('utf-8')

def offset_special_character(binario):
    """
    Recebe string binária de um caractere e calcula o offset em relação a 'A'
    """
    caractere = binario_para_caractere(binario)
    return ord(caractere) - ord(main_strings[0])

absolute_positions = []
offset_positions = []

# Exemplo com binary_caracteres
for bin_str in binary_caracteres:
    try:
        offset = offset_special_character(bin_str)
        print(f"{bin_str} → Offset = {offset}, Posição Absoluta = {offset + 65}")
        absolute_positions.append(offset + 65)
        offset_positions.append(offset)
    except Exception as e:
        print(f"Erro com {bin_str}: {e}")
 
quantidade_faltante = 0 
 # Verificar quais caracteres faltam
for i in range(192, 252, 1):
    if i not in absolute_positions:
        quantidade_faltante += 1
        char = chr(i)
        print(f"Caractere {i} não encontrado. Caractere: {char} -> Binário: {char.encode('utf-8')}")

print(f"\nQuantidade de caracteres faltando: {quantidade_faltante}")

caracteres_completos = ''.join(chr(i) for i in range(192, 256))
binary_caracteres = [' '.join(f"{byte:08b}" for byte in c.encode('utf-8')) for c in caracteres_completos]

print("\nCaracteres completos e seus binários:\n")
for i in range(len(caracteres_completos)):
    print(f"{caracteres_completos[i]} = {binary_caracteres[i]}, {i+192}")

print("\nCaracteres completos e seus binários:\n")
for i in range(len(caracteres_completos)):
    print(caracteres_completos[i], end='')  # Não quebra a linha
print()  # Quebra a linha só no final


