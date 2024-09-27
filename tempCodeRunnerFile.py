def solve():
    while negativo() and verificar_viabilidade_base(tabela):
        # Se a função calcular retornar False, interrompemos o loop
        if calcular() == False:
            break  # Para o loop se não houver variáveis para entrar na base

        # Imprime o tableau após cada iteração
        imprimir_tabela()