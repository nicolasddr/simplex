

A, b, c, B, tabela = [], [], [], [], []
n_var = -1
m_rest = -1
tabela = []



def ler_entrada(arquivo):
    global A, b, c, B, tabela
    global n_var, m_rest
    with open(arquivo, 'r') as f: # 'with' garante que o arquivo será fechado
        # P: n(variáveis) e m(restrições)
        linha = f.readline().strip().split()

        n_var = int(linha[1]) # Número de variáveis
        m_rest = int(linha[2]) # Número de restrições

        # F: cn(função objetivo)
        linha = f.readline().strip().split()
        for valor in linha[1:]:
            c.append(float(valor))
        c.append(0.0)
        tabela.append(c)

        # R: restrições
        for i in range(m_rest):
            linha = f.readline().strip().split()

            linha_A = []
            for valor in linha[1:-1]:
                linha_A.append(float(valor))
            A.append(linha_A) # Adiciona a linha na matriz A
            b.append(float(linha[-1])) # Adiciona ao vetor b

            linha_A.append(float(linha[-1])) # Adiciona o elemento b na linha
            tabela.append(linha_A)


        # B: variáveis que estão na base
        linha = f.readline().strip().split()
        for valor in linha[1:]:
            B.append(int(valor))


def imprimir_problema():
    global A, b, c, B
    global n_var, m_rest

    print(f"n (número de variáveis): {n_var}")
    print(f"m (número de restrições): {m_rest}")

    print("\nVetor de custos c:")
    print(" ".join(f"{ci:.3f}" for ci in c))

    print("\nMatriz A:")
    for linha in A:
        print(" ".join(f"{aij:.3f}" for aij in linha))
    
    print("\nVetor b:")
    print(" ".join(f"{bi:.3f}" for bi in b))
    
    print("\nBase inicial B:")
    print(" ".join(map(str, B)))

def imprimir_tabela():

    print("   ", end="")
    for var in range(n_var):
        print(f" x{var+1:<5} ", end="")
    print("rhs")

    
    print("z | ", end="")
    for valor in tabela[0][:-1]:
        print(f"{valor:<8.3f}", end="")
    print(f"{tabela[0][-1]:<8.3f}")  

    for i, linha in enumerate(tabela[1:]):   
        print(f"{B[i]:<1} | ", end="")
        for valor in linha[:-1]:  
            print(f"{valor:<8.3f}", end="")
        print(f"{linha[-1]:<8.3f}")  

# PROBLEMA
def entra_na_base():
    # Pega a linha da função objetivo, excluindo a última coluna (coluna b)
    linha_objetivo = tabela[0][:-1]  # Assumindo que a primeira linha é a função objetivo
    
    menor_val = float('inf')  # Inicializa com um valor muito grande
    indice = -1  # Índice da variável que deve entrar na base

    # Itera sobre todas as variáveis da linha da função objetivo
    for i in range(len(linha_objetivo)):
        # Considera apenas coeficientes negativos que não estão na base
        if linha_objetivo[i] < 0 and (i + 1) not in B:  # (i + 1) é usado para verificar o índice 1-based
            if linha_objetivo[i] < menor_val:  # Se encontrar um valor menor
                menor_val = linha_objetivo[i]  # Atualiza menor_val
                indice = i  # Armazena o índice da variável que deve entrar na base

    # Se nenhum índice foi encontrado, retorna None
    if indice == -1:
        print("Nenhuma variável pode entrar na base.")
        return None

    num_var = indice + 1  # Converte para índice 1-based
    print(f"Variável {num_var} deve entrar na base. Possui valor {menor_val}. Indice={indice}")
    return indice




