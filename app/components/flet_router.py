import flet as ft

# views
from views.index_view import IndexView
from views.admin_view import AdminView
from views.user_view import UserView
from views.results_view import ResultsView

import flet as ft

class Router:

    def __init__(self, page, myPyrebase):
        self.page = page
        self.routes = {
            "/": IndexView(page, myPyrebase),
            "/adminView": AdminView(page, myPyrebase),
            "/userView": UserView(page, myPyrebase),
            "/resultView": ResultsView(page, myPyrebase),
        }
        self.body = ft.Container(content=self.routes['/']["view"])

    def route_change(self, route):
        self.body.content = self.routes[route.route].get("view")
        self.page.title = self.routes[route.route].get("title")
        if self.routes[route.route].get("load"):
            self.routes[route.route].get("load")()
        self.page.update()
        
# HAY QUE AÑADIR UN BOTÓN PARA ELIMINAR EL FICHERO DE PROPUESTAS ANTIGUO AUNQUE AL SUBIR UNO NUEVO SE SOBREESCRIBE AL TENER L MISMO NOMBRE, Y HAY QUE CONSIDERAR QUE LOS USUARIOS TENGAN QUE VOTAR EN NUEVOS FICHEROS
# TAMBIÉN HAY QUE CONSIDERAR QUE AL CERRAR CERSIÓN Y ABRIR CON OTRO USUARIO SE QUEDAN GUARDADOS LOS RESULTADOS DE LAS VOTACIONES (EN LOS SELECCIONABLES)
# POR ÚLTIMO EN LA MUESTRA DE RESULTADOS SE PODRÍAN DESTACAR DOS ERRORES (UNO POR SI EL USUSARIO AÚN NO HA REALIZADO SU VOTACIÓN ES DECIR SI NO EXISTE EL FICHERO Y OTRO
# POR SI NO HAY NINGUNA PROPUESTA CON ESE TIPO DE VOTACIÓN; SI,NO,ABSTENCIÓN)