import flet as ft
from firebase_admin import auth,storage,credentials
import json
import os
from components.you_alert import YouAlert

def ResultsView(page, myPyrebase):
    title = "App TFG Parlamento"
    def handle_admin(e):
        for i in range(len(cartas)):
            page.controls.pop()
            page.update()
        
        cartas.clear()
        page.go('/adminView')
        
    def handle_logout(*e):
        for i in range(len(cartas)):
            page.controls.pop()
            page.update()
        cartas.clear()
        username.value = ""
        myPyrebase.kill_all_streams()
        myPyrebase.sign_out()
        page.go("/")
    
    def delete_file(file_path):
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"El archivo {file_path} ha sido eliminado con éxito.")
            except Exception as e:
                print(f"Ocurrió un error al intentar eliminar el archivo: {e}")
        else:
            print(f"El archivo {file_path} no existe.")
    
    def obtener_todos_los_usuarios():
        usuarios = []
        # Obtiene los usuarios de la primera página
        pagina = auth.list_users()
        # Agrega los usuarios de la primera página a la lista
        for usuario in pagina.users:
            usuarios.append(usuario)
        # Itera sobre las páginas restantes y agrega los usuarios a la lista
        while pagina.has_next_page:
            pagina = pagina.get_next_page()
            for usuario in pagina.users:
                usuarios.append(usuario)
        #Se elimina el usuario admin de la lista de usuarios        
        for usuario in usuarios:
            email = usuario.email
            email_str = str(email)
            if email_str == 'admin@gmail.com':
                usuarios.remove(usuario)
        return usuarios
    
    def descargar_archivos():
        for usuario in lista_usuarios:
            fileName = (usuario.email + 'resultados.json')
            # Nombre del archivo que deseas descargar
            blob = storage.bucket().blob(fileName)
            # Descarga el archivo a la ubicación especificada
            if blob.exists():
                try:
                    ruta = ('./assets/download/' + fileName)
                    blob.download_to_filename(ruta)
                    datos_entrada = cargar_datos(ruta)
                    lista_usuariovotos.append([usuario.email, datos_entrada])
                    print(f"El archivo '{fileName}' ha sido descargado correctamente.")
                except Exception as e:
                    print(f"No se pudo descargar el archivo '{fileName}': {e}")
            else:
                print(f"El archivo '{fileName}' no existe en Google Cloud Storage.")
                                    
    cartas = []
    lista_usuarios = obtener_todos_los_usuarios()
    lista_usuariovotos = []
    mytable = ft.DataTable(
		# AND ENABLE CHECKBOX FOR SELECT multiple
		heading_row_color="#043A68",
        heading_row_height = 60,
        heading_text_style = ft.TextStyle(size = 16, color = "white", weight="bold"),
        show_checkbox_column=False,
		columns=[
			ft.DataColumn(ft.Text("Propuesta")),
			],
		rows=[],
        width=page.window_width
		)
    dlg = ft.AlertDialog(
        content = ft.Column(
            [mytable],
            scroll=ft.ScrollMode.ALWAYS,
            )
    )
    #Función que se encarga de agrupar las propuestas según la intención de voto
    def completar_overlay(lista_datos):
        # Creamos un diccionario para almacenar los elementos agrupados por Voto
        grupos = {}
        # Iteramos sobre la entrada de datos y los agrupamos por Usuario y Voto
        for usuario, propuestas in lista_datos:
            if usuario not in grupos:
                grupos[usuario] = {}
            for propuesta in propuestas:
                voto = propuesta["Voto"]
                if voto not in grupos[usuario]:
                    grupos[usuario][voto] = []
                grupos[usuario][voto].append(propuesta)
        
        #Impresión de las propuestas según la intención de voto de cada usuario
        for usuario, propuestas in grupos.items():
            for voto, propuestas_voto in propuestas.items():
                for propuesta in propuestas_voto:
                    print("Propuesta:", propuesta)
        
        return grupos  
    
    def cargar_datos(ruta_archivo):
        try:
            with open(ruta_archivo, 'r') as archivo:
                datos = json.load(archivo)

            print("Datos cargados correctamente.")
            return datos
        except FileNotFoundError:
            print(f"El archivo {ruta_archivo} no fue encontrado.")
        except json.JSONDecodeError:
            print(f"Error al decodificar el archivo JSON {ruta_archivo}.")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
        
    def load_table(datos):
        mytable.rows.clear()
        for x in datos:
            mytable.rows.append(
                ft.DataRow(
                    selected = True,
                    cells = [
                        ft.DataCell(ft.Text(x['Propuesta'])),
                    ]
                )
            )  
    
    def open_dlg(datos):
        if datos is None:
            snackbar = ft.SnackBar(
                content=ft.Text("No hay ninguna propuesta con este resultado"),
                duration=2000,
                bgcolor="red"
            )
            page.snack_bar = snackbar
            page.snack_bar.open = True
            page.update()
        else:
            load_table(datos)
            page.dialog = dlg
            dlg.open = True
            page.update()
    
    def create_carta(nombre, grupos):
        email = "@gmail.com"
        resultado = nombre.replace(email, "") 
        si = grupos.get(nombre, {}).get('Si', None)
        no = grupos.get(nombre, {}).get('No', None)
        abstencion = grupos.get(nombre, {}).get('Abstencion', None)
        print(nombre)
        print(si)
        carta = ft.Card(
            content=ft.Container(
                width=500,
                content=ft.Column(
                    [
                        ft.ListTile(
                            title=ft.Text(f"Resumen de votaciones del usuario {resultado}", color="white", weight="bold",size=16),
                        ),
                        ft.ListTile(
                            title=ft.Text("Agrupación Sí", color="white"),
                            trailing=ft.ElevatedButton("Mostrar", bgcolor="#facf25", color = "#043A68", on_click= lambda e :open_dlg(si)),
                        ),
                        ft.ListTile(
                            title=ft.Text("Agrupación No", color="white"),
                            trailing=ft.ElevatedButton("Mostrar", bgcolor="#facf25", color = "#043A68", on_click= lambda f :open_dlg(no)),
                        ),
                        ft.ListTile(
                            title=ft.Text("Agrupación Abstención", color="white"),
                            trailing=ft.ElevatedButton("Mostrar", bgcolor="#facf25", color = "#043A68", on_click= lambda g :open_dlg(abstencion)),
                        ),
                    ],
                    spacing=0,
                ),
                padding=ft.padding.symmetric(vertical=10),
            ),
            color="#043A68",
        )
        page.update()
        return carta
    
    
    def create_overlay(grupos):
        for usuario in lista_usuarios:
            cartas.append(create_carta(usuario.email, grupos))
            fichero = "./assets/download/" + usuario.email + "resultados.json"
            delete_file(fichero)
        
        for carta in cartas:
            page.add(carta)
        
        
    
    username = ft.TextField(label="Nombre de usuario", width=300)
    banner = ft.Text("Resultados de las votaciones", weight = "bold", color = ft.colors.WHITE, size = 32)
    home_button = ft.TextButton("", icon=ft.icons.HOME_ROUNDED, icon_color=ft.colors.WHITE, on_click=lambda _:page.go('/'))
    logout_button = ft.FilledButton(" ", tooltip = "Cerrar sesión", icon=ft.icons.EXIT_TO_APP_ROUNDED, on_click=handle_logout, style=ft.ButtonStyle( shape = ft.RoundedRectangleBorder(radius=0),  bgcolor = "#043A68", color = ft.colors.RED))
    admin_button = ft.FilledButton(
        " ", tooltip = "Panel de administrador",
        icon = ft.icons.ADMIN_PANEL_SETTINGS_OUTLINED,
        style = ft.ButtonStyle( shape = ft.RoundedRectangleBorder(radius=0), bgcolor = "#043A68", color = ft.colors.WHITE),
        disabled = False,
        on_click = handle_admin
    )
    navbar = ft.Container(
        padding = ft.padding.all(10),
        bgcolor="#043A68",
        content = ft.Row(
            [home_button, banner, admin_button, logout_button],
            alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
        )    
    )
    boton =  ft.ElevatedButton("Cargar los resultados",
        bgcolor="#043A68", color = "white",
        on_click = lambda e :create_overlay(completar_overlay(lista_usuariovotos)))
     
    myPage = ft.Column(
        [navbar,boton],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    
    return {
        "view":myPage,
        "title": title,
        "load": descargar_archivos
        }
    
    #FALTA ELIMINAR LOS FICHEROS QUE SE DESCARGUEN