def sai_da_base(indice_var_entrando):
    results = {}  # Se quiser usar no futuro, mas não é mais necessário aqui
    menor_div = float('inf')  # Inicializa com um valor grande
    indice_menor_div = -1  # Índice da variável que vai sair da base
    
    for i in range(1, m_rest + 1):  # Loop começa em 1 para ignorar a função objetivo
        if tabela[i][indice_var_entrando] > 0:  # Só consideramos coeficientes positivos
            div = tabela[i][-1] / tabela[i][indice_var_entrando]  # Calcula a razão
            # Verifica se esta divisão é a menor até agora
            print(f"{tabela[i][-1]}/{tabela[i][indice_var_entrando]}")
            if div < menor_div:
                menor_div = div
                indice_menor_div = i-1  # Armazena o índice da menor razão
            
            # Armazena no dicionário, se quiser usar depois
            results[i - 1] = div  # Usa 'i-1' para ajustar o índice
    indice = indice_menor_div  # Índice da variável que vai sair da base
    if indice != -1:
        print(f"Variável {B[indice]} sai da base. Índice={indice}")
        return indice
    else:
        print(f"Base=None")
        return None


def nova_linha(linha, entrando, linha_pivot):
    pivot = linha[entrando] * -1
    print(f"pivot = {pivot}")

    result_line = [value * pivot for value in linha_pivot] 
    print(result_line)

    new_line = []

    for i in range(len(linha)):
        sum_value = result_line[i] + linha[i]
        new_line.append(sum_value)

    print(new_line)
    return new_line

def negativo():
    negative = False
    for i in range(n_var):
        if tabela[0][i] < 0:
            negative = True
    
    return negative



def calcular():
    # Encontrar a variável que deve entrar na base
    indice_var_entrando = entra_na_base()

    # Verifica se a função entra_na_base retornou None (nenhuma variável pode entrar)
    if indice_var_entrando is None:
        print("Nenhuma variável pode entrar na base. O processo foi interrompido.")
        return False  # Interrompe o cálculo e indica falha

    # Encontrar a variável que deve sair da base
    indice_var_saindo = sai_da_base(indice_var_entrando)

    if indice_var_saindo is None:
        print("Nenhuma variável pode sair da base. O processo foi interrompido.")
        print(f"RHS = {tabela[0][-1]}")
        return False  # Interrompe o cálculo e indica falha

    indice_var_saindo += 1
    
    # Copiar a linha pivô antes de alterar
    linha_pivot = tabela[indice_var_saindo]

    # Escalar a linha pivô para que o pivô seja 1
    valor_pivot = linha_pivot[indice_var_entrando]
    linha_pivot = [x / valor_pivot for x in linha_pivot]
    tabela[indice_var_saindo] = linha_pivot

    # Ajustar as outras linhas do tableau
    for i in range(len(tabela)):
        if i != indice_var_saindo:
            linha = tabela[i]
            coef_ajuste = linha[indice_var_entrando]
            # Ajustar a linha para zerar o coeficiente da variável que entrou na base
            tabela[i] = [linha[j] - coef_ajuste * linha_pivot[j] for j in range(len(linha))]

    # Atualizar a base com a nova variável entrante
    B[indice_var_saindo - 1] = indice_var_entrando + 1

    return True  # Indica sucesso no cálculo



def verificar_viabilidade_base(tableau):
    # Excluímos a primeira linha (função objetivo) e verificamos a coluna b (última coluna)
    for linha in tableau[1:]:
        valor_b = linha[-1]  # Última coluna da linha (valor de b)
        if valor_b < 0:  # Se algum valor em b for negativo, a base não é viável
            return False
    return True  # Se todos os valores em b forem >= 0, a base é viável



def solve():
    while negativo() and verificar_viabilidade_base(tabela):
        # Se a função calcular retornar False, interrompemos o loop
        if calcular() == False:
            break  # Para o loop se não houver variáveis para entrar na base

        # Imprime o tableau após cada iteração
        imprimir_tabela()

    # Verifica por que o loop foi interrompido
    if not verificar_viabilidade_base(tabela):
        print("A base se tornou inviável. O processo foi interrompido.")
        return
    elif not negativo():
        print("A solução ótima foi encontrada. Não há mais variáveis negativas.")
        return
    else:
        print("O processo foi interrompido pois nenhuma variável pode entrar na base.")
        return



ler_entrada('ex4.lp')
imprimir_problema()
solve()


