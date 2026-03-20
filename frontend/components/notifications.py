import flet as ft

def show_not_found_notification(page: ft.Page):
    def go_to_acortar(e):
        page.go("/acortar")
        page.update()

    snack_bar = ft.SnackBar(
        content=ft.Text("NO SE ENCONTRO REGISTRO PARA ESTE LINK. ¿DESEAS AÑADIR UNO?"),
        bgcolor=ft.Colors.RED,
        duration=2000, 
        behavior= "FLOATING", 
        width= 300,
        action = "agregar",
        on_action=lambda _: go_to_acortar(None),
        shape = ft.RoundedRectangleBorder(radius=20)
    )
    
    page.show_dialog(snack_bar)
    page.update()
