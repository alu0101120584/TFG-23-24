import flet as ft
import json
import firebase_admin
from firebase_admin import storage,credentials

def UserView(page, myPyrebase):
    
    def handle_logout(*e):
        username.value = ""
        myPyrebase.kill_all_streams()
        myPyrebase.sign_out()
        page.go("/")
    
    def vote(e,data,index):
        you_edit = e.control.value
        for i ,x in enumerate(datos):
            if i == index:
                datos[index]['Voto'] = you_edit
                break

        page.update()

    def print_table(diccionario, ruta_archivo):
        #with open(ruta_archivo, "w") as archivo:
        #    json.dump(diccionario, archivo)
        print(diccionario)
            
    def load_table():
        for i,x in enumerate(datos):
            mytable.rows.append(
                ft.DataRow(
                    cells = [
                        ft.DataCell(
                            ft.Text(x['Propuesta'], size=16, weight="bold"),
                        ),
                        ft.DataCell(
                            ft.Row([
                                ft.Dropdown(
                                    on_change=lambda e, i=i:vote(e,x,i),
                                    border=ft.InputBorder.NONE,
                                    hint_text="   -   ",
                                    width = 100,
                                    options = [
                                        ft.dropdown.Option("Si"),
                                        ft.dropdown.Option("No"),
                                        ft.dropdown.Option("Abstencion")
                                    ]
                                )
                            ])
                        ),
                    ]
                )
            )
    
    def descargar_archivo(nombre_archivo):
        # Nombre del archivo que deseas descargar
        blob = storage.bucket().blob(nombre_archivo)

        # Descarga el archivo a la ubicación especificada
        blob.download_to_filename("./assets/download/propuestas.json")
    
    username = ft.TextField(label="Nombre de usuario", width=300)   
    home_button = ft.TextButton("", icon=ft.icons.HOME_ROUNDED, icon_color=ft.colors.WHITE, on_click=lambda _:page.go('/'))
    logout_button = ft.FilledButton(" ", tooltip = "Cerrar sesión", icon=ft.icons.EXIT_TO_APP_ROUNDED, on_click=handle_logout, style=ft.ButtonStyle( shape = ft.RoundedRectangleBorder(radius=0),  bgcolor = "#043A68", color = ft.colors.RED))
    banner = ft.Text("Votación a las propuestas", weight = "bold", color = ft.colors.WHITE, size = 32)
    cabecera = ft.Container(
        padding = ft.padding.all(10),
        bgcolor="#043A68",
        content = ft.Row(
            [home_button, banner, logout_button],
            alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
        )    
    )
     
    mytable = ft.DataTable(
		columns=[
			ft.DataColumn(ft.Text("Propuesta")),
            ft.DataColumn(ft.Text("Voto")),
			],
		rows=[], 
		)
    
    with open('./assets/propuestas.json', 'r') as archivo:
        # Carga el contenido del archivo JSON en una lista
        datos = json.load(archivo)
            
    load_table()
    descargar_archivo("propuestas.json")
    
    myPage = ft.Column( 
        controls = [
            cabecera,
            mytable,
            ft.ElevatedButton(
                "Boton",
                on_click = lambda e: print(datos)
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
        alignment=ft.MainAxisAlignment.CENTER,
        spacing = 50,
    )

                
    return {
        "view":myPage,
        "title": "userView",
        }