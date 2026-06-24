import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self.p2 = None
        self.p1 = None

    def fillC(self):
        self.c = self._model.getC()
        for y in self.c:
            self._view._ddcategory.options.append(ft.dropdown.Option(key=y[0],
                                                                     text=y[1]))
        self._view.update_page()

    def fillDDr(self):
        self.p = self._model.getNodi()
        for y in self.p:
            self._view._ddProdStart.options.append(ft.dropdown.Option(key=y.product_id,
                                                                     text=y.product_name,
                                                                     data=y,
                                                                     on_click=self.choice1))
            self._view._ddProdEnd.options.append(ft.dropdown.Option(key=y.product_id,
                                                                     text=y.product_name,
                                                                     data=y,
                                                                     on_click=self.choice2))
        self._view.update_page()

    def choice1(self, e):
        self.p1 = e.control.data

    def choice2(self, e):
        self.p2 = e.control.data


    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        self.cc = self._view._ddcategory.value
        self._d1 = self._view._dp1.value
        self._d2 = self._view._dp2.value

        if self.cc is None or self._d1 is None or self._d2 is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("seleziona categoria o anni giusti"))
            self._view.update_page()
            return

        if self._d1 > self._d2:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("seleziona anni in ordine"))
            self._view.update_page()
            return

        self._model.creaG(self.cc, self._d1, self._d2)
        self._view.txt_result.controls.clear()
        nodi, archi = self._model.len()
        self._view.txt_result.controls.append(ft.Text(f"grafo creato con nodi {nodi} e archi {archi}"))
        self.fillDDr()
        self._view.update_page()

    def handleBestProdotti(self, e):
        lista = self._model.bestProdotti()
        for l in lista:
            self._view.txt_result.controls.append(ft.Text(f"{l}"))
        self._view.update_page()

    def handleCercaCammino(self, e):
        self.l = self._view._txtInLun.value
        if self.l is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("seleziona lunghezza"))
            self._view.update_page()
            return

        try:
            self.l = int(self.l)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("seleziona lunghezza intera"))
            self._view.update_page()
            return

        if self._d1 is None or self._d2 is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("seleziona"))
            self._view.update_page()
            return

        best, somma = self._model.cerca(self.p1, self.p2, self.l)
        if len(best) == 0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("non esiste"))
            self._view.update_page()
            return
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"{somma}"))
        for l in best:
            self._view.txt_result.controls.append(ft.Text(f"{l}"))
        self._view.update_page()




    def setDates(self):
        first, last = self._model.getDateRange()

        self._view._dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view._dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp2.current_date = datetime.date(last.year, last.month, last.day)
