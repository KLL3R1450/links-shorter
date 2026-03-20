import flet as ft
import httpx

class CapturaView(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.tf_original = ft.TextField(label="Ingresa el link original", width=400)
        self.tf_acortado = ft.TextField(label="Link acortado", width=400, read_only=True)
        
        self.controls = [
            ft.Text("Acortar Nuevo Link", size=25, weight="bold"),
            self.tf_original,
            ft.ElevatedButton("Acortar Link", on_click=self.acortar_click),
            self.tf_acortado,
            ft.ElevatedButton("Volver al Inicio", on_click=lambda _: page.go("/"))
        ]
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.alignment = ft.MainAxisAlignment.CENTER

    async def acortar_click(self, e):
        if not self.tf_original.value:
            return

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    "http://127.0.0.1:8000/links/crear", 
                    json={"long_url": self.tf_original.value}
                )
                if response.status_code == 200:
                    data = response.json()
                    self.tf_acortado.value = data["short_id"]
                    self.page.update()
            except Exception as ex:
                print(f"Error: {ex}")
