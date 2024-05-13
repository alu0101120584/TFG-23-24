import flet as ft

def ResultsView(page, myPyrebase):
    
    def handle_admin(e):
        page.go('/adminView')
        
    def handle_logout(*e):
        username.value = ""
        myPyrebase.kill_all_streams()
        myPyrebase.sign_out()
        page.go("/")
        
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
    
    table=ft.DataTable(
        expand = 1,
        border=ft.border.all(2, "#043A68"),
        show_bottom_border=True,
        columns=[
                ft.DataColumn(ft.Text("Propuesta")),
                ft.DataColumn(ft.Text("Fecha")),
                ft.DataColumn(ft.Text("Decisión")),
            ],
    )
    
    #Modificar para leer del fichero .json que se encuentra almacenado en firebase y mostrarlo aquí
    for i in range (1, 30):
        table.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("Propuesta número 1")),
                    ft.DataCell(ft.Text("03/05/2024")),
                    ft.DataCell(ft.Text("Abstención")),
                ]
            )
        )
    
    lv = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
    lv.controls.append(table)
    
    myPage = ft.Column(
        [navbar, lv]
    )
    
    return {
        "view":myPage,
        "title": "UserView",
        }