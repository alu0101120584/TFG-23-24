import flet as ft
from components.fletRouter import Router
from db.flet_pyrebase import PyrebaseWrapper

def main(page: ft.Page):
    """
    Programa principal. Se encarga de inicializar el Router que gestionará los cambios entre
    las distintas vistas de la app.
    """
    
    page.window_height = 700
    page.window_width = 1000
    page.scroll = "auto"
    page.window_maximizable = False
    page.window_resizable = False
        
    myPyrebase = PyrebaseWrapper(page)
    myRouter = Router(page, myPyrebase)

    page.on_route_change = myRouter.routeChange

    page.add(
        myRouter.body
    )

    page.go('/')
    
if __name__ == "__main__":
    ft.app(target=main, assets_dir='assets', upload_dir="upload")

    