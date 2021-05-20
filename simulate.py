#import matplotlib.pyplot as plt
import numpy as np
import model
import crc_models as cm
import os
import copy
import matplotlib.pyplot as plt


def divide(list_of_lists, d):
    for list in list_of_lists:
        for i, num in enumerate(list):
            list[i] = num / d
    return list_of_lists





def simulate(model, duration):

    detailedCount = 10
    totalSimulations = 100
    dataPoints = 1000




    try:
        os.mkdir('output_files')
    except:
        print("the directory already exists")


    #crc.run(duration)
    #crc.show_history()

    #part 1 - make detailed graphs

    for i in range(detailedCount):
        modelToSim = copy.deepcopy(model)

        modelToSim.run(duration, dataCount = dataPoints - 1)
        modelToSim.make_history_graph()
        modelToSim.save_history_graph('output_files/sim' + str(i + 1))
        #modelToSim.show_history_graph()
        plt.close()

    #part 2 - run a lot of simulations and make mean, meansquare data

    sumTotal = []
    sumSquareTotal = []
    standardDev = []
    upperBounds = []
    lowerBounds = []
    for pop in modelToSim.get_populations():
        sumTotal.append([0] * dataPoints)
        sumSquareTotal.append([0] * dataPoints)
        standardDev.append([0] * dataPoints)
        upperBounds.append([0] * dataPoints)
        lowerBounds.append([0]*dataPoints)

    for _ in range(totalSimulations):
        modelToSim = copy.deepcopy(model)
        modelToSim.run(duration, dataCount = dataPoints - 1)

        for i, pop in enumerate(modelToSim.get_populations()):
            for j, popCount in enumerate(pop.get_history()):
                sumTotal[i][j] += popCount
                sumSquareTotal[i][j] += (popCount ** 2)

    timeHistory = modelToSim.get_time_history()
    meanHistory = divide(sumTotal, totalSimulations)
    meanSquaredHistory = divide(sumSquareTotal, totalSimulations)




    for i in range(len(standardDev)):
        for j in range(len(standardDev[i])):
            temp = meanSquaredHistory[i][j] \
                - meanHistory[i][j] ** 2
            standardDev[i][j] = temp ** 0.5
            upperBounds[i][j] = meanHistory[i][j] + standardDev[i][j]
            lowerBounds[i][j] = meanHistory[i][j] - standardDev[i][j]


    #part 3 - make an averages plot

    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_title("average population growth over time")
    ax.set_xlabel("time")
    ax.set_ylabel("population count")

    for i, pop in enumerate(model.get_populations()):
        ax.plot(timeHistory, meanHistory[i], label = pop.label)

    ax.legend()
    fig.savefig("output_files/simMean", transparent=False, dpi=160, bbox_inches="tight")
    plt.close()

    #part 4 - make a bounding plot

    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_title("average population growth over time")
    ax.set_xlabel("time")
    ax.set_ylabel("population count")
    colors = ['blue', 'orange', 'green']
    for i, pop in enumerate(model.get_populations()):
        ax.plot(timeHistory, upperBounds[i], label = pop.label + " upper bound", color = colors[i])
        ax.plot(timeHistory, lowerBounds[i], label = pop.label + " lower bound", color = colors[i])

    ax.legend()
    fig.savefig("output_files/simBounds", transparent=False, dpi=160, bbox_inches="tight")
    plt.close()


    #print(meanHistory)
    #print(meanSquaredHistory)
    #print(standardDev)


    print('done')

def main():

    birthRate = 1.15
    deathRate = 1
    growToGoRate = 0.1
    goToGoneRate = 0.1
    startingGrow = 100
    startingGo = 0
    startingGone = 0
    duration = 8



    crc = cm.SimplestModel(birthRate, deathRate, growToGoRate, goToGoneRate, startingGrow, startingGo, startingGone)

    simulate(crc, duration)

if __name__ == "__main__":
    main()
