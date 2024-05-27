import flet as ft

class YouAlert(ft.UserControl):
    def __init__(self,mydata,mytable):
        super().__init__()
        self.mydata = mydata
        self.mytable = mytable

        self.mytable.rows.clear()
        for x in self.mydata:
            self.mytable.rows.append(
                ft.DataRow(
                    selected = True,
                    cells = [
                        ft.DataCell(ft.Text(x['Propuesta'])),
                    ]
                )
            )
 
    def OpenYouAlert(self):
        res = ft.AlertDialog(
            content=ft.Column([self.mytable],
                scroll=ft.ScrollMode.ALWAYS,
            )
        )
        return res
 
    def showdetails(self,e):
        open_alert = self.OpenYouAlert()
        self.page.dialog = open_alert
        open_alert.open = True
        self.page.update()
 
    def build(self):
        return ft.Column(
            [
                ft.Text("Mostrar las propuestas que se someterán a votación",size=16,color = "#043A68",weight= ft.FontWeight.BOLD),
                ft.FilledButton(
                    "Visualizar",
                    style=ft.ButtonStyle( shape = ft.RoundedRectangleBorder(radius=0), bgcolor = "#043A68", color = "white",),
                    icon=ft.icons.PREVIEW,
                    disabled=False,
                    height=40,
                    width=300,
                    on_click=self.showdetails
                ),        
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )