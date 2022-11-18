import cProfile
import random
import csv
import sys
import pstats, io
from pstats import SortKey
from math import floor

# import cProfile, pstats, io
# from pstats import SortKey


import matplotlib.pyplot as plt
from numpy import Inf

# random.seed(42)


TIMES_MORE_LIKELY_TO_SPREAD_TO_OWN_CELL = 2


# Almost 2.5 times faster than random.randint
def myrandint0(high):
    '''Returns a random int btw 0 and high, inclusive.'''
    return floor((high + 1) * random.random())


def csv2celldist(csv_filename):
    file = open(csv_filename, encoding='utf-8')
    is_title = True
    titles = None
    with file as csvfile:
        reader = csv.reader(csvfile)
        out = dict()
        cnt = 0
        for r in reader:
            if is_title:
                titles = [s.lower() for s in r]
                is_title = False
            else:
                from_cell = r[0].lower()
                for to_cell_ind in range(1, cnt):
                    to_cell = titles[to_cell_ind]
                    out[(from_cell, to_cell)] = float(r[to_cell_ind])
                    out[(to_cell, from_cell)] = float(r[to_cell_ind])
            cnt += 1
    return out


def weighted_choice(probs):
    '''
    Returns index into x, chosen at random with probabilities given by probs.
    '''
    rnd = random.random()
    cumsum = 0
    for i, prob in enumerate(probs):
        cumsum += prob
        if rnd < cumsum:
            return i
    assert(False)


class Grid():
    def __init__(self, area, cells):
        self.cells = cells
        self.cell_dist_dict = csv2celldist(f'dist_{area}.csv')
        self._make_cellprobs()

    def cell_dist(self, name1, name2):
        return self.cell_dist_dict[(name1, name2)]

    def add(self, dict_to_add):
        for cell in self.cells:
            to_add = dict_to_add[cell.name]
            cell.add(to_add)

    def sim(self, n_generations):
        out = []

        self.write_out(out)  # Generation 0

        for gen in range(n_generations):
            for cell in self.cells:
                for agent in cell.agents:
                    if agent.is_adopter:
                        receiving_cell = self.choose_receiving_cell(cell)
                        while True:
                            receiving_agent = receiving_cell.choose_receiving_agent()
                            if receiving_agent is not agent:
                                break
                            # else:
                            #     print(" SAMMMMMMMMMMMMMMMMMMMA !!!!!!!!!!!!!!!!!!!!!!!")
                        receiving_agent.to_be_adopter = True
            self.to_be2is_adopter()
            
            self.write_out(out)
            print(gen / n_generations)
            # frac_adopters = dict()
            # for cell in self.cells:
            #     frac_adopters[cell.name] = cell.get_frac_adopters()
            # out.append(frac_adopters)
        
        return out

    def write_out(self, out):
        frac_adopters = dict()
        for cell in self.cells:
            frac_adopters[cell.name] = cell.get_frac_adopters()
        out.append(frac_adopters)
        self.pretty_print()
        
    def pretty_print(self):
        n_adopters = dict()
        for cell in self.cells:
            n = cell.get_n_adopters()
            tot = len(cell.agents)
            if n > 0:
                n_adopters[cell.name] = f"{n} ({round(n / tot * 100)}%)"
        print(n_adopters)

    def to_be2is_adopter(self):
        for cell in self.cells:
            for agent in cell.agents:
                if agent.to_be_adopter:
                    agent.is_adopter = True

    def choose_receiving_cell(self, cell):
        cell_probs = self.cell_probs[cell.name]
        cell_ind = weighted_choice(cell_probs)
        return self.cells[cell_ind]

    def _make_cellprobs(self):
        self.cell_probs = dict()
        for cell in self.cells:
            min_dist = Inf
            dists_from_cell = []
            for other_cell in self.cells:
                if other_cell.name == cell.name:
                    dists_from_cell.append(None)  # Computed after loop
                else:
                    d = self.cell_dist(cell.name, other_cell.name)
                    dists_from_cell.append(d)
                    if d < min_dist:
                        min_dist = d

            # The cell itself gets distance using TIMES_MORE_LIKELY_TO_SPREAD_TO_OWN_CELL:
            inds_None = [i for i, v in enumerate(dists_from_cell) if v is None]
            ind_None = inds_None[0]
            dists_from_cell[ind_None] = min_dist / TIMES_MORE_LIKELY_TO_SPREAD_TO_OWN_CELL

            cell_weights = []
            for c, d in zip(self.cells, dists_from_cell):
                cell_weights.append(len(c.agents) / d**2)
            sum_cell_weights = sum(cell_weights)
            cell_probs = [weight / sum_cell_weights for weight in cell_weights]
            self.cell_probs[cell.name] = cell_probs

    def to_dict(self):
        out = dict()
        for cell in self.cells:
            out[cell.name.lower()] = cell.get_frac_adopters()
        return out


