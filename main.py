# Plotting the data from a series of thermal tests performed on 25 November 2022.
# The tests ran in a FormD T1 v2 sandwich using:
#       Asus B550i strix
#       2x16 GB of Crucial RGB 3600c16 ram
#       Tuned Ryzen 5900x (PBO & CO)
#       Undervolted 3080 FE
#       Phanteks Glacier One 240MP AIO
#       Corsair SF750 PSU.
#
# Parameters were:
#       Side panel:
#           Aluminium
#           Acrylic mesh
#           Tempered glass (TG)
#       Top panel:
#           Stock
#           Acrylic mesh
#           Hollow
#       Fan combinations:
#       A12x15 + T30
#       A12x15 + A12x25
#       A12x25 + A12x25
#       A12x25 + T30
#

import matplotlib.pyplot as plt
import pandas as pd


def importKey():
    # Imports "tests.txt" which has the 11 executed test parameters and acts as the key
    keyRead = pd.read_csv("data/tests.txt")
    return keyRead


def importAmbients():
    # Imports the ambient temperature recorded for each of the 11 configurations.
    ambient = []
    for i in range(11):
        ambient.append(pd.read_csv("data/" + str(i + 1) + "/ambient.txt", header=None)[0][0])

    return ambient


def importHwInfo(fileName, ambient):
    # Imports the HWInfo data from the testing, discards irrelevant data, and adjusts for changes in ambient temperature
    hwInfoRead = []
    # The baseline ambient
    ambientBase = 22

    for i in range(11):  # 11 configs that all get added to 1 variable
        # print(i + 1)  # for debugging in case one of the files is not reading correctly

        # The footer has the header repeated as well as the data source
        lastRead = pd.read_csv("data/" + str(i + 1) + fileName, header=0, skipfooter=2, encoding='mbcs',
                               engine='python')

        # Only selects interesting columns and adjusts for changes in ambient temperature throughout testing
        lastRead = lastRead.loc[:, ["T_Sensor [°C]", "CPU [°C]", "GPU Temperature [°C]", "CPU Package Power [W]",
                                    "CPU [RPM]", "Chassis1 [RPM]", "GPU Fan1 [RPM]", "GPU Power [W]", "Date", "Time"]]
        lastRead.loc[:, ["T_Sensor [°C]", "CPU [°C]", "GPU Temperature [°C]"]] = \
            lastRead.loc[:, ["T_Sensor [°C]", "CPU [°C]", "GPU Temperature [°C]"]].sub(ambient[i])
        lastRead.loc[:, ["T_Sensor [°C]", "CPU [°C]", "GPU Temperature [°C]"]] = \
            lastRead.loc[:, ["T_Sensor [°C]", "CPU [°C]", "GPU Temperature [°C]"]].add(ambientBase)

        # I want a relative time in seconds, I get the first timestamp, so I can subtract it from all other timestamps.
        time0 = pd.to_datetime(lastRead.Date[0] + " " + lastRead.Time[0], format='%d.%m.%Y %H:%M:%S.%f')
        relTime = pd.to_datetime(lastRead.Date + " " + lastRead.Time, format='%d.%m.%Y %H:%M:%S.%f') - time0
        relTime = relTime.apply(lambda x: round(x.total_seconds()))
        lastRead.insert(0, 'relTime', relTime)

        hwInfoRead.append(lastRead)

    return hwInfoRead


def monsterPlot(data, title, key):
    # This function plots a 2x4 subplot containing the 8 interesting parameters for all 11 configurations.
    # The purpose is solely as a sanity check so I can compare power etc. conveniently.

    # Setting up the subplots and some formatting
    fig, axs = plt.subplots(nrows=2, ncols=4)
    plt.rc('font', size=24)
    fig.set_dpi(100)
    fig.set_size_inches(38.40, 21.60)
    fig.suptitle(title, fontsize=24)

    # More plot formatting
    plotThings = ["T_Sensor [°C]", "CPU [°C]", "GPU Temperature [°C]", "CPU Package Power [W]", "CPU [RPM]",
                  "Chassis1 [RPM]", "GPU Fan1 [RPM]", "GPU Power [W]"]
    ylabels = ["Temperature (°C)", "Temperature (°C)", "Temperature (°C)", "CPU Package Power (W)",
               "A12x15/A12x25 fan speed (rpm)", "T30/A12x25 fan speed (rpm)", "GPU Fan speed (rpm)", "GPU Power (W)"]
    plotMarkers = [".", "o", "v", "^", "1", "2", "8", "s", "p", "*", "x"]
    plotcolours = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan', 'magenta']

    for ax, whatPlot, ylabel in zip(axs.flat, plotThings, ylabels):
        # Iterates over all the subplots and things to plot
        for config, plotMarker, plotColour in zip(range(11), plotMarkers, plotcolours):
            # 11 configs to plot per chart

            ax.plot(data[config]['relTime'], data[config][whatPlot], marker=plotMarker, color=plotColour, markersize=9)
            ax.set_title(whatPlot)
            ax.set_xlabel("Time (s)", fontsize=18)
            ax.set_ylabel(ylabel, fontsize=18)
            ax.grid(which='both')
            ax.tick_params(labelsize=18)

    # It's a big ugly legend, but no real way around it
    plt.legend(key['Fan'] + '\n' + key['Side panel'] + ' side panel\n' + key['Top panel'] + ' top panel',
               bbox_to_anchor=(1.05, 2), loc=2, borderaxespad=0.)

    plt.subplots_adjust(left=0.03, right=0.84)
    plt.savefig('figure/' + title.replace(' ', '_') + '_large' + '.jpg')
    fig.show()


