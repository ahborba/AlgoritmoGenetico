import random


class Item:

    def __init__(self, volume, importancia):
        self.volume = volume
        self.importancia = importancia


class Mochila:
    def __init__(self):
        self.mochila = []
        self.pai = []
        self.mae = []
        self.filho = []
        self.maior = []
        self.importancia_pai = 0
        self.importancia_mae = 0
        self.volume_pai=0
        self.volume_mae=0
        self.importancia_maior = 0
        self.volume_maior = 0 
        self.volume = None
        self.geracao = 0
        self.ler_arquivo()

    def ler_arquivo(self):
        path = input('insira o path para o arquivo:')
        file = open(path)
        # file = open('./entrada/item_50.csv')
        for linha in file:
            linha = linha.strip('\n')
            item = linha.split(',')
            if item[0] == 'item_id':
                continue
            elif item[0] == 'Mochila':
                self.volume = int(item[1])
                continue
            self.mochila.append(Item(int(item[1]), int(item[2])))

    def criar_pais(self):
        i = 0
        volume = 0
        importancia = 0
        #gera pai
        while i < len(self.mochila):
            item = self.mochila[i]
            if random.randint(0, 1) == 1:
                if volume+item.volume <= self.volume:
                    self.pai.append(1)
                    volume += item.volume
                    importancia += item.importancia
                else:
                    self.pai.append(0)
            else:
                self.pai.append(0)
            i += 1
        self.importancia_pai = importancia
        self.volume_pai = volume
        print(self.pai, 'volume:',volume,'importancia:',importancia)
        volume = 0
        importancia = 0
        i = 0
        while i < len(self.mochila):
            item = self.mochila[i]
            if random.randint(0, 1) == 1:
                if volume+item.volume <= self.volume:
                    self.mae.append(1)
                    volume += item.volume
                    importancia += item.importancia
                else:
                    self.mae.append(0)
            else:
                self.mae.append(0)
            i += 1
        self.importancia_mae = importancia
        self.volume_mae = volume
        print(self.mae, 'volume:',volume,'importancia:',importancia)

    
    def mutacao(self):
        taxa_mutacao = int(0.15 * len(self.filho)) + 1
        while taxa_mutacao > 0:
            i = 0
            volume = 0

            while i < len(self.filho):
                probabilidade = random.random()
                if(probabilidade < 0.1):
                    taxa_mutacao-=1
                    if self.filho[i] == 0:
                        self.filho[i] = 1
                    else:
                        self.filho[i] = 0

                if self.filho[i] == 1:
                    volume += int(self.mochila[i].volume)

            
                i+=1
        return volume

    def crossingOver(self):
        while True:
            self.filho = []
            i = 0
            volume = 0
            porcentagem = random.random()
            qtd_pai = int(porcentagem * len(self.mochila))
            while i < qtd_pai:
                item_pai = self.pai[i]
                if item_pai == 1:
                    volume += self.mochila[i].volume 
                self.filho.append(item_pai)
                i += 1
            while i < len(self.mochila):
                item_mae = self.mae[i]
                if item_mae == 1:
                    volume += self.mochila[i].volume 
                self.filho.append(item_mae)
                i += 1
            volume = self.mutacao()
            if volume < self.volume:
                break
        i = 0 
        importancia = 0
        while i < len(self.filho):
            if self.filho[i] == 1:
                importancia += self.mochila[i].importancia
            i+=1
        print ('Filho:','volume:',volume,'importancia:',importancia)
    
    def gerarNovosPais(self):
        importancia_pai = 0
        importancia_mae = 0
        importancia_filho = 0
        volume_pai = 0
        volume_mae = 0
        volume_filho = 0
        i = 0
        for item in self.mochila:
            if self.mae[i] == 1:
                importancia_mae += item.importancia
                volume_pai +=item.volume
            if self.pai[i] == 1:
                importancia_pai += item.importancia
                volume_mae += item.volume
            if self.filho[i] == 1:
                importancia_filho += item.importancia
                volume_filho +=item.volume
            i+=1
        # print('pai:',self.importancia_pai,'mae:',self.importancia_mae,'filho',importancia_filho)
        if importancia_pai > importancia_mae:
            self.mae = self.filho
            self.importancia_mae = importancia_filho
            self.volume_mae = volume_filho
            self.importancia_pai = importancia_pai
        else:
            self.pai = self.filho
            self.importancia_pai = importancia_filho
            self.volume_pai = volume_filho
            self.importancia_mae = importancia_mae
        # print('pai:',self.importancia_pai,'mae:',self.importancia_mae,'filho',importancia_filho)
        self.filho = []

    def verifica_maior(self,i):
        # print('pai:',self.importancia_pai,'mae:',self.importancia_mae,'maior:',self.importancia_maior)
        
        if self.importancia_pai > self.importancia_maior:
            self.maior = self.pai[:]
            self.importancia_maior = self.importancia_pai
            self.volume_maior = self.volume_pai
            self.geracao = i
        if self.importancia_mae > self.importancia_maior:
            self.maior = self.mae[:]
            self.importancia_maior = self.importancia_mae
            self.volume_maior = self.volume_mae
            self.geracao = i

    def printar_geracao(self,espacos,i):
        print('+==========',end='')
        j = 0
        while j < espacos -1:
            print('=',end='')
            j+=1
        print('+')
        print('|GERACAO: ',i,'|',sep='')
        print('+==========',end='')
        j = 0
        while j < espacos -1:
            print('=',end='')
            j+=1
        print('+')

    def achaTamanho(self,numero):
        numero = abs(int(numero))
        if numero < 2:
            return 1
        count = 0
        valor = 1
        while valor <= numero:
            valor *= 10
            count += 1
        return count

    def algGenetico(self):
        geracoes = int(input("Deseja quantas gerações? "))
        i = 0
        self.verifica_maior(0)
        espacos = 0
        while i <= geracoes:
            espacos = self.achaTamanho(i)
            self.printar_geracao(espacos,i)
            self.crossingOver()
            self.gerarNovosPais()
            self.verifica_maior(i)
            i+=1
        print(self.maior,'volume:',self.volume_maior,'importancia:',self.importancia_maior)
        print('Maior importancia ocorre na Geração ',self.geracao)
        self.gerar_saida()

    def gerar_saida(self):
        arq = open('./saida.csv', 'w')
        for i in self.maior:
            item = str(i)+'\n'
            arq.write(item)
        arq.close()


mochila = Mochila()
mochila.criar_pais()
mochila.algGenetico()
