import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt


def sliding_average(values, sample_size):
    out = [None] * len(values)
    for i, val in enumerate(values):
        if i < sample_size:
            out[i] = sum(values[0: (i + 1)]) / (i + 1)
        else:
            out[i] = sum(values[(i - sample_size): i]) / sample_size
    return out


def from_excel(filename):
    with open(filename) as file:
        lines = [line.strip() for line in file]    
    first_line = lines[0]
    n_cols = len(first_line.split('\t'))
    
    out = list()
    for _ in range(n_cols):
        out.append(list())

    for line in lines:
        line_split = line.split('\t')
        assert(len(line_split) == n_cols)
        for col in range(n_cols):
            val = float(line_split[col].replace(',', '.'))
            out[col].append(val)
    return out


def get_time_labels(yticks, timenum, time):
    yticks_new = []
    for ytick in yticks:
        if ytick in timenum:            
            ind = timenum.index(ytick)        
            ytick_new = time[ind]
            if ytick_new.endswith('M12'):
                ytick_new = ytick_new[:-3]
                ytick_new = str(int(ytick_new) + 1)
        else:
            ytick_new = ""
        yticks_new.append(ytick_new)
    return yticks_new


def time2num(time):
    timenum = []
    for t in time:
        if '_' in t:
            y, m = t.split('_')
        else:
            y, m = t.split('M')
        y = int(y)
        m = int(m)
        tnum = (y - 2006) + m / 12
        timenum.append(tnum)
    return timenum


