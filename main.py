# Trabalho de Implementação - SO UnB 2025.1

# Leonardo Pereira Cortes - 200030582
# Leonardo Ramos Barbosa - 211010360
# Vinicius Gonzaga Ribeiro - 190059273

import sys
# from gerenciador_processos import 
# from gerenciador_memoria import 
# from gerenciador_es import 
from gerenciador_arquivos import GerenciadorArquivos

def ler_processos(arquivo):
    processos = []
    with open(arquivo, 'r') as f:
        for linha in f:
            if linha.strip():
                dados = [int(x.strip()) for x in linha.strip().split(',')]
                processos.append(dados)
    return processos


def ler_arquivo_arquivos(arquivo):
    with open(arquivo, 'r') as f:
        linhas = [linha.strip() for linha in f if linha.strip()]

    qtd_blocos = int(linhas[0])
    qtd_segmentos = int(linhas[1])
    arquivos_existentes = []
    for i in range(2, 2 + qtd_segmentos):
        nome, inicio, tamanho = [x.strip() for x in linhas[i].split(',')]
        arquivos_existentes.append((nome, int(inicio), int(tamanho)))

    operacoes = []
    for i in range(2 + qtd_segmentos, len(linhas)):
        partes = [x.strip() for x in linhas[i].split(',')]
        if len(partes) == 4:
            id_processo, cod_op, nome_arq, blocos = partes
            operacoes.append((int(id_processo), int(cod_op), nome_arq, int(blocos)))
        else:
            id_processo, cod_op, nome_arq = partes
            operacoes.append((int(id_processo), int(cod_op), nome_arq, None))
    return qtd_blocos, arquivos_existentes, operacoes


def main():
    if len(sys.argv) < 3:
        print("Uso: python main.py processes.txt files.txt")
        sys.exit(1)

    arquivo_processos = sys.argv[1]
    arquivo_arquivos = sys.argv[2]

    # Lê os processos
    processos = ler_processos(arquivo_processos)

    # Lê informações do sistema de arquivos
    qtd_blocos, arquivos_existentes, operacoes = ler_arquivo_arquivos(arquivo_arquivos)

    print("dispatcher =>")
    for i, p in enumerate(processos):
        print(f" PID: {i} offset: {i * 65} blocks: {p[3]} priority: {p[1]} time: {p[2]} printers: {p[4]} scanners: {p[5]} modems: {p[6]} drives: {p[7]}")
        print(f"process {i} =>")
        print(f" P{i} STARTED")
        for j in range(p[2]):
            print(f" P{i} instruction {j+1}")
        print(f" P{i} return SIGINT")

    print("Sistema de arquivos =>")

    # Inicialização do gerenciador de arquivos
    arquivo = GerenciadorArquivos(qtd_blocos, arquivos_existentes)

    # Para cada operação lida do arquivo de operações:
    for idx, op in enumerate(operacoes):
        id_proc, cod_op, nome, blocos = op
        if id_proc >= len(processos):
            print(f"Operação {idx+1} => Falha O processo {id_proc} não existe.")
            continue
        prioridade = processos[id_proc][1]
        if cod_op == 0:  # Create
            ok, msg = arquivo.criar_arquivo(id_proc, prioridade, nome, blocos)
        elif cod_op == 1:  # Delete
            ok, msg = arquivo.deletar_arquivo(id_proc, prioridade, nome)
        else:
            ok, msg = False, "Operação desconhecida."
        status = "Sucesso" if ok else "Falha"
        print(f"Operação {idx+1} => {status} {msg}")

    # Ao final:
    print("Mapa do disco:", arquivo.mapa_disco())


if __name__ == '__main__':
    main()