class Cell():
    def __init__(self, name, n_agents, n_adopted):
        assert(n_agents >= n_adopted)
        self.name = name
        self.n_agents = n_agents
        self.agents = []
        for i in range(n_agents):
            is_adopted = i < n_adopted
            agent = Agent(is_adopted)
            self.agents.append(agent)

    def add(self, n_to_adopt):
        assert(n_to_adopt <= self.n_agents - self.get_n_adopters())
        non_adopted_agents = []
        for agent in self.agents:
            if not agent.is_adopter:
                non_adopted_agents.append(agent)
        for agent in non_adopted_agents[:n_to_adopt]:
            agent.is_adopter = True

    def get_frac_adopters(self):
        return self.get_n_adopters() / self.n_agents

    def get_n_adopters(self):
        n_adopters = 0
        for agent in self.agents:
            if agent.is_adopter:
                n_adopters += 1
        return n_adopters

    def choose_receiving_agent(self):
        # agent_ind = random.randint(0, self.n_agents - 1)
        agent_ind = myrandint0(self.n_agents - 1)
        return self.agents[agent_ind]


class Agent():
    def __init__(self, is_adopter=False):
        self.is_adopter = is_adopter
        self.to_be_adopter = False


def torstenify(x, y):    
    d = dict()
    for xval, yval in zip(x, y):
        if xval not in d:
            d[xval] = yval

    xvals = list(d.keys())
    xvals.sort()
    outx = []
    outy = []
    for xval in xvals:
        outx.append(xval)
        outy.append(d[xval])
    return outx, outy


