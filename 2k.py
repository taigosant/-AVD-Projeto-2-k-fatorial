import numpy
from functools import reduce
from itertools import product
ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def generate_table(k):
    labels = []
    # atribuindo labels aos fatores
    for i in range(0, k):
        labels.append(ascii_uppercase[i])

    # label de interacao de todos os fatores
    interation_all = reduce(lambda x, y: x + y, labels)

    # adicionando interacoes a lista de labels
    for i in range(0, k):
        for j in range(i+1, k):
            labels.append(labels[i] + labels[j])

    if k > 2:
        labels.append(interation_all)

    # print(labels)

    # criando a tabela verdade inicial
    outra_table = numpy.array(list(product([1, -1], repeat=k)))
    # print(outra_table)

    # gerando a coluna que contem a interacao de todos os fatores. ex: ABC..
    interation_all_array = numpy.ones(2**k)

    for i in range (0,k):
        interation_all_array = interation_all_array * outra_table[:, i]

    interation_all_array = interation_all_array.reshape(len(outra_table), 1)

    # gerando os arrays de interacoes. ex: AB, AC, BC..
    labels_pos = k
    for i in range(0, k):
        for j in range(i+1, k):
            x = outra_table[:, i]
            y = outra_table[:, j]
            prod = numpy.array(x*y).reshape(len(outra_table),1)
            # print(labels[labels_pos], x, y, prod)
            outra_table = numpy.append(outra_table, prod, axis=1)
            labels_pos += 1

    # adicionando o array de tdas as interacoes na ultima coluna da tabela
    if k > 2:
        outra_table = numpy.append(outra_table, interation_all_array, axis=1)

    # print(outra_table)
    return labels, outra_table


if __name__ == '__main__':
    k = 0
    num_exp = 0
    try:
        k = int(input(">> Numero de fatores: "))
    except Exception:
        print("entrada invalida")
        exit(0)

    num_exp = 2**k
    labels, matrix = generate_table(k)
    print("-> fatores: ", labels, "\n")
    print("-> tabela de sinais:\n", matrix)

    ys = list(eval(input(">> informe a lista de y's: ")))
    if len(ys) != num_exp:
        print("lista de y's invalida")
        exit(0)

    print("-> valores de y: ", ys)

    efeitos = []

    for i in range(0, len(labels)):
        efeito_atual = numpy.dot(matrix[:, i], ys)/num_exp
        efeitos.append(efeito_atual)

    print("-> efeitos para cada fator: ")
    print(list(zip(labels, efeitos)))

    sst = 0
    variacao_explicada = []
    for e in efeitos:
        variacao_explicada_atual = num_exp * (e**2)
        sst += variacao_explicada_atual
        variacao_explicada.append(variacao_explicada_atual)

    print("-> SST: ", sst)
    proporcoes_fatores = map(lambda x: round(x/sst, 2), variacao_explicada)

    print("-> importancia de cada fator conforme sua proporcao:\n", list(zip(labels, proporcoes_fatores)))





