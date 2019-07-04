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
        self.volume = None
        self.ler_arquivo()

    def ler_arquivo(self):
        file = open('./entrada/item_50.csv')
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
        while i < len(self.mochila):
            item = self.mochila[i]
            if random.randint(0, 1) == 1:
                if volume+item.volume <= self.volume:
                    self.pai.append(1)
                    volume += item.volume
            else:
                self.pai.append(0)
            i += 1
        print(self.pai, volume)
        volume = 0
        i = 0
        while i < len(self.mochila):
            item = self.mochila[i]
            if random.randint(0, 1) == 1:
                if volume+item.volume <= self.volume:
                    self.mae.append(1)
                    volume += item.volume
            else:
                self.mae.append(0)
            i += 1
        print(self.mae, volume)

    def crossingOver(self):
        while True:
            i = 0
            volume = 0
            porcentagem = random.random()
            qtd_pai = int(porcentagem * len(self.mochila))
            print(qtd_pai)
            while i < qtd_pai:
                item_pai = self.pai[i]
                if item_pai == 1:
                    volume += self.mochila[i].volume 
                self.filho.append(item_pai)
                i += 1
            print(i)
            while i < len(self.mochila):
                item_mae = self.mae[i]
                if item_mae == 1:
                    volume += self.mochila[i].volume 
                self.filho.append(item_mae)
                i += 1
            if volume < self.volume:
                break

    def algGenetico(self):
        geracoes = int(input("Deseja quantas gerações? "))
        i = 0
        # while i < geracoes:
        self.crossingOver()


mochila = Mochila()
mochila.criar_pais()
mochila.algGenetico()
