import flet as ft
import httpx
from components.notifications import show_not_found_notification

class ViewRedirigirLink(ft.View):
    def __init__(self, page: ft.Page):
        
        self.tf_corto = ft.TextField(label="Ingresa el link corto", width=400)
        
        super().__init__(
            route="/consulta",
            controls = [
            ft.AppBar(title=ft.Text("Redirigir Link"), bgcolor=ft.Colors.AMBER),
            ft.Column(
                [
                    self.tf_corto,
                    ft.Button("Ir al Link", on_click=self.redirigir_click),
                    ft.Button("Volver al Inicio", on_click=lambda _: page.go("/"))
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True
            )
            ]
        )
        
        self.main_page = page

    async def redirigir_click(self, e):
        if not self.tf_corto.value:
            return

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"http://127.0.0.1:8000/links/{self.tf_corto.value}")
                if response.status_code == 200:
                    data = response.json()
                    url = data["long_url"]
                    
                    # Asegurar que el URL tenga protocolo para que launch_url no falle
                    if not url.startswith(("http://", "https://")):
                        url = "https://" + url
                    
                    await self.page.launch_url(url)
                    self.page.update()
                else:
                    show_not_found_notification(self.page)
            except Exception as ex:
                print(f"Error en redirección: {ex}")
