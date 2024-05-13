import flet as ft
import json
from firebase_admin import credentials,initialize_app,storage
import os
from components.you_alert import YouAlert

mycred = credentials.Certificate("./db/servicio.json")
initialize_app(mycred,{'storageBucket':'tfg-parlamento.appspot.com'})

def AdminView(page, myPyrebase):
    title = "Admin View"
    you_selected = ft.Column()
    
    with open('./assets/propuestas.json', 'r') as archivo:
        # Carga el contenido del archivo JSON en una lista
        datos = json.load(archivo)
        
    def handle_sign_up(e):
        try:
            myPyrebase.register_user(name.value, username.value, email.value, password.value)
            name.value, username.value, email.value, password.value = '', '', '', ''
            page.go('/')
        except:
            handle_sign_in_error()

    def handle_sign_in_error():
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Completa todos los campos", color=ft.colors.WHITE),
            bgcolor=ft.colors.RED
        )
        page.snack_bar.open = True
        page.update()
    
    def handle_result(e):
        page.go('/resultView')
        
    def handle_logout(*e):
        username.value = ""
        myPyrebase.kill_all_streams()
        myPyrebase.sign_out()
        page.go("/")
    
    def load_table():
        for x in datos:
            mytable.rows.append(
                ft.DataRow(
                    selected = True,
                    cells = [
                        ft.DataCell(ft.Text(x['Propuesta'])),
                    ]
                )
            )
    
    async def uploadnow(e:ft.FilePickerResultEvent):
        for x in e.files:
            try:
                fileName = x.path
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
                print("Se ha subido el fichero con éxito")
            except Exception as e:
                print(e)
                print("Ha ocurrido un error en la subida del fichero")
    
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
    
    banner = ft.Text("Panel de control de administrador", weight = "bold", color = ft.colors.WHITE, size = 32)
    name = ft.TextField(label="Nombre", width=300)
    username = ft.TextField(label="Nombre de usuario", width=300)
    email = ft.TextField(label="Email", width=300)
    password = ft.TextField(label="Contraseña", width=300, password=True, can_reveal_password=True)
    
    home_button = ft.TextButton("", icon=ft.icons.HOME_ROUNDED, icon_color=ft.colors.WHITE, on_click=lambda _:page.go('/'))
    logout_button = ft.FilledButton(" ", tooltip = "Cerrar sesión", icon=ft.icons.EXIT_TO_APP_ROUNDED, on_click=handle_logout, style=ft.ButtonStyle( shape = ft.RoundedRectangleBorder(radius=0),  bgcolor = "#043A68", color = ft.colors.RED))
    
    register_button = ft.Container(
        alignment = ft.alignment.center,
        height = 40,
        bgcolor = "#043A68",
        width = 300,
        content = ft.Text(
            "Registrar",
            color=ft.colors.WHITE,
            size=14,
            ),
        on_click= handle_sign_up
    )
       
    result_button = ft.FilledButton(
        " ", tooltip = "Mostrar resultados",
        icon = ft.icons.PREVIEW,
        style = ft.ButtonStyle( shape = ft.RoundedRectangleBorder(radius=0), bgcolor = "#043A68", color = ft.colors.WHITE),
        disabled = False,
        on_click = handle_result
    )
    
    load_table()
    youalert = YouAlert(datos, mytable)
    file_picker = ft.FilePicker(on_result=uploadnow)
    
    myPage = ft.Column(
        width=page.window_width,
        controls = [
            ft.Container(
                padding = ft.padding.all(10),
                bgcolor="#043A68",
                content = ft.Row(
                    [home_button, banner, result_button, logout_button],
                    alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
                )    
            ),
            ft.Row(
                controls = [
                    ft.Container(
                        expand = 3,
                        content = ft.Column(
                            #alignment = ft.MainAxisAlignment.START,
                            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                            spacing = 40,
                            controls = [
                                ft.Text(
                                    "Cargar archivo que contiene las propuestas",
                                    size = 16,
                                    color = "#043A68",
                                    weight= ft.FontWeight.BOLD
                                ),
                                ft.FilledButton(
                                    "Seleccionar archivo",
                                    style=ft.ButtonStyle( shape = ft.RoundedRectangleBorder(radius=0), bgcolor = "#043A68", color = "white",),
                                    icon=ft.icons.UPLOAD_FILE,
                                    height=40,
                                    width=300,
                                    on_click=lambda e:file_picker.pick_files()
                                ),
                                youalert
                            ]
                        )
                    ),
                    ft.Container(
                        expand = 2,
                        padding = ft.padding.only(top=80),
                        content = ft.Column(
                            [
                                ft.Row(
                                    [name],
                                alignment=ft.MainAxisAlignment.CENTER
                                ),
                                ft.Row(
                                    [username],
                                alignment=ft.MainAxisAlignment.CENTER
                                ),
                                ft.Row(
                                    [email],
                                alignment=ft.MainAxisAlignment.CENTER
                                    ),
                                ft.Row(
                                    [password],
                                alignment=ft.MainAxisAlignment.CENTER
                                    ),
                                ft.Row(
                                    [register_button],
                                alignment=ft.MainAxisAlignment.CENTER),
                            ]
                        )
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )     
        ],
    )
    page.overlay.append(file_picker)
    myPage.expand = True

    return {
        "view":myPage,
        "title": "AdminView",
        }