import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.g = nx.DiGraph()
        self.mappa = {}
        self.n = []
        pass

    def creaG(self, c, min, max):
        self.g.clear()
        self.n = DAO.getN(c)
        for n in self.n:
            self.mappa[n.product_id] = n
        self.g.add_nodes_from(self.n)

        self.a = DAO.getA(c, min, max)
        print(f"archi da query: {len(self.a)}")  # ← aggiungi questo
        cont_else = 0
        for a in self.a:
            if a[2] < a[3]:
                self.g.add_edge(self.mappa[a[0]], self.mappa[a[1]], weight = int(a[4]))
            elif a[2] > a[3]:
                self.g.add_edge(self.mappa[a[1]], self.mappa[a[0]], weight=int(a[4]))
            else:
                cont_else += 1
                self.g.add_edge(self.mappa[a[0]], self.mappa[a[1]], weight=int(a[4]))
                self.g.add_edge(self.mappa[a[1]], self.mappa[a[0]], weight=int(a[4]))

        print("coppie =", len(self.a))
        print("parita =", cont_else)
        print("archi =", self.g.number_of_edges())

    def len(self):
        return len(self.g.nodes), len(self.g.edges)

    def bestProdotti(self):
        lista = []
        for n in self.g.nodes():
            e = 0
            u = 0
            for ae in self.g.in_edges(n, data=True):
                e += ae[2]["weight"]
            for au in self.g.out_edges(n, data=True):
                u += au[2]["weight"]
            somma = e-u
            lista.append((n, somma))
        listao = sorted(lista, key=lambda x: x[1], reverse=True)
        return listao[:5]

    def getC(self):
        return DAO.getC()

    def getNodi(self):
        return self.n

    def getDateRange(self):
        return DAO.getDateRange()


    def cerca(self, s, e, l):
        self.best = []
        self.punti = 0
        parziale = [s]
        self.ric(parziale, l, e)
        return self.best, self.punti

    def ric(self, parziale, l, end):
        if len(parziale) == l and parziale[-1] == end:
            if self.costo(parziale) > self.punti:
                self.best = copy.deepcopy(parziale)
                self.punti = self.costo(parziale)
                return

        for n in self.g.successors(parziale[-1]):
            if n not in parziale and len(parziale) < l:
                parziale.append(n)
                self.ric(parziale, l, end)
                parziale.pop()

    def costo(self, parziale):
        somma = 0
        for i in range(0, len(parziale)-1):
            somma += self.g[parziale[i]][parziale[i+1]]["weight"]

        return somma

