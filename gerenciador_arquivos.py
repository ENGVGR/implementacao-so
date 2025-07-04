class GerenciadorArquivos:
    def __init__(self, num_blocos, arquivos_iniciais):
        self.num_blocos = num_blocos
        self.disco = [0] * num_blocos
        self.arquivos = {}
        
        for nome, inicio, tamanho in arquivos_iniciais:
            self.arquivos[nome] = {'inicio': inicio, 'tamanho': tamanho, 'dono': None}
            for i in range(inicio, inicio + tamanho):
                self.disco[i] = nome

    def criar_arquivo(self, id_proc, prioridade, nome, tamanho):
        livre = 0
        start = -1
        for i in range(self.num_blocos):
            if self.disco[i] == 0:
                if start == -1:
                    start = i
                livre += 1
                if livre == tamanho:
                    break
            else:
                start = -1
                livre = 0

        if livre < tamanho:
            return False, f"O processo {id_proc} não pode criar o arquivo {nome} (falta de espaço)."
        if nome in self.arquivos:
            return False, f"O arquivo {nome} já existe."
        # Aloca espaço
        for i in range(start, start + tamanho):
            self.disco[i] = nome
        self.arquivos[nome] = {'inicio': start, 'tamanho': tamanho, 'dono': id_proc}
        blocos = ', '.join(str(b) for b in range(start, start + tamanho))
        return True, f"O processo {id_proc} criou o arquivo {nome} (blocos {blocos})."

    def deletar_arquivo(self, id_proc, prioridade, nome):
        if nome not in self.arquivos:
            return False, f"O processo {id_proc} não pode deletar o arquivo {nome} porque ele não existe."
        dono = self.arquivos[nome]['dono']
        if prioridade != 0 and dono != id_proc:
            return False, f"O processo {id_proc} não pode deletar o arquivo {nome} (não é o dono)."
        inicio = self.arquivos[nome]['inicio']
        tamanho = self.arquivos[nome]['tamanho']
        for i in range(inicio, inicio + tamanho):
            self.disco[i] = 0
        del self.arquivos[nome]
        return True, f"O processo {id_proc} deletou o arquivo {nome}."

    def mapa_disco(self):
        return " ".join(str(b) if b != 0 else "0" for b in self.disco)
