import random
from random import randint, sample
import time

file = open('matriz', 'r')  # leitura do arquivo

nlinhas, ncolunas = file.readline().split()
linhas = file.read().splitlines()

coordenadas = {}
pontos_e = []

for i in range(int(nlinhas)):
    line = linhas[i].split()
    for j in line:
        if j != '0':
            coordenadas[j] = (i, line.index(j))
            pontos_e.append(j)
pontos_e.remove('R')

t1 = time.process_time()


def pop_generator(delivery_points, pop_size):
    pop = [list(sample(delivery_points, len(delivery_points))) for _ in range(pop_size)]
    return pop


def fitness(rota):  # calculo o tamanho do caminho de uma rota
    c = 0
    rota_cost = 0

    rota.append('R')
    rota.insert(0, 'R')

    while c < len(rota) - 1:
        custo_eixoy = abs(coordenadas[rota[c]][0] - coordenadas[rota[c + 1]][0])
        custo_exiox = abs(coordenadas[rota[c]][1] - coordenadas[rota[c + 1]][1])
        rota_cost += custo_exiox + custo_eixoy
        c += 1

    del (rota[0], rota[-1])

    return rota_cost


def rank(pop):  # função auxiliar
    pop.sort(key=lambda x: x[0])
    return pop


def selection(pop, m, k):  # seleção por torneio
    mais_adpt = []
    torneio = []

    for i in range(m):
        duelistas = random.sample(pop, k)
        for j in duelistas:
            torneio.append((fitness(j), j))
        campeao = rank(torneio)[0][1]
        mais_adpt.append(campeao)

    return mais_adpt

#def selection(pop, m): # SELEÇÃO POR ROLETA
#    fitness_sum = sum([1/fitness(cromossomo) for cromossomo in pop])
#    selected = []
#    for i in range(m):
#        aleatorio = random.uniform(0, fitness_sum)
#        for cromossomo in pop:
#            aleatorio -= 1/fitness(cromossomo)
#            if aleatorio <= 0:
#                selected.append(cromossomo)
#                break
#    return selected


def crossover(pai1, pai2):  # cruzamento realizado por PMX
    ponto_corte = randint(1, len(pai1) - 1)
    backup = pai2[:]
    offspring = []

    for filho in range(2):
        for point in range(ponto_corte):
            if pai1[point] != pai2[point]:
                temp = pai2[point]
                pai2[point] = pai1[point]

                for mudar_ponto in range(point + 1, len(pai2)):
                    if pai2[point] == pai2[mudar_ponto]:
                        pai2[mudar_ponto] = temp
                        break

        offspring.append(pai2)
        pai2 = pai1
        pai1 = backup

    return offspring


def mutation(rota):  # mutação por swap com 0.07% de chance de ocorrer
    if random.random() <= 0.07:
        ponto_m = randint(0, len(rota) - 2)
        backup = rota[ponto_m]

        rota[ponto_m] = rota[ponto_m + 1]
        rota[ponto_m + 1] = backup

        return rota


def ag(n):
    global melhor_solucao
    p = pop_generator(pontos_e, 100)  # população inicial
    menor_caminho = 9999999999
    contador_geracao = 0  # contador de gerações
    lista_menorc = []

    while contador_geracao < n:
        selecionados = selection(p, 20, 5)  # seleção dos 20 mais aptos
        p = []
        for k in range(100):
            p1 = random.choice(selecionados)  # escolha do pai 1
            p2 = random.choice(selecionados)  # escolha do pai 2

            filho1, filho2 = crossover(p1, p2)  # geração de filhos

            mutation(filho1)  # chance de mutação
            mutation(filho2)  # chance de mutação

            p.append(filho1)  # reinserção da população
            p.append(filho2)  # reinserção da população

        contador_geracao += 1

        solucao_atual = selection(p, 2, 1)[0]

        if fitness(solucao_atual) < menor_caminho:
            menor_caminho = fitness(solucao_atual)
            lista_menorc.append(str(menor_caminho))
            melhor_solucao = solucao_atual

    return melhor_solucao, lista_menorc


t2 = time.process_time()

result = ag(80)

print("O tempo Necessário foi: ", (t2 - t1))
print('Melhor percurso:', '->'.join(result[0]))
print('Evolução do algoritmo:', '->'.join(result[1]))
for ponto in result[0]:
    print(f'Ponto {ponto}: {coordenadas[ponto]}')
