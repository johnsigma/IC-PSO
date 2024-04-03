import random

# melhorPosicaoGlobal = 0

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


def espaco_de_busca(numTarefas, numProcessadores, tamanhoPopulacao, dicionarioTarefas):
    espacoDeBusca = []

    for _ in range(tamanhoPopulacao):
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

        espacoDeBusca.append(particula)

    return espacoDeBusca

def inicializa_exame(tamanhoEnxame, espacoDeBusca):
    enxame = []
    for i in range(tamanhoEnxame):
        posicao = random.randint(0, len(espacoDeBusca)-1)
        fitness = fitness(espacoDeBusca[posicao], numProcessadores, numTarefas, dicionarioTarefas)
        particula = {
            'posicao_atual': posicao,
            'melhor_posicao': posicao,
            'velocidade': 0,
            'fitness_atual': fitness,
            'melhor_fitness': fitness
        }
        enxame.append(particula)

    return enxame

def melhor_fitness_global(enxame, espacoDeBusca, numProcessadores, numTarefas, dicionarioTarefas):
    melhor = {
        'fitness': enxame[0]['fitness_atual'],
        'posicao': enxame[0]['posicao_atual']
    }
    for i in range(len(enxame)):
        fitness = fitness(espacoDeBusca[enxame[i]['posicao_atual']], numProcessadores, numTarefas, dicionarioTarefas)
        if fitness < melhor['fitness']:
            melhor['fitness'] = fitness
            melhor['posicao'] = enxame[i]['posicao_atual']
    
    return melhor

def atualiza_enxame(enxame, espacoDeBusca, dicionarioTarefas, numProcessadores, numTarefas):
    for i in range(len(enxame)):
        fitness_atual = enxame[i]['fitness_atual']
        fitness_melhor = enxame[i]['melhor_fitness']
        # fitness_atual = fitness(espacoDeBusca[enxame[i]['posicao_atual']], numProcessadores, numTarefas, dicionarioTarefas)
        # fitness_melhor = fitness(espacoDeBusca[enxame[i]['melhor_posicao']], numProcessadores, numTarefas, dicionarioTarefas)

        if fitness_atual < fitness_melhor:
            enxame[i]['melhor_posicao'] = enxame[i]['posicao_atual']

if __name__ == '__main__':
    dicionarioTarefas = {}
    numTarefas = 0
    nomeArquivo = 'exemplo.stg'
    numProcessadores = 4
    tamanhoPopulacao = 20

    numTarefas, dicionarioTarefas = ler_arquivo(
        nomeArquivo, numTarefas, dicionarioTarefas)

    espacoBusca = espaco_de_busca(
        numTarefas, numProcessadores, tamanhoPopulacao, dicionarioTarefas)
    
    enxame = inicializa_exame(tamanhoPopulacao, espacoBusca)
    print('Espaço de busca:')

    for particula in espacoBusca:
        print('\n\nFitness:')
        f = fitness(particula, numProcessadores, numTarefas, dicionarioTarefas)
        print(f)

    print('\n\nEnxame:')
    for particula in enxame:
        print(particula)