import numpy as np
import matplotlib.pyplot as plt


def main():
    print("Digite o nome do arquivo .dat")
    nameFile = input()
    if nameFile[-4:] == ".dat":
        fullNameFile = nameFile
    else:
        fullNameFile = nameFile + ".dat"
    try:
        file = open(fullNameFile, "r")
        print("Arquivo aberto com sucesso!")
    except:
        print("Erro ao abrir arquivo!")
        return

    print("Digite o campo independente (eixo X, campo padrão = time):")
    independentVariable = input()
    if independentVariable == "":
        independentVariable = "time"

    print("Quantas variaveis deseja plotar? (eixo y)")
    numberVariables = int(input())
    nameVariables = []
    for i in range(numberVariables):
        print("Digite o nome da " + str(i + 1) + "º variavel")
        name = input()
        print("1-tensão\n2-corrente\n3-nenhum")
        type = input()
        if type == "1":
            type = ".Vt"
            unit = "V"
        elif type == "2":
            type = ".It"
            unit = "A"
        elif type == "3":
            type = ""
            unit = ""
        nameVariables.append(name + type)
    print("Quantas repetições deseja?")
    nRepeticoes = input()
    if nRepeticoes == "" or nRepeticoes == "0":
        nRepeticoes = 1
    else:
        nRepeticoes = int(nRepeticoes)
    labelRepicoes = []
    if nRepeticoes != 1:
        for i in range(nRepeticoes):
            print("Digite o titulo da repetições" + str(i + 1) + ":")
            label = input()
            labelRepicoes.append(label)
    print("Digite a legenda do eixo X")
    xLabel = input()
    print("Digite a legenda do eixo Y")
    yLabel = input()
    print("Deseja mostrar ponto máximo?\n1-sim\n2-não")
    auxInput = input()
    if auxInput == "1":
        showMaxPoint = True
    else:
        showMaxPoint = False
    print("Deseja mostrar ponto mínimo?\n1-sim\n2-não")
    auxInput = input()
    if auxInput == "1":
        showMinPoint = True
    else:
        showMinPoint = False
    print("Digite o titulo do gráfico")
    title = input()
    x = []
    print("Deseja marcar ponto especifico?\n1-sim\n2-não")
    auxInput = input()
    yPoints = []
    if(auxInput == "1"):
        print("Quantos?")
        auxInput = int(input())
        for i in range(auxInput):
            print("Valor do valor do eixo Y:")
            yPoints.append(float(input()))
    print("Deseja adicionar grade logarítmica no eixo x?\n1-sim\n2-não")
    auxInput = input()
    if(auxInput == "1"):
        log = True
    else:
        log = False
    runX = False
    for line in file:
        if runX:
            if line == "</indep>\n":
                runX = False
                break
            else:
                if log:
                    x.append(np.log10(float(line)))
                else:
                    x.append(float(line))
                continue
        if line[:6] == "<indep":
            valuesLine = line.split(" ")
            steps = int(valuesLine[2][:-2])
            if valuesLine[1] == independentVariable:
                runX = True
    valuesVariables = np.zeros((numberVariables, steps))
    run = numberVariables * [False]
    print("Variavel independente encontrada!")
    countFillVariables = 0
    if nRepeticoes == 1:
        while countFillVariables < numberVariables:
            line = file.readline()
            if(not line) :
                return
            if line[:4] == "<dep":
                valuesLine = line.split(" ")
                try:
                    i = nameVariables.index(valuesLine[1])
                except:
                    continue
                if valuesLine[1] == nameVariables[i]:
                    run[i] = True
                    for j in range(steps):
                        line = file.readline()
                        valuesVariables[i][j] = float(line)
                    countFillVariables += 1
    else:
        repeticoesVariables = np.zeros((nRepeticoes, steps))
        while countFillVariables < nRepeticoes:
            print("Começando busca")
            line = file.readline()
            if(not line) :
                return
            if line[:4] == "<dep":
                i = 0
                valuesLine = line.split(" ")
                if valuesLine[1] == nameVariables[0]:
                    run[i] = True
                    for n in range(nRepeticoes):
                        for j in range(steps):
                            line = file.readline()
                            repeticoesVariables[n][j] = float(line)
                            countFillVariables += 1
                    # i += 1
    file.close()
    i = 0
    fig, ax = plt.subplots(constrained_layout=True)
    if nRepeticoes == 1:
        valueFor = valuesVariables
    else:
        valueFor = repeticoesVariables
    for y in valueFor:
        if nRepeticoes == 1:
            ax.plot(x, y, label=nameVariables[i].split(".")[0])
        else:
            ax.plot(x, y, label=labelRepicoes[i])
        i += 1
        if showMaxPoint:
            xmax = round(x[np.argmax(y)], 8)
            ymax = round(y.max(), 8)
            ax.annotate(
                str(ymax)+unit,
                xy=(xmax, ymax),
                xycoords="data",
                xytext=(-20, -20),
                textcoords="offset points",
                bbox=dict(boxstyle="round", fc="0.8"),
                arrowprops=dict(
                    arrowstyle="->",
                    shrinkA=0,
                    shrinkB=10,
                    connectionstyle="angle,angleA=0,angleB=90,rad=10",
                ),
            )
        if showMinPoint:
            print("Min show")
            xmin = round(x[np.argmin(y)], 8)
            ymin = round(y.min(), 8)
            ax.annotate(
                str(ymin) + unit,
                xy=(xmin, ymin),
                xycoords="data",
                xytext=(-20, 20),
                textcoords="offset points",
                bbox=dict(boxstyle="round", fc="0.8"),
                arrowprops=dict(
                    arrowstyle="->",
                    shrinkA=0,
                    shrinkB=10,
                    connectionstyle="angle,angleA=0,angleB=90,rad=10",
                ),
            )
        if yPoints:
            for point in yPoints:
                indexY = 0
                for index in range(steps):
                    if round(y[index],0) == point:
                        indexY = index
                xmin = round(x[indexY], 8)
                ymin = round(point, 8)
                ax.annotate(
                    str(ymin) + unit + '\n' + str(round(10**xmin,2)) + ' Hz',
                    xy=(xmin, ymin),
                    xycoords="data",
                    xytext=(-20, 20),
                    textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="0.8"),
                    arrowprops=dict(
                        arrowstyle="->",
                        shrinkA=0,
                        shrinkB=10,
                        connectionstyle="angle,angleA=0,angleB=90,rad=10",
                    ),
                )
    ax.legend()
    ax.set_xlabel(xLabel)
    ax.set_ylabel(yLabel)
    ax.set_title(title)
    plt.show()
    return

if __name__ == "__main__":
    main()
