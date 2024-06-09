import flet as ft
import json
from firebase_admin import credentials,initialize_app,storage
import os
from components.youAlert import YouAlert

mycred = credentials.Certificate("./db/servicio.json")
initialize_app(mycred,{'storageBucket':'tfg-parlamento.appspot.com'})

def AdminView(page, myPyrebase):
    title = "App TFG Parlamento"
    
    with open('../assets/propuestas.json', 'r') as archivo:
        # Carga el contenido del archivo JSON en una lista
        datos = json.load(archivo)
    
    def validateInputs():
        emailValue = email.value
        passwordValue = password.value

        # Verificar longitud de la contraseña
        if len(passwordValue) < 8:
            showSnackbar("La contraseña debe tener al menos 8 caracteres.")
            return False

        # Verificar formato del correo electrónico
        if "@" not in emailValue or "." not in emailValue:
            showSnackbar("Por favor, introduce un correo electrónico válido.")
            return False

        return True

    def showSnackbar(message):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color=ft.colors.WHITE),
            bgcolor=ft.colors.RED,
            duration=2000
        )
        page.snack_bar.open = True
        page.update()
    
    def handleSignUp(e):
        if validateInputs():
            try:
                myPyrebase.register_user(name.value, username.value, email.value, password.value)
                name.value, username.value, email.value, password.value = '', '', '', ''
                page.go('/')
            except:
                handleSignInError()

    def handleSignInError():
        showSnackbar("Error al registrar usuario. Por favor, inténtalo de nuevo.")
    
    def handleResult(e):
        page.go('/resultView')
        
    def handleLogout(*e):
        username.value = ""
        myPyrebase.kill_all_streams()
        myPyrebase.sign_out()
        page.go("/")
    
    def loadTable():
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
    
    async def uploadFile(e:ft.FilePickerResultEvent):
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
                
    def deleteVotes():
        pass
    
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
    
    homeButton = ft.TextButton("", icon=ft.icons.HOME_ROUNDED, icon_color=ft.colors.WHITE, on_click=lambda _:page.go('/'))
    logoutButton = ft.FilledButton(" ", tooltip = "Cerrar sesión", icon=ft.icons.EXIT_TO_APP_ROUNDED, on_click=handleLogout, style=ft.ButtonStyle( shape = ft.RoundedRectangleBorder(radius=0),  bgcolor = "#043A68", color = ft.colors.RED))
    
    registerButton = ft.Container(
        alignment = ft.alignment.center,
        height = 40,
        bgcolor = "#043A68",
        width = 300,
        content = ft.Text(
            "Registrar",
            color=ft.colors.WHITE,
            size=16,
            ),
        on_click= handleSignUp
    )
       
    resultButton = ft.FilledButton(
        " ", tooltip = "Mostrar resultados",
        icon = ft.icons.PREVIEW,
        style = ft.ButtonStyle( shape = ft.RoundedRectangleBorder(radius=0), bgcolor = "#043A68", color = ft.colors.WHITE),
        disabled = False,
        on_click = handleResult
    )
    
    loadTable()
    youalert = YouAlert(datos, mytable)
    file_picker = ft.FilePicker(on_result=uploadFile)
    
    myPage = ft.Column(
        width=page.window_width,
        controls = [
            ft.Container(
                padding = ft.padding.all(10),
                bgcolor="#043A68",
                content = ft.Row(
                    [homeButton, banner, resultButton, logoutButton],
                    alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
                )    
            ),
            ft.Row(
                controls = [
                    ft.Container(
                        expand = 3,
                        content = ft.Column(
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
                                youalert,
                                ft.Text(
                                    "Eliminar los votos de los usuarios en Firebase",
                                    size = 16,
                                    color = "#043A68",
                                    weight= ft.FontWeight.BOLD
                                ),
                                ft.FilledButton(
                                    "Eliminar",
                                    style=ft.ButtonStyle( shape = ft.RoundedRectangleBorder(radius=0), bgcolor = "#043A68", color = "white",),
                                    icon=ft.icons.UPLOAD_FILE,
                                    height=40,
                                    width=300,
                                    on_click=lambda e:deleteVotes
                                )
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
                                    [registerButton],
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
        "title": title,
        }