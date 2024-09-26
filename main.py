

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


# Retorna a variável que deve entrar na base
def entra_na_base():
    pivot = min(c)
    num_var = c.index(pivot) + 1
    print(f"Variável {num_var} deve entrar na base. Possui valor {pivot}")
    return num_var # Índice = num_var-1

def sai_da_base(var_entrando):
    results = {}
    for i in range(m_rest):
        if A[i][var_entrando-1] > 0:
            div = b[i]/A[i][var_entrando-1]
            results[i] = div
    indice = min(results, key=results.get)
    
    print(f"Variável {B[indice]} sai da base")
    return B[indice]


ler_entrada('modelo.lp')
imprimir_problema()
var_entrando = entra_na_base()
sai_da_base(var_entrando)
imprimir_tabela()