def make_grid(area):
    if area == "sto":
        cell_names = ["Upplands Väsby", "Vallentuna", "Österåker", "Värmdö", "Järfälla", "Ekerö",
                      "Huddinge", "Botkyrka", "Salem", "Haninge", "Tyresö", "Upplands-Bro",
                      "Nykvarn", "Täby", "Danderyd", "Sollentuna", "Stockholm", "Södertälje",
                      "Nacka", "Sundbyberg", "Solna", "Lidingö", "Vaxholm", "Norrtälje",
                      "Sigtuna", "Nynäshamn", "Håbo", "Knivsta", "Heby", "Tierp", "Uppsala",
                      "Enköping", "Östhammar", "Gnesta", "Flen", "Strängnäs", "Trosa"]
        populations = [39400, 30145, 39495, 38313, 66286, 25433, 97614, 82816, 15417, 77200,
                       42952, 23680, 9317, 63866, 31379, 64768, 848523, 86354, 90143, 38748,
                       68420, 44043, 10954, 56102, 40126, 24704, 19632, 14777, 13353, 20131,
                       197939, 39793, 21373, 10358, 16058, 32414, 11466]
        # Sum of nyreg for all months 2006-2010
        n_cars = [100, 36, 141, 59, 126, 34, 157, 70, 18, 78, 54, 25, 2, 238, 199, 130,
                  4204, 87, 532, 498, 757, 138, 39, 87, 62, 20, 9, 13, 2, 3, 339, 72, 11,
                  3, 6, 128, 16]

    elif area == "gbg":
        cell_names = ["Härryda", "Partille", "Öckerö", "Stenungsund", "Tjörn", "Orust",
                      "Ale", "Lerum", "Vårgårda", "Bollebygd", "Lilla Edet", "Mark",
                      "Herrljunga", "Göteborg", "Mölndal", "Kungälv", "Alingsås",
                      "Falkenberg", "Varberg", "Kungsbacka"]
        populations = [34467, 35194, 12458, 24321, 14965, 15190, 27428, 38531, 10961, 8365, 12565, 33844, 9309, 514133, 61010, 41275, 37775, 41024, 58057, 75046]
        n_cars = [16, 31, 8, 13, 20, 2, 9, 35, 2, 2, 5, 14, 2, 1376, 153, 78, 50, 47, 54, 99]

        # cell_names2 = ["HÄRRYDA", "PARTILLE", "ÖCKERÖ", "STENUNGSUND", "TJÖRN", "ORUST", "SOTENÄS", "MUNKEDAL", "TANUM", "DALS-ED", "FÄRGELANDA", "ALE", "LERUM", "VÅRGÅRDA", "BOLLEBYGD", "GRÄSTORP", "ESSUNGA", "KARLSBORG", "GULLSPÅNG", "TRANEMO", "BENGTSFORS", "MELLERUD", "LILLA EDET", "MARK", "SVENLJUNGA", "HERRLJUNGA", "VARA", "GÖTENE", "TIBRO", "TÖREBODA", "GÖTEBORG", "MÖLNDAL", "KUNGÄLV", "LYSEKIL", "UDDEVALLA", "STRÖMSTAD", "VÄNERSBORG", "TROLLHÄTTAN", "ALINGSÅS", "BORÅS", "ULRICEHAMN", "ÅMÅL", "MARIESTAD", "LIDKÖPING", "SKARA", "SKÖVDE", "HJO", "TIDAHOLM", "FALKÖPING", "Falkenberg", "Varberg", "Kungsbacka"]
        # cell_names2 = [c.lower() for c in cell_names2]
        # n_cars2 = [16, 31, 8, 13, 20, 2, 9, 3, 5, 28, 4, 9, 35, 2, 2, 0, 1, 5, 5, 1, 2, 2, 5, 14, 0, 2, 4, 15, 3, 3, 1376, 153, 78, 15, 23, 29, 20, 47, 50, 190, 68, 12, 104, 57, 18, 152, 2, 3, 20, 47, 54, 99]
        
    elif area == "malmo":
        cell_names = ["Svalöv", "Staffanstorp", "Burlöv", "Vellinge", "Örkelljunga",
                      "Bjuv", "Kävlinge", "Lomma", "Svedala", "Skurup", "Sjöbo", "Hörby",
                      "Höör", "Tomelilla", "Perstorp", "Klippan", "Åstorp", "Båstad",
                      "Malmö", "Lund", "Landskrona", "Helsingborg", "Höganäs", "Eslöv",
                      "Ystad", "Trelleborg", "Simrishamn", "Ängelholm"]
        populations = [13232, 22248, 16680, 33269, 9623, 14837, 29038, 21548, 19807, 15002,
                       18104, 14833, 15462, 12897, 7104, 16530, 14765, 14250, 299315,
                       110589, 41744, 129378, 24661, 31591, 28332, 42223, 19258, 39419]
        n_cars = [391, 978, 746, 2287, 825, 441, 1569, 1259, 898, 496, 546, 522, 985, 411,
                 158, 424, 372, 749, 25011, 17205, 1234, 8306, 1013, 1095, 1688, 1678,
                 761, 3044]
    else:
        assert(False)

    assert(len(n_cars) == len(cell_names)), f"{len(n_cars)}, should be {len(cell_names)}"

    cell_names = [s.lower() for s in cell_names]

    cells = []
    for cell_name, population, n in zip(cell_names, populations, n_cars):
        cell = Cell(cell_name, population, n)
        cells.append(cell)
    return Grid(area, cells)


