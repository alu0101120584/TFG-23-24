import flet as ft
import json
import os
import firebase_admin
from firebase_admin import auth,storage,credentials
import pyrebase
from db.flet_pyrebase import PyrebaseWrapper

def UserView(page, myPyrebase):
    title = "App TFG Parlamento"
    
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
                                    alignment = ft.alignment.center,
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
    
    def upload(datos):
        #Obtener el email del usuario que esta logeado en la app
        user = myPyrebase.auth.get_account_info(myPyrebase.idToken)
        email = user['users'][0]['email']
        
        fileName = (email + 'resultados.json')
        
        print(fileName)
        ruta = ('./' + fileName)
        #Crear un fichero.json con los resultados
        with open(ruta, "w") as archivo:
            json.dump(datos, archivo)
        
        #Subir el fichero con los resultados del usuario a firebase    
        bucket = storage.bucket()
        blob = bucket.blob(os.path.basename(fileName))
        blob.upload_from_filename(fileName)
        
        # SI SE SUBE CON ÉXITO MOSTRAR UNA SNACKBAR
        page.snack_bar = ft.SnackBar(
            ft.Text("Fichero subido con éxito"),
            bgcolor="green"
        )
        page.snack_bar.open = True
        page.update()
        
        #Se elimina el archivo que se ha creado en local
        if os.path.exists(ruta):
            os.remove(ruta)

    
    username = ft.TextField(label="Nombre de usuario", width=300)   
    banner = ft.Text("Votación a las propuestas", weight = "bold", color = ft.colors.WHITE, size = 32)
    
    home_button = ft.TextButton("", icon=ft.icons.HOME_ROUNDED, icon_color=ft.colors.WHITE, on_click=lambda _:page.go('/'))
    logout_button = ft.FilledButton(
        " ",
        tooltip = "Cerrar sesión",
        icon=ft.icons.EXIT_TO_APP_ROUNDED,
        on_click=handle_logout,
        style=ft.ButtonStyle( 
            shape = ft.RoundedRectangleBorder(radius=0),
            bgcolor = "#043A68", 
            color = ft.colors.RED
        )
    )

    subir_button = ft.Container(
        alignment = ft.alignment.center,
        height = 40,
        bgcolor = "#043A68",
        width = 300,
        content = ft.Text(
            "Subir votación",
            color=ft.colors.WHITE,
            size=14,
            ),
        on_click= lambda e:upload(datos) 
        #on_click = lambda e:print_table(datos, './imprimir.json')
    )
    
    cabecera = ft.Container(
        padding = ft.padding.all(10),
        bgcolor="#043A68",
        content = ft.Row(
            [home_button, banner, logout_button],
            alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
        )    
    )
     
    mytable = ft.DataTable(
        heading_row_color="#043A68",
        heading_row_height = 60,
        heading_text_style = ft.TextStyle(size = 16, color = "white", weight="bold"),
        width=page.window_width/2,
        column_spacing=220,
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
            subir_button
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
        alignment=ft.MainAxisAlignment.CENTER,
        spacing = 50,
    )

                
    return {
        "view":myPage,
        "title": title,
        }