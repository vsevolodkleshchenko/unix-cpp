import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import scipy.spatial.distance as ssd
import random
import time
import collections


class Car:
    def __init__(self, city):
        n_nodes = city.number_of_nodes()
        start = random.randint(0, n_nodes - 1)
        end = random.randint(0, n_nodes - 1)
        while start == end:
            end = random.randint(0, n_nodes - 1)
        self.pos = start
        self.neighs = [neigh for neigh in city.neighbors(start)]
        self.dir = None
        self.aim = end
        self.status = 'alive'

    def _check(self):
        if self.status == 'finished':
            pass

    def aim_distance(self, city):
        return ssd.pdist([city.nodes[self.pos]['pos'], city.nodes[self.aim]['pos']])

    def update(self, city):
        self.pos = self.dir
        self.neighs = [neigh for neigh in city.neighbors(self.dir)]
        if self.dir == self.aim:
            self.status = 'finished'
        self.dir = None
        self._check()

    def go(self, city):
        best_neigh = random.sample(self.neighs, 1)[0]
        best_distance = ssd.pdist([city.nodes[best_neigh]['pos'], city.nodes[self.aim]['pos']])
        for neigh in self.neighs:
            neigh_distance = ssd.pdist([city.nodes[neigh]['pos'], city.nodes[self.aim]['pos']])
            if neigh_distance <= best_distance:
                best_neigh = neigh
                best_distance = neigh_distance
        self.dir = best_neigh


class Traffic:
    def __init__(self, city, n_cars, trackers=None, dt=0.35):
        self.cars = [Car(city) for _ in range(n_cars)]
        self.city = city
        self.time = 6.
        self.dt = dt
        self.workload = []
        self.problems = []
        self.trackers = trackers
        if self.trackers is not None:
            self.tracks = [[] for _ in range(len(trackers))]
        self.set_drawing_setting()

    def set_drawing_setting(self):
        plt.ion()
        self.figure, self.axis = plt.subplots(1, 2, figsize=(13, 5))
        self.axis[1].set_xlabel('time')
        self.axis[1].set_ylabel('# cars')

    @property
    def n_cars(self):
        return len(self.cars)

    def update(self):
        for car in self.cars:
            car.update(self.city)
            if car.status == 'finished':
                self.cars.remove(car)
        self.time += self.dt

    def update_tracks(self):
        if self.trackers is not None:
            for t, track in enumerate(self.tracks):
                track.append(self.city[self.trackers[t][0]][self.trackers[t][1]]['weight'])

    def add_cars(self, n_cars):
        if self.time < 7 or 10 < self.time < 16 or 22 < self.time < 24:
            pass
        if 7 <= self.time <= 9 or 17 <= self.time <= 20:
            n_cars *= 10
        else:
            n_cars *= 3
        for i in range(n_cars):
            self.cars.append(Car(self.city))

    def unmeasure(self):
        for car in self.cars:
            self.city[car.pos][car.dir]['weight'] = 0

    def measure(self):
        for car in self.cars:
            self.city[car.pos][car.dir]['weight'] += 1
        self.workload.append(self.n_cars)
        self.big = [(u, v) for (u, v, d) in self.city.edges(data=True) if d["weight"] >= 10]
        self.norm = [(u, v) for (u, v, d) in self.city.edges(data=True) if 3 < d["weight"] < 10]
        self.small = [(u, v) for (u, v, d) in self.city.edges(data=True) if d["weight"] <= 3]
        self.problems.extend(self.big)

    def go(self):
        self.add_cars(15)
        for car in self.cars:
            car.go(self.city)
        self.measure()
        self.update_tracks()
        self.visualise()
        self.unmeasure()
        self.update()

    def simulate(self):
        while self.time <= 23:
            self.go()
        print("Самые загруженные участки:", collections.Counter(self.problems).most_common(5), sep='\n')
        plt.ioff()
        plt.close(self.figure)

    def visualise(self):
        edge_labels = nx.get_edge_attributes(self.city, "weight")
        node_poses = nx.get_node_attributes(self.city, "pos")
        nx.draw(self.city, node_poses, ax=self.axis[0], with_labels=True)
        nx.draw_networkx_nodes(self.city, node_poses, node_size=60, ax=self.axis[0])
        nx.draw_networkx_edges(self.city, node_poses, edgelist=self.big, width=1.8, edge_color="r", ax=self.axis[0])
        nx.draw_networkx_edges(self.city, node_poses, edgelist=self.norm, width=1.8, edge_color="b", ax=self.axis[0])
        nx.draw_networkx_edges(self.city, node_poses, edgelist=self.small, width=1.8, edge_color="g", ax=self.axis[0])
        nx.draw_networkx_edge_labels(self.city, node_poses, edge_labels, ax=self.axis[0])
        timing = [6. + i * self.dt for i in range(len(self.workload))]
        self.figure.suptitle(f'{self.time}')
        self.axis[1].bar(timing, self.workload)
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
        self.axis[0].cla()
        self.axis[1].cla()


def plot_analytics(trfc):
    fig1, axs1 = plt.subplots(1, 2, figsize=(12, 5))
    node_poses = nx.get_node_attributes(trfc.city, "pos")
    nx.draw(trfc.city, node_poses, with_labels=True, ax=axs1[0])
    if trfc.tracks is not None:
        for track in trfc.tracks:
            time = [6. + i * trfc.dt for i in range(len(track))]
            axs1[1].plot(time, track)
    axs1[1].legend(trfc.trackers)
    plt.show()


def build_graph():
    g = nx.random_geometric_graph(15, radius=0.4, seed=3)
    node_poses = nx.spring_layout(g, seed=7)
    nx.set_edge_attributes(g, values=0, name='weight')
    nx.set_node_attributes(g, values=node_poses, name='pos')
    return g, node_poses


if __name__ == '__main__':
    # graph, nposes = build_graph()
    #
    # traffic = Traffic(graph, n_cars=30, trackers=[(6, 7), (1, 4), (0, 3)])
    # traffic.simulate()
    # plot_analytics(traffic)

    new_graph, new_nposes = build_graph()
    new_graph.add_edge(4, 3, weight=0)
    new_graph.add_edge(4, 6, weight=0)
    new_graph.add_edge(1, 7, weight=0)
    # fig, axs = plt.subplots(1, 2, figsize=(14, 7))
    # nx.draw(graph, nposes, with_labels=True, ax=axs[0])
    # nx.draw(new_graph, new_nposes, with_labels=True, ax=axs[1])
    # plt.show()

    new_traffic = Traffic(new_graph, n_cars=30, trackers=[(6, 7), (1, 4), (0, 3)])
    new_traffic.simulate()
    plot_analytics(new_traffic)
