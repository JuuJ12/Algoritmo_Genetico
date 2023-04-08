import time
matriz = open('matriz', 'r')
def permut(lista):
    if len(lista) <= 1:
        yield lista
        return
    for i, atual in enumerate(lista):
        elementos_res = lista[:i] + lista[i + 1:]
        for p in permut(elementos_res):
            yield [atual] + p


def main():

    l, c = matriz.readline().split()
    linhas = matriz.read().splitlines()


    local_c = {}
    ponto_e = []

    for i in range(int(l)):
        fios = linhas[i].split()
        for j in fios:
            if j != '0':
                local_c[j] = (i, fios.index(j))
                ponto_e.append(j)
    #print(ponto_e)
    ponto_e.remove('R')
    #print(ponto_e)
    caminho_m = int('999999999999999999')
    t1 = time.process_time()
    for v in list(permut(ponto_e)):
        custa_a = 0
        timer = 0

        v = list(v)
        v.append('R')
        v.insert(0, 'R')

        while timer < len(v) - 1:
            vertical_c = abs(local_c[v[timer]][0] - local_c[v[timer + 1]][0])
            horizontal_c = abs(local_c[v[timer]][1] - local_c[v[timer + 1]][1])
            custa_a += horizontal_c + vertical_c
            timer += 1
            #print(vertical_c)
            #print(horizontal_c)
        if custa_a < caminho_m:
            caminho_m = custa_a
            trajeto = v
    t2 = time.process_time()
    print(t2-t1)
    print(local_c)
    print(caminho_m)
    print((trajeto[1:-1]))
main()
