import flet as ft

# views
from views.index_view import IndexView
from views.register_view import RegisterView
from views.admin_view import AdminView
from views.user_view import UserView
from views.results_view import ResultsView
from views.prueba_view import PruebaView

import flet as ft

class Router:

    def __init__(self, page, myPyrebase):
        self.page = page
        self.routes = {
            "/": IndexView(page, myPyrebase),
            "/register": RegisterView(page, myPyrebase),
            "/adminView": AdminView(page, myPyrebase),
            "/userView": UserView(page, myPyrebase),
            "/resultView": ResultsView(page, myPyrebase),
            "/pruebaView": PruebaView(page, myPyrebase),
        }
        self.body = ft.Container(content=self.routes['/']["view"])

    def route_change(self, route):
        self.body.content = self.routes[route.route].get("view")
        self.page.title = self.routes[route.route].get("title")
        if self.routes[route.route].get("load"):
            self.routes[route.route].get("load")()
        self.page.update()
        
