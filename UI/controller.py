import flet as ft
from UI.view import View
from model.model import Model


class Controller:

    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def fillDDLocation(self):
        listaLoc = self._model.getLocalization()
        listaLoc.sort(key = lambda x: x[0], reverse = True)
        options = map(lambda x : ft.dropdown.Option(x), listaLoc)
        self._view.dd_localization.options = options
        self._view.update_page()

    def handle_graph(self, e):
        localization = self._view.dd_localization.value
        if localization is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Attenzione, selezionare una Localization dal menù", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(localization)
        nNodes, nEdges = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato con {nNodes} nodi  e {nEdges} archi", color="green"))
        self._view.update_page()

        listaArchiOrd = self._model.getSortedEdges()
        for e in listaArchiOrd:
            self._view.txt_result.controls.append(ft.Text(f"{e[0]} <--> {e[1]} peso = {e[2]}"))

        self._view.update_page()


    def analyze_graph(self, e):
        cc = self._model.getComponenteConnessa()
        self._view.txt_result.controls.append(ft.Text(f"Le componenti connesse sono: "))
        for c in cc:
            listaGeni = []
            for i in c:
                listaGeni.append(i.GeneID)
            self._view.txt_result.controls.append(ft.Text(f"{listaGeni} || lunghezza della componente {len(c)}"))
        self._view.update_page()


    def handle_path(self, e):
        pass

