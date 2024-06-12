import flet as ft
from firebase_admin import auth,storage,credentials
import json
import io
from components.youAlert import YouAlert

def ResultsView(page, myPyrebase):
    title = "App TFG Parlamento"
    flag = bool
    tb = ft.DataTable(
            border = ft.border.all(1, "black"),
            width = 1000,
            divider_thickness = 2,
            horizontal_lines = ft.border.BorderSide(1, "black"),
            heading_row_color="#043A68",
            data_row_color="#BFD7FF",
            columns = [
                ft.DataColumn(ft.Text("Propuestas", color="white", weight="bold", size = 16)),
                ft.DataColumn(ft.Text("Votaciones", color="white", weight="bold", size = 16))
            ],
            rows = []
        )
    
    def handleAdmin(e):
        if flag:
            page.controls.pop()
            page.update()
        for i in range(len(cards)):
            page.controls.pop()
            page.update()
        cards.clear()
        loadButton.disabled = False
        allButton.disabled = False
        page.go('/adminView')
        
    def handleLogout(*e):
        if flag:
            page.controls.pop()
            page.update()
        for i in range(len(cards)):
            page.controls.pop()
            page.update()
        cards.clear()
        username.value = ""
        myPyrebase.kill_all_streams()
        myPyrebase.sign_out()
        loadButton.disabled = False
        allButton.disabled = False
        page.go("/")
    
    def getAllUsers():
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
    
    def loadData(file_content):
        return json.load(io.StringIO(file_content))
    
    def downloadFile():
        for user in userList:
            fileName = f'{user.email}resultados.json'
            # Nombre del archivo que deseas leer
            blob = storage.bucket().blob(fileName)

            # Comprobar si el blob existe antes de intentar leerlo
            if blob.exists():
                try:
                    # Leer el contenido del archivo en memoria
                    content = blob.download_as_text()
                    datos_entrada = loadData(content)
                    resultsUserList.append([user.email, datos_entrada])
                except Exception as e:
                    print(f"No se pudo leer el archivo '{fileName}': {e}")
                                   
    cards = []
    userList = getAllUsers()
    resultsUserList = []
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
    def completeOverlay(lista_datos):
        # Creamos un diccionario para almacenar los elementos agrupados por Voto
        groups = {}
        # Iteramos sobre la entrada de datos y los agrupamos por Usuario y Voto
        for usuario, propuestas in lista_datos:
            if usuario not in groups:
                groups[usuario] = {}
            for propuesta in propuestas:
                voto = propuesta["Voto"]
                if voto not in groups[usuario]:
                    groups[usuario][voto] = []
                groups[usuario][voto].append(propuesta)
        
        return groups  
        
    def loadTable(datos):
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
            loadTable(datos)
            page.dialog = dlg
            dlg.open = True
            page.update()
    
    def createCard(nombre, groups):
        email = "@gmail.com"
        outcome = nombre.replace(email, "").upper() 
        card = ft.Card(
            content=ft.Container(
                width=800,
                content=ft.Column(
                    [
                        ft.ListTile(
                            title=ft.Text(f"Resumen de votaciones del usuario {outcome}", color="white", weight="bold",size=20),
                        ),
                        ft.ListTile(
                            title=ft.Text("Votación Sí", color="white"),
                            trailing=ft.ElevatedButton("Mostrar", bgcolor="#facf25", color = "#043A68", on_click= lambda e :open_dlg(groups.get(nombre, {}).get('Si', None))),
                        ),
                        ft.ListTile(
                            title=ft.Text("Votación No", color="white"),
                            trailing=ft.ElevatedButton("Mostrar", bgcolor="#facf25", color = "#043A68", on_click= lambda f :open_dlg(groups.get(nombre, {}).get('No', None))),
                        ),
                        ft.ListTile(
                            title=ft.Text("Votación Abstención", color="white"),
                            trailing=ft.ElevatedButton("Mostrar", bgcolor="#facf25", color = "#043A68", on_click= lambda g :open_dlg(groups.get(nombre, {}).get('Abstencion', None))),
                        ),
                    ],
                    spacing=0,
                ),
                padding=ft.padding.symmetric(vertical=10),
            ),
            color="#043A68",
        )
        page.update()
        return card
    
    def createOverlay(groups):
        for user in userList:
            cards.append(createCard(user.email, groups))
        
        for card in cards:
            page.add(card)
        loadButton.disabled = True
        page.update()
        
    username = ft.TextField(label="Nombre de usuario", width=300)
    banner = ft.Text("Resultados de las votaciones", weight = "bold", color = ft.colors.WHITE, size = 32)
    homeButton = ft.TextButton("", icon=ft.icons.HOME_ROUNDED, icon_color=ft.colors.WHITE, on_click=handleLogout)
    logoutButton = ft.FilledButton(" ", tooltip = "Cerrar sesión", icon=ft.icons.EXIT_TO_APP_ROUNDED, on_click=handleLogout, style=ft.ButtonStyle( shape = ft.RoundedRectangleBorder(radius=0),  bgcolor = "#043A68", color = ft.colors.RED))
    adminButton = ft.FilledButton(
        " ", tooltip = "Panel de administrador",
        icon = ft.icons.ADMIN_PANEL_SETTINGS_OUTLINED,
        style = ft.ButtonStyle( shape = ft.RoundedRectangleBorder(radius=0), bgcolor = "#043A68", color = ft.colors.WHITE),
        disabled = False,
        on_click = handleAdmin
    )
    header = ft.Container(
        padding = ft.padding.all(10),
        bgcolor="#043A68",
        content = ft.Row(
            [homeButton, banner, adminButton, logoutButton],
            alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
        )    
    )
    
    
    #MODIFICACIONES
    def createMatrix(lista_datos):
        flag = True
        tb.rows.clear()
        data_dict = {}
        # Llenar el diccionario con los votos
        for partido, propuestas in lista_datos:
            for p in propuestas:
                if p['Propuesta'] not in data_dict:
                    data_dict[p['Propuesta']] = {}
                data_dict[p['Propuesta']][partido] = p['Voto']

        # Obtener una lista de todas las propuestas y partidos
        propuestas = sorted(data_dict.keys())
        partidos = sorted(set(partido for partido, _ in lista_datos))

        matrix = []
        header = ['Propuesta'] + partidos
        matrix.append(header)

        # Llenar la matriz con los votos
        for propuesta in propuestas:
            fila = [propuesta]
            for partido in partidos:
                fila.append(data_dict[propuesta].get(partido, 'NA'))
            matrix.append(fila)
        
        agrupaciones = {}
    
        # Agrupar propuestas con resultados idénticos
        for fila in matrix[1:]:  # Omitir el encabezado
            resultados = tuple(fila[1:])  # Convertir resultados a tupla para usar como clave
            propuesta = fila[0]
            if resultados not in agrupaciones:
                agrupaciones[resultados] = []
            agrupaciones[resultados].append(propuesta)

        lv = ft.ListView(spacing=10, padding=20, auto_scroll=True)
        for resultados, propuestas in agrupaciones.items():
            lv.controls.append(ft.Text(f"Propuestas: {propuestas},Votaciones {resultados}: "))
        
        for resultados, propuestas in agrupaciones.items():
            tb.rows.append(
                ft.DataRow(
                    cells = [
                        ft.DataCell(ft.Text(f"{', '.join(propuestas)}", size = 14)),
                        ft.DataCell(ft.Text(f"{', '.join(resultados)}", size = 14)),
                    ]
                )
            )
        
        allButton.disabled = True
        page.add(tb)
        page.update()        
    

    loadButton =  ft.ElevatedButton("Mostrar votaciones usuarios",
        bgcolor="#043A68", color = "white",
        on_click = lambda e :createOverlay(completeOverlay(resultsUserList)))
    
    allButton = ft.ElevatedButton("Mostrar agrupaciones de propuestas",
        bgcolor="#043A68", color = "white",
        on_click = lambda e :createMatrix(resultsUserList))
    
    myPage = ft.Column(
        controls = [
            header,
            ft.Row(
                controls=[
                ft.Column([allButton]),
                ft.Column([loadButton]),
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    
    return {
        "view":myPage,
        "title": title,
        "load": downloadFile()
        }