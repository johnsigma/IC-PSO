import random


def ler_arquivo(nomeArquivo, numTarefas, dicionarioTarefas):
    with open(nomeArquivo, 'r') as arquivo:
        # Itera sobre cada linha no arquivo
        i = 0
        for linha in arquivo:
            if i == 0:
                numTarefas = int(linha.strip()) + 2
            else:
                if linha.__contains__('#'):
                    break
                linha = linha.strip().split(' ')
                linha_formatada = [valor for valor in linha if valor != '']
                dicionarioTarefas[linha_formatada[0]] = {
                    'tarefa': linha_formatada[0],
                    'tempo_execucao': linha_formatada[1],
                    'num_predecessores': linha_formatada[2],
                    'predecessores': linha_formatada[3:]
                }
            i += 1
    return numTarefas, dicionarioTarefas


def fitness(particula, numProcessadores, numTarefas, dicionarioTarefas):

    RT = [0] * numProcessadores
    ST = [0] * numTarefas
    FT = [0] * numTarefas

    LT = list(map(lambda x: x['tarefa'], particula))

    S_length = 1

    for _ in range(numTarefas):
        if len(LT) == 0:
            break

        tarefa = int(LT.pop(0))

        for j in range(numProcessadores):
            if particula[tarefa]['processador'] == j:
                ST[tarefa] = max(RT[j], FT[tarefa])
                FT[tarefa] = ST[tarefa] + \
                    int(dicionarioTarefas[str(tarefa)]['tempo_execucao'])
                RT[j] = FT[tarefa]

        S_length = max(FT)

    a = 1

    return (a / S_length)


def inicializa_enxame(numTarefas, numProcessadores, tamanhoEnxame, dicionarioTarefas):
    enxame = []

    for _ in range(tamanhoEnxame):
        particula = []
        tarefasAlocadas = []

        while len(particula) < numTarefas:

            while True:

                if len(particula) == 0:
                    tarefasAlocadas.append(0)
                    particula.append({
                        'tarefa': '0',
                        'processador': random.randint(0, numProcessadores-1)
                    })
                    continue

                indiceTarefa = random.randint(0, numTarefas-1)

                if indiceTarefa in tarefasAlocadas:
                    continue

                tarefa = dicionarioTarefas[str(indiceTarefa)]

                predecessores = tarefa['predecessores']
                numPredecessores = len(predecessores)
                predecessoresEncontrados = 0

                if (numPredecessores >= 1):
                    for individuo in particula:
                        tarefaAux = individuo['tarefa']
                        if tarefaAux in predecessores:
                            predecessoresEncontrados += 1

                if predecessoresEncontrados == numPredecessores:
                    particula.append({
                        'tarefa': str(indiceTarefa),
                        'processador': random.randint(0, numProcessadores-1)
                    })
                    tarefasAlocadas.append(indiceTarefa)
                    break

        enxame.append(particula)

    return enxame


if __name__ == '__main__':
    dicionarioTarefas = {}
    numTarefas = 0
    nomeArquivo = 'exemplo.stg'
    numProcessadores = 4
    tamanhoEnxame = 20

    numTarefas, dicionarioTarefas = ler_arquivo(
        nomeArquivo, numTarefas, dicionarioTarefas)

    enxame = inicializa_enxame(
        numTarefas, numProcessadores, tamanhoEnxame, dicionarioTarefas)

    for particula in enxame:
        print('\n\nFitness:')
        f = fitness(particula, numProcessadores, numTarefas, dicionarioTarefas)
        print(f)
