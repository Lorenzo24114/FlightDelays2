import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceArrivo=None
        self._choicePartenza=None

    def handleAnalizza(self,e):
        cMinTxt=self._view._txtInCMin.value
        if cMinTxt is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire un valore per numero minimo di compagnie", color="red"))
            self._view.update_page()
            return
        try:
            cMin=int(cMinTxt)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire un valore intero", color="red"))
            self._view.update_page()
            return
        
        if cMin<=0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire un valore per numero minimo di compagnie che sia un intero positivo", color="red"))
            self._view.update_page()
            return
        
        self._model.buildGraph(cMin)
        allNodes=self._model.getAllNodes()
        self._fillDropdown(allNodes)

        nNodes,nEdges=self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo creato", color="green"))
        self._view.txt_result.controls.append(ft.Text(f"Grafo contiene: n nodi {nNodes}, n edge{nEdges}", color="green"))
        self._view.update_page()

        self.fillDropdown()

    def handleConnessi(self,e):
        if self._choicePartenza is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire un aeroporto di partenza", color="red"))
            self._view.update_page()
            return
        viciniT=self._model.getViciniOrdinati(self._choicePartenza)
        self._view.txt_result.controls.clear()
        for v in viciniT:
            self._view.txt_result.controls.append(ft.Text(f"{v[0]} - peso : {v[1]}"))
            self._view.update_page()

    def handleCerca(self,e):
        if self._choicePartenza is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire un aeroporto di partenza", color="red"))
            self._view.update_page()
            return
        if self._choiceArrivo is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire un aeroporto di arrivo", color="red"))
            self._view.update_page()
            return
        t=self._view._txtInNTratteMax.value
        try:
            tInt=int(t)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire un valore intero positvo", color="red"))
            self._view.update_page()
            return
        
        path,score=self._model.getCamminoOttimo(self._choicePartenza,self._choiceArrivo,tInt)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Cammino tra {self._choicePartenza} e {self._choiceArrivo} trovato", color="green"))
        self._view.txt_result.controls.append(ft.Text(f"Cammino ha uno score di  {score} e contiene i seguenti nodi:", ))
        for p in path:
            self._view.txt_result.controls.append(ft.Text(f"{p}"))
        self._view.update_page()
    def handleTestConnessione(self,e):
        if self._choicePartenza is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire un aeroporto di partenza", color="red"))
            self._view.update_page()
            return
        if self._choiceArrivo is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire un aeroporto di arrivo", color="red"))
            self._view.update_page()
            return
        if not self._model.hasPath(self._choicePartenza,self._choiceArrivo):
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Non ho trovato un cammino tra {self._choicePartenza} e {self._choiceArrivo}", color="orange"))
            self._view.update_page()
            return
        path=self._model.getPath(self._choicePartenza,self._choiceArrivo)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Ho trovato un cammino tra {self._choicePartenza} e {self._choiceArrivo}. Di seguito i nodi che compongono il cammino:",))
            
        for p in path:
            self._view.txt_result.controls.append(ft.Text(f"{p}"))
        self._view.update_page()

    def _fillDropdown(self,allNodes):
        for n in allNodes:
            self._view._ddAeroportoP.options.append(ft.dropdown.Option(data=n,key=n.IATA_CODE,on_click=self._choiceDDPartenza))
        
            self._view._ddAeroportoA.options.append(ft.dropdown.Option(data=n,key=n.IATA_CODE,on_click=self._choiceDDArrivo))

    def _choiceDDPartenza(self,e):
        self._choicePartenza=e.control.data
    
    def _choiceDDArrivo(self,e):
        self._choiceArrivo=e.control.data