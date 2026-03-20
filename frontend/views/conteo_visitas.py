import flet as ft
import httpx
from components.notifications import show_not_found_notification

class ViewConteoVisitas(ft.View):
    def __init__(self, page: ft.Page):
        
        
        self.tf_corto = ft.TextField(label="Ingresa el link corto", width=400)
        self.tf_conteo = ft.TextField(label="Conteo de visitas", width=400, read_only=True)
        self.tf_original = ft.TextField(label="Link original", width=400, read_only=True)
        
        super().__init__(
            route = "/conteo",
            controls=[
                ft.AppBar(title=ft.Text("Conteo de Visitas"), bgcolor=ft.Colors.AMBER),
                ft.Column(
                    [
                        self.tf_corto,
                        ft.ElevatedButton("Ver Conteo", on_click=self.conteo_click),
                        self.tf_conteo,
                        self.tf_original,
                        ft.ElevatedButton("Volver al Inicio", on_click=lambda _: page.go("/"))
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    expand=True
                )
            ]
        )
        
        self.main_page = page
        


    async def conteo_click(self, e):
        if not self.tf_corto.value:
            return

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"http://127.0.0.1:8000/links/conteo/{self.tf_corto.value}")
                if response.status_code == 200:
                    data = response.json()
                    self.tf_conteo.value = str(data["visits"])
                    self.tf_original.value = data["long_url"]
                    self.page.update()
                else:
                    self.tf_conteo.value = ""
                    self.tf_original.value = ""
                    show_not_found_notification(self.page)
            except Exception as ex:
                print(f"Error al conectar con el backend: {ex}")