def plot_s_curves(out):
    cellnames = out[0].keys()

    plt.figure()
    for cellname in cellnames:
        y = []
        for frac_adopters in out:
            y.append(frac_adopters[cellname])
        plt.plot(y, label=cellname)
    plt.legend()


def plot_torsten(ax, area, out):
    cellnames = out[0].keys()
    
    percs = list(range(0, 101, 1))
    # gens_to_plot = [0, 5, 10, 15, 20, 25, 30]
    for gen, frac_adopters in enumerate(out):
        # if gen not in gens_to_plot:
            # continue
        x = []
        y = []
        for perc in percs:
            n_cells = 0
            for cellname in cellnames:
                if frac_adopters[cellname] > perc / 100:
                    n_cells += 1
            x.append(n_cells)                    
            y.append(perc)
        xt, yt = torstenify(x, y)
        ax.plot(xt, yt, label=f"Generation {gen}")
    plt.grid()
    plt.xlabel('Antal kommuner')
    plt.ylabel('Above percentage adopters')
    # plt.legend()
    plt.title(area)


def tsv2out(area, tsv_filename, n_months_in_gen):
    def row2dict(r, keys):
        d = dict()
        for i, key in enumerate(keys):
            d[key] = int(r[i])
        return d

    grid = make_grid(area)

    # file = open(tsv_filename, encoding='utf-8', delimiter='\t')
    file = open(tsv_filename, encoding='utf-8')
    filerows = list(csv.reader(file, delimiter='\t'))
    file.close()

    filerows = filerows[:140]

    n_rows = len(filerows)
    kommun_names = [s.lower() for s in filerows[0][1:]]

    out = []
    out.append(grid.to_dict())

    done = False
    row_ind = 1
    while not done:
        for _ in range(n_months_in_gen):
            row = filerows[row_ind][1:]
            row_ind += 1
            done = (row_ind >= n_rows)
            if done:
                break
            row_dict = row2dict(row, kommun_names)
            grid.add(row_dict)
        out.append(grid.to_dict())
        grid.pretty_print()
    return out


if __name__ == "__main__":

    fig = plt.figure()

    # SIMULATED DATA
    ax = fig.add_subplot(2, 3, 1)
    grid = make_grid('sto')
    out = grid.sim(n_generations=10)
    #plot_s_curves(out)
    plot_torsten(ax, 'Stockholm simulated', out)

    # EMPIRICAL DATA
    ax = fig.add_subplot(2, 3, 4)
    N_MONTHS_IN_GENERATION = 14
    empirical_sto = tsv2out('sto', 'n_cars_sto.tsv', N_MONTHS_IN_GENERATION)
    # plot_s_curves(empirical_sto)
    plot_torsten(ax, 'Stockholm emprirical', empirical_sto)



    # SIMULATED DATA
    ax = fig.add_subplot(2, 3, 2)
    grid = make_grid('gbg')
    out = grid.sim(n_generations=10)
    #plot_s_curves(out)
    plot_torsten(ax, 'Gothenburg simulated', out)

    # EMPIRICAL DATA
    ax = fig.add_subplot(2, 3, 5)
    N_MONTHS_IN_GENERATION = 14
    empirical_sto = tsv2out('gbg', 'n_cars_gbg.tsv', N_MONTHS_IN_GENERATION)
    # plot_s_curves(empirical_sto)
    plot_torsten(ax, 'Gothenburg emprirical', empirical_sto)






    # SIMULATED DATA
    ax = fig.add_subplot(2, 3, 3)
    grid = make_grid('malmo')
    out = grid.sim(n_generations=10)
    #plot_s_curves(out)
    plot_torsten(ax, 'Malmö simulated', out)

    # EMPIRICAL DATA
    ax = fig.add_subplot(2, 3, 6)
    N_MONTHS_IN_GENERATION = 14
    empirical_sto = tsv2out('malmo', 'n_cars_malmo.tsv', N_MONTHS_IN_GENERATION)
    # plot_s_curves(empirical_sto)
    plot_torsten(ax, 'Malmö emprirical', empirical_sto)




    plt.show()

