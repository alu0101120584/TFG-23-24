import flet as ft

def IndexView(page, myPyrebase=None):
    title = "App TFG Parlamento"

    def handleSignInError():
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Credenciales incorrectos. Por favor inténtalo de nuevo.", color=ft.colors.WHITE),
            bgcolor=ft.colors.RED
        )
        page.snack_bar.open = True
        page.update()

    def handleSignIn(e):
        try:
            myPyrebase.sign_in(email.value, password.value)
            password.value = ""
            if (email.value == "admin@gmail.com"):
                page.go("/adminView")
            else:
                page.go("/userView")
            
        except:
            handleSignInError()
            page.update()
        
    def handleAdmin(e):
        page.go('/adminView')
        
    email = ft.TextField(label="Email", bgcolor = ft.colors.WHITE, width=300, height=40)
    password = ft.TextField(label="Contraseña", bgcolor = ft.colors.WHITE, width=300, height=40, password=True)
    
    logInButton = ft.Container(
        alignment = ft.alignment.center,
        height=40,
        bgcolor="#043A68",
        width=300,
        content=ft.Text(
            "Acceder", 
            color="white",
            size=16,
            ),
        on_click= handleAdmin
    )
   
    myPage = ft.Row(
        controls = [
            ft.Container(
                content = ft.Column(
                    [
                        ft.Container(
                            ft.Text(
                                "Identificación de ususario",
                                size=32,
                                weight=ft.FontWeight.BOLD,
                            ), 
                            alignment=ft.alignment.center,
                            padding = ft.padding.only(top=40),
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
                            [logInButton],
                            alignment=ft.MainAxisAlignment.CENTER),
                    ],
                    spacing = 40,
                ),
                bgcolor = "#facf25", 
                border = ft.border.all(2, "#043A68"),
                height = 420,
                width = 500,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER
    )
    
    return {
        "view":myPage,
        "title": title,
        }