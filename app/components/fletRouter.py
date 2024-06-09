import flet as ft

from views.indexView import IndexView
from views.adminView import AdminView
from views.userView import UserView
from views.resultsView import ResultsView

import flet as ft

class Router:
    """Representa un enrutador para la aplicación.
    
    Attributes:
        page (flet.Page)
        routes (diccionario Python)
        body (flet.Container)
    """

    def __init__(self, page, myPyrebase):
        """Inicializa en objeto de tipo Router.

        Args:
            self
            page (flet.Page)
            myPyrebase (PyrebaseWrapper)
        """
        self.page = page
        self.routes = {
            "/": IndexView(page, myPyrebase),
            "/adminView": AdminView(page, myPyrebase),
            "/userView": UserView(page, myPyrebase),
            "/resultView": ResultsView(page, myPyrebase),
        }
        self.body = ft.Container(content=self.routes['/']["view"])

    def routeChange(self, route):
        """Se encarga de actualizar el contenido de la Page de Flet

        Args:
            route (diccionario Python)
        """
        self.body.content = self.routes[route.route].get("view")
        self.page.title = self.routes[route.route].get("title")
        if self.routes[route.route].get("load"):
            self.routes[route.route].get("load")()
        self.page.update()