def main():
    # time = [
    # "2006_01",
    # "2006_02",
    # "2006_03",
    # "2006_04",
    # "2006_05",
    # "2006_06",
    # "2006_07",
    # "2006_08",
    # "2006_09",
    # "2006_10",
    # "2006_11",
    # "2006_12",
    # "2007_01",
    # "2007_02",
    # "2007_03",
    # "2007_04",
    # "2007_05",
    # "2007_06",
    # "2007_07",
    # "2007_08",
    # "2007_09",
    # "2007_10",
    # "2007_11",
    # "2007_12",
    # "2008_01",
    # "2008_02",
    # "2008_03",
    # "2008_04",
    # "2008_05",
    # "2008_06",
    # "2008_07",
    # "2008_08",
    # "2008_09",
    # "2008_10",
    # "2008_11",
    # "2008_12",
    # "2009_01",
    # "2009_02",
    # "2009_03",
    # "2009_04",
    # "2009_05",
    # "2009_06",
    # "2009_07",
    # "2009_08",
    # "2009_09",
    # "2009_10",
    # "2009_11",
    # "2009_12",
    # "2010_01",
    # "2010_02",
    # "2010_03",
    # "2010_04",
    # "2010_05",
    # "2010_06",
    # "2010_07",
    # "2010_08",
    # "2010_09",
    # "2010_10",
    # "2010_11",
    # "2010_12",
    # "2011_01",
    # "2011_02",
    # "2011_03",
    # "2011_04",
    # "2011_05",
    # "2011_06",
    # "2011_07",
    # "2011_08",
    # "2011_09",
    # "2011_10",
    # "2011_11",
    # "2011_12",
    # "2012_01",
    # "2012_02",
    # "2012_03",
    # "2012_04",
    # "2012_05",
    # "2012_06",
    # "2012_07",
    # "2012_08",
    # "2012_09",
    # "2012_10",
    # "2012_11",
    # "2012_12",
    # "2013_01",
    # "2013_02",
    # "2013_03",
    # "2013_04",
    # "2013_05",
    # "2013_06",
    # "2013_07",
    # "2013_08",
    # "2013_09",
    # "2013_10",
    # "2013_11",
    # "2013_12",
    # "2014_01",
    # "2014_02",
    # "2014_03",
    # "2014_04",
    # "2014_05",
    # "2014_06",
    # "2014_07",
    # "2014_08",
    # "2014_09",
    # "2014_10",
    # "2014_11",
    # "2014_12",
    # "2015_01",
    # "2015_02",
    # "2015_03",
    # "2015_04",
    # "2015_05",
    # "2015_06",
    # "2015_07",
    # "2015_08",
    # "2015_09",
    # "2015_10",
    # "2015_11",
    # "2015_12",
    # "2016_01",
    # "2016_02",
    # "2016_03",
    # "2016_04",
    # "2016_05",
    # "2016_06",
    # "2016_07",
    # "2016_08",
    # "2016_09",
    # "2016_10",
    # "2016_11",
    # "2016_12",
    # "2017_01",
    # "2017_02",
    # "2017_03",
    # "2017_04",
    # "2017_05",
    # "2017_06",
    # "2017_07",
    # "2017_08",
    # "2017_09",
    # "2017_10",
    # "2017_11",
    # "2017_12",
    # "2018_01",
    # "2018_02",
    # "2018_03",
    # "2018_04",
    # "2018_05",
    # "2018_06",
    # "2018_07",
    # "2018_08",
    # "2018_09",
    # "2018_10",
    # "2018_11",
    # "2018_12",
    # "2019_01",
    # "2019_02",
    # "2019_03",
    # "2019_04",
    # "2019_05",
    # "2019_06",
    # "2019_07",
    # "2019_08",
    # "2019_09",
    # "2019_10",
    # "2019_11",
    # "2019_12",
    # "2020_01",
    # "2020_02",
    # "2020_03",
    # "2020_04",
    # "2020_05",
    # "2020_06",
    # "2020_07",
    # "2020_08",
    # "2020_09",
    # "2020_10",
    # "2020_11",
    # "2020_12",
    # "2021_01",
    # "2021_02",
    # "2021_03",
    # "2021_04",
    # "2021_05",
    # "2021_06",
    # "2021_07",
    # "2021_08",
    # "2021_09",
    # "2021_10",
    # "2021_11",
    # "2021_12",
    # "2022_01",
    # "2022_02",
    # "2022_03",
    # "2022_04",
    # "2022_05",
    # "2022_06",
    # "2022_07",
    # "2022_08"
    # ]

    # timenum = time2num(time)

    # sample_size = 200

    # sto = from_excel('stockholm.txt')
    # sto = sliding_average(sto[0], sample_size)

    # # Stockholm mean within tier, 3 tiers
    # sto_MWT3 = from_excel('stockholm_mean_within_tier3.txt')
    # T1 = sliding_average(sto_MWT3[0], sample_size)
    # T2 = sliding_average(sto_MWT3[1], sample_size)
    # T3 = sliding_average(sto_MWT3[2], sample_size)

    # fig = plt.figure(figsize=(10, 10))
    # ax = plt.axes(projection='3d')
    # ax.plot([0] * len(time), timenum, sto, label='Stockholm')
    # ax.plot([1] * len(time), timenum, T1, label='Dist 1')
    # ax.plot([2] * len(time), timenum, T2, label='Dist 2')
    # ax.plot([3] * len(time), timenum, T3, label='Dist 3')    
    # ax.set_yticklabels(get_time_labels(ax.get_yticks(), timenum, time))

    # plt.title('stockholm mean within tier')
    # plt.legend()

    # # Stockholm mean within tier, 7 tiers
    # sto_MWT7 = from_excel('stockholm_mean_within_tier7.txt')
    # T1 = sliding_average(sto_MWT7[0], sample_size)
    # T2 = sliding_average(sto_MWT7[1], sample_size)
    # T3 = sliding_average(sto_MWT7[2], sample_size)
    # T4 = sliding_average(sto_MWT7[3], sample_size)
    # T5 = sliding_average(sto_MWT7[4], sample_size)
    # T6 = sliding_average(sto_MWT7[5], sample_size)
    # T7 = sliding_average(sto_MWT7[6], sample_size)

    # plt.figure(figsize=(10, 10))
    # ax = plt.axes(projection='3d')
    # ax.plot([0] * len(time), timenum, sto, label='Stockholm')
    # ax.plot([1] * len(time), timenum, T1, label='Dist 1')
    # ax.plot([2] * len(time), timenum, T2, label='Dist 2')
    # ax.plot([3] * len(time), timenum, T3, label='Dist 3')
    # ax.plot([4] * len(time), timenum, T4, label='Dist 4')
    # ax.plot([5] * len(time), timenum, T5, label='Dist 5')
    # ax.plot([6] * len(time), timenum, T6, label='Dist 6')
    # ax.set_yticklabels(get_time_labels(ax.get_yticks(), timenum, time))
    # plt.title('stockholm mean within tier')
    # plt.legend()


    # ---------------------------------------------------------------------------------------------
    # Stockholm new tier 7
    time_newtier7 = [
        "2011M01",
        "2011M02",
        "2011M03",
        "2011M04",
        "2011M05",
        "2011M06",
        "2011M07",
        "2011M08",
        "2011M09",
        "2011M10",
        "2011M11",
        "2011M12",
        "2012M01",
        "2012M02",
        "2012M03",
        "2012M04",
        "2012M05",
        "2012M06",
        "2012M07",
        "2012M08",
        "2012M09",
        "2012M10",
        "2012M11",
        "2012M12",
        "2013M01",
        "2013M02",
        "2013M03",
        "2013M04",
        "2013M05",
        "2013M06",
        "2013M07",
        "2013M08",
        "2013M09",
        "2013M10",
        "2013M11",
        "2013M12",
        "2014M01",
        "2014M02",
        "2014M03",
        "2014M04",
        "2014M05",
        "2014M06",
        "2014M07",
        "2014M08",
        "2014M09",
        "2014M10",
        "2014M11",
        "2014M12",
        "2015M01",
        "2015M02",
        "2015M03",
        "2015M04",
        "2015M05",
        "2015M06",
        "2015M07",
        "2015M08",
        "2015M09",
        "2015M10",
        "2015M11",
        "2015M12",
        "2016M01",
        "2016M02",
        "2016M03",
        "2016M04",
        "2016M05",
        "2016M06",
        "2016M07",
        "2016M08",
        "2016M09",
        "2016M10",
        "2016M11",
        "2016M12",
        "2017M01",
        "2017M02",
        "2017M03",
        "2017M04",
        "2017M05",
        "2017M06",
        "2017M07",
        "2017M08",
        "2017M09",
        "2017M10",
        "2017M11",
        "2017M12",
        "2018M01",
        "2018M02",
        "2018M03",
        "2018M04",
        "2018M05",
        "2018M06",
        "2018M07",
        "2018M08",
        "2018M09",
        "2018M10",
        "2018M11",
        "2018M12",
        "2019M01",
        "2019M02",
        "2019M03",
        "2019M04",
        "2019M05",
        "2019M06",
        "2019M07",
        "2019M08",
        "2019M09",
        "2019M10",
        "2019M11",
        "2019M12",
        "2020M01",
        "2020M02",
        "2020M03",
        "2020M04",
        "2020M05",
        "2020M06",
        "2020M07",
        "2020M08",
        "2020M09",
        "2020M10",
        "2020M11",
        "2020M12",
        "2021M01",
        "2021M02",
        "2021M03",
        "2021M04",
        "2021M05",
        "2021M06",
        "2021M07",
        "2021M08",
        "2021M09",
        "2021M10",
        "2021M11",
        "2021M12",
        "2022M01",
        "2022M02",
        "2022M03",
        "2022M04",
        "2022M05",
        "2022M06",
        "2022M07",
        "2022M08",
        "2022M09" 
    ]
    timenum_newtier7 = time2num(time_newtier7)

    sample_size = 50

    # Stockhlm percar
    data = from_excel('stockholm_percar.txt')
    T0 = sliding_average(data[0], sample_size)
    T1 = sliding_average(data[1], sample_size)
    T2 = sliding_average(data[2], sample_size)
    T3 = sliding_average(data[3], sample_size)
    T4 = sliding_average(data[4], sample_size)
    T5 = sliding_average(data[5], sample_size)

    plt.figure(figsize=(8, 7))
    # ax = plt.axes(projection='3d')
    ax = plt.axes()
    # ax.plot([0] * len(timenum_newtier7), timenum_newtier7, T0, label='Stockholm')
    # ax.plot([1] * len(timenum_newtier7), timenum_newtier7, T1, label='Zone 1')
    # ax.plot([2] * len(timenum_newtier7), timenum_newtier7, T2, label='Zone 2')
    # ax.plot([3] * len(timenum_newtier7), timenum_newtier7, T3, label='Zone 3')
    # ax.plot([4] * len(timenum_newtier7), timenum_newtier7, T4, label='Zone 4')
    # ax.plot([5] * len(timenum_newtier7), timenum_newtier7, T5, label='Zone 5')
    ax.plot(timenum_newtier7, T0, label='Stockholm', linewidth=4)
    ax.plot(timenum_newtier7, T1, label='Zone 1')
    ax.plot(timenum_newtier7, T2, label='Zone 2')
    ax.plot(timenum_newtier7, T3, label='Zone 3')
    ax.plot(timenum_newtier7, T4, label='Zone 4')
    ax.plot(timenum_newtier7, T5, label='Zone 5')

    ax.set_xticklabels(get_time_labels(ax.get_xticks(), timenum_newtier7, time_newtier7))
    # ax.set_yticklabels(get_time_labels(ax.get_yticks(), timenum_newtier7, time_newtier7))
    plt.xlabel("Year")
    plt.ylabel("Proportion electric cars to all newly registred cars")
    plt.title('Stockholm')
    plt.grid()
    plt.ylim([0, 0.5])
    plt.legend()

    # Gbg percar
    data = from_excel('gbg_percar.txt')
    T0 = sliding_average(data[0], sample_size)
    T1 = sliding_average(data[1], sample_size)
    T2 = sliding_average(data[2], sample_size)
    T3 = sliding_average(data[3], sample_size)
    T4 = sliding_average(data[4], sample_size)
    T5 = sliding_average(data[5], sample_size)

    plt.figure(figsize=(8, 7))
    # ax = plt.axes(projection='3d')
    ax = plt.axes()
    # ax.plot([0] * len(timenum_newtier7), timenum_newtier7, T0, label='Gothenburg')
    # ax.plot([1] * len(timenum_newtier7), timenum_newtier7, T1, label='Zone 1')
    # ax.plot([2] * len(timenum_newtier7), timenum_newtier7, T2, label='Zone 2')
    # ax.plot([3] * len(timenum_newtier7), timenum_newtier7, T3, label='Zone 3')
    # ax.plot([4] * len(timenum_newtier7), timenum_newtier7, T4, label='Zone 4')
    # ax.plot([5] * len(timenum_newtier7), timenum_newtier7, T5, label='Zone 5')

    ax.plot(timenum_newtier7, T0, label='Gothenburg', linewidth=4)
    ax.plot(timenum_newtier7, T1, label='Zone 1')
    ax.plot(timenum_newtier7, T2, label='Zone 2')
    ax.plot(timenum_newtier7, T3, label='Zone 3')
    ax.plot(timenum_newtier7, T4, label='Zone 4')
    ax.plot(timenum_newtier7, T5, label='Zone 5')
    ax.set_xticklabels(get_time_labels(ax.get_xticks(), timenum_newtier7, time_newtier7))
    plt.title('Gothenburg')
    plt.legend()
    plt.grid()
    plt.ylim([0, 0.5])

    # Malmo percar
    data = from_excel('malmo_percar.txt')
    T0 = sliding_average(data[0], sample_size)
    T1 = sliding_average(data[1], sample_size)
    T2 = sliding_average(data[2], sample_size)
    T3 = sliding_average(data[3], sample_size)
    T4 = sliding_average(data[4], sample_size)
    T5 = sliding_average(data[5], sample_size)

    plt.figure(figsize=(8, 7))
    # ax = plt.axes(projection='3d')
    ax = plt.axes()
    # ax.plot([0] * len(timenum_newtier7), timenum_newtier7, T0, label='Malmo')
    # ax.plot([1] * len(timenum_newtier7), timenum_newtier7, T1, label='Zone 1')
    # ax.plot([2] * len(timenum_newtier7), timenum_newtier7, T2, label='Zone 2')
    # ax.plot([3] * len(timenum_newtier7), timenum_newtier7, T3, label='Zone 3')
    # ax.plot([4] * len(timenum_newtier7), timenum_newtier7, T4, label='Zone 4')
    # ax.plot([5] * len(timenum_newtier7), timenum_newtier7, T5, label='Zone 5')

    ax.plot(timenum_newtier7, T0, label='Malmo', linewidth=4)
    ax.plot(timenum_newtier7, T1, label='Zone 1')
    ax.plot(timenum_newtier7, T2, label='Zone 2')
    ax.plot(timenum_newtier7, T3, label='Zone 3')
    ax.plot(timenum_newtier7, T4, label='Zone 4')
    ax.plot(timenum_newtier7, T5, label='Zone 5')
    ax.set_xticklabels(get_time_labels(ax.get_xticks(), timenum_newtier7, time_newtier7))
    plt.title('Malmo')
    plt.legend()
    plt.grid()
    plt.ylim([0, 0.5])

    plt.show()


if __name__ == "__main__":
    main()