def fancyMean(start, end, source, data):
    # Calculates the mean between the timestamps "start" and "end", based on 'relTime'.
    # Source is the data point for which the mean is calculated, and the data is, of course, the data.
    meanCalc = [meanIt[(meanIt['relTime'] > start) & (meanIt['relTime'] < end)][source].mean() for meanIt in data]
    return meanCalc


def barChartPlot_3(cpu, gpu, liq, key, title):
    # Makes a bar chart with 3 columns per config and does a bunch of formatting

    # The x-axis ticks, basically the 11 configurations
    configs = key['Fan'] + '\n' + key['Side panel'] + '\n' + key['Top panel']

    # Create the chart and some basic formatting
    fig, ax = plt.subplots()
    plt.rc('font', size=36)
    fig.set_dpi(100)
    fig.set_size_inches(38.40, 21.60)
    bar_width = 0.25
    x_coordinates = list(range(len(configs)))

    # Plotting the actual bar charts
    bar1 = plt.bar(x_coordinates, liq, bar_width)
    bar2 = plt.bar([i + bar_width for i in x_coordinates], cpu, bar_width)
    bar3 = plt.bar([i + bar_width * 2 for i in x_coordinates], gpu, bar_width)

    # Add labels and a title
    plt.xlabel("Configurations listed as Fans, Side Panel, Top Panel")
    plt.ylabel("Temperature (°C)")
    plt.title("Equilibrium temperatures after 15 minutes of " + title)

    ax.bar_label(bar1, [round(item) for item in liq])
    ax.bar_label(bar2, [round(item) for item in cpu])
    ax.bar_label(bar3, [round(item) for item in gpu])

    # Add a legend
    plt.legend((bar1, bar2, bar3), ('AIO Liquid', 'CPU', 'GPU'), loc='lower right')

    # Add x ticks
    ax.tick_params(labelsize=23)
    plt.xticks([x + bar_width for x in x_coordinates], configs)
    plt.subplots_adjust(left=0.05, right=0.95)

    # Display the chart
    plt.savefig('figure/' + title.replace(' ', '_') + '.jpg')
    plt.show()


def barChartPlot_2(liq, cpu, key, title):
    # Makes a bar chart with 2 columns per config and does a bunch of formatting

    # The x-axis ticks, basically the 11 configurations
    configs = key['Fan'] + '\n' + key['Side panel'] + '\n' + key['Top panel']

    # Create the chart and some basic formatting
    fig, ax = plt.subplots()
    plt.rc('font', size=36)
    fig.set_dpi(100)
    fig.set_size_inches(38.40, 21.60)
    bar_width = 0.25
    x_coordinates = list(range(len(configs)))

    # Plotting the actual bar charts
    bar1 = plt.bar(x_coordinates, liq, bar_width)
    bar2 = plt.bar([i + bar_width for i in x_coordinates], cpu, bar_width)

    # Add labels and a title
    plt.xlabel("Configurations listed as Fans, Side Panel, Top Panel")
    plt.ylabel("Temperature (°C)")
    plt.title("Equilibrium temperatures after 10 minutes of " + title)

    ax.bar_label(bar1, [round(item) for item in liq])
    ax.bar_label(bar2, [round(item) for item in cpu])

    # Add a legend
    plt.legend((bar1, bar2), ('AIO Liquid', 'CPU'), loc='lower right')

    # Add x ticks
    ax.tick_params(labelsize=23)
    plt.xticks([x + bar_width/2 for x in x_coordinates], configs)
    plt.subplots_adjust(left=0.05, right=0.95)

    # Display the chart
    plt.savefig('figure/' + title.replace(' ', '_') + '.jpg')
    plt.show()


if __name__ == '__main__':
    print('Hello there')

    # Import the key and test data
    key = importKey()
    print('key read successful')
    ambient = importAmbients()
    print('Ambient read successful')
    cb = importHwInfo("/cb.csv", ambient)
    print('cb read successful')
    cp77 = importHwInfo("/cp.csv", ambient)
    print('cp77 read successful')
    occt = importHwInfo("/occt.csv", ambient)
    print('occt read successful')

    # Makes some general overview plots
    monsterPlot(cb, "Cinebench R23", key)
    monsterPlot(cp77, "Cyberpunk 2077", key)
    monsterPlot(occt, "OCCT Power Virus", key)

    # Calculating means from the data

    # Between 300s and 600s the thermals are stable for the CB run
    cbCPU = fancyMean(300, 600, "CPU [°C]", cb)
    cbLiq = fancyMean(300, 600, "T_Sensor [°C]", cb)

    # Temperatures are stable between 700 and 850s for Cyberpunk 2077 and OCCT
    cp77CPU = fancyMean(700, 850, "CPU [°C]", cp77)
    cp77GPU = fancyMean(700, 850, "GPU Temperature [°C]", cp77)
    cp77Liq = fancyMean(700, 850, "T_Sensor [°C]", cp77)

    occtCPU = fancyMean(700, 850, "CPU [°C]", occt)
    occtGPU = fancyMean(700, 850, "GPU Temperature [°C]", occt)
    occtLiq = fancyMean(700, 850, "T_Sensor [°C]", occt)

    # Plotting the bar charts
    barChartPlot_2(cbLiq, cbCPU, key, 'Cinebench R23')
    barChartPlot_3(cp77CPU, cp77GPU, cp77Liq, key, 'Cyberpunk 2077')
    barChartPlot_3(occtCPU, occtGPU, occtLiq, key, 'OCCT')

    print('General Kenobi')
