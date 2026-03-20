import flet as ft
import httpx
from components.notifications import show_not_found_notification

class ConsultaView(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.tf_corto = ft.TextField(label="Ingresa el link corto", width=400)
        
        self.controls = [
            ft.Text("Redirigir Link", size=25, weight="bold"),
            self.tf_corto,
            ft.ElevatedButton("Ir al Link Original", on_click=self.redirigir_click),
            ft.ElevatedButton("Volver al Inicio", on_click=lambda _: page.go("/"))
        ]
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.alignment = ft.MainAxisAlignment.CENTER

    async def redirigir_click(self, e):
        if not self.tf_corto.value:
            return

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"http://127.0.0.1:8000/links/{self.tf_corto.value}")
                if response.status_code == 200:
                    data = response.json()
                    await self.page.launch_url_async(data["long_url"])
                else:
                    show_not_found_notification(self.page)
            except Exception as ex:
                print(f"Error: {ex}")
