import re

def valida_cnpj_alfanumerico(cnpj_completo):
    """
    Valida um CNPJ alfanumérico de 14 caracteres.
    A regra de conversão é: A=17, B=18, C=19... e os números de 0 a 9 mantêm seu valor.
    """

    # Converte a string para maiúsculas e remove espaços para padronizar
    cnpj_completo = cnpj_completo.upper().strip()
    # transforma em maiusculos e retira os espaços em branco

    # 1. Verifica o formato: 12 caracteres alfanuméricos + 2 numéricos
    # A expressão regular (regex) garante que a string tem o formato correto.
    padrao_regex = r"^[A-Z0-9]{12}[0-9]{2}$"
    if not re.match(padrao_regex, cnpj_completo):
        print("ERRO: Formato inválido. O CNPJ deve ter 14 caracteres, com os 2 últimos sendo numéricos.")
        return False

    # Separa a base (os 12 primeiros caracteres) e os DVs (os 2 últimos)
    cnpj_base = cnpj_completo[:12]
    dvs_fornecidos = cnpj_completo[12:]

    def calcular_dv(base):
        """Calcula um único dígito verificador para a base fornecida."""

        def char_para_valor(char):
            """Converte um caractere para um valor numérico seguindo a regra personalizada."""
            if char.isdigit():
                return int(char)
            else:
                # Regra: A=17, B=18, C=19...
                return ord(char) - ord('A') + 17
                """ord() retorna o valor ASC 65."""

        soma = 0
        peso = 2  # O peso inicial para a soma ponderada
        # Percorre a base de trás para frente
        for i in range(len(base) - 1, -1, -1):
            valor = char_para_valor(base[i])
            soma += valor * peso
            peso += 1  # Incrementa o peso
            if peso > 9:
                peso = 2  # Reseta o peso para 2 se ele ultrapassar 9

        # Calcula o resto da divisão da soma por 11
        resto = soma % 11
        # Se o resto for menor que 2, o DV é 0; caso contrário, é 11 menos o resto
        dv = 0 if resto < 2 else 11 - resto
        
        return str(dv)

    # 2. Calcula os dígitos verificadores com a nossa regra
    dv1_calculado = calcular_dv(cnpj_base)
    base_com_dv1 = cnpj_base + dv1_calculado
    dv2_calculado = calcular_dv(base_com_dv1)
    
    dvs_calculados = dv1_calculado + dv2_calculado

    # 3. Compara os DVs fornecidos com os calculados para a validação final
    if dvs_calculados == dvs_fornecidos:
        print(f"O CNPJ '{cnpj_completo}' é VÁLIDO. DVs corretos: {dvs_calculados}")
        return True
    else:
        print(f"O CNPJ '{cnpj_completo}' é INVÁLIDO. DVs corretos seriam: {dvs_calculados}")
        return False

# --- Exemplos de uso ---
print("--- Testando CNPJs com a sua regra de cálculo ---")

# Exemplo com a base "ABCDEFGHIJKL" e DVs "62"
print("\nVerificando o CNPJ com DVs corretos:")
valida_cnpj_alfanumerico("ABCDEFGHIJKL62") 

# Exemplo com os DVs incorretos (o "80" que você mencionou)
print("\nVerificando o CNPJ com DVs incorretos:")
valida_cnpj_alfanumerico("ABCDEFGHIJKL80")

# Exemplo com formato inválido (letra no lugar do DV)
print("\nVerificando o CNPJ com formato inválido:")
valida_cnpj_alfanumerico("ABCDEFGHIJKLAZ")