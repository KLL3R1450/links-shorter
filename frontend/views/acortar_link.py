import flet as ft
import httpx

class ViewAcortarLink(ft.View):
    def __init__(self, page: ft.Page):
            # 1. Definimos los componentes que necesitan ser accedidos por otros métodos
        self.tf_original = ft.TextField(label="Ingresa el link original", width=400)
        self.tf_acortado = ft.TextField(label="Link acortado", width=400, read_only=True)
        
        # 2. Llamamos al constructor padre sin asignar self.page manualmente
        
        super().__init__(
            route="/acortar",
            controls=[
                ft.AppBar(title=ft.Text("Acortar Link"), bgcolor=ft.Colors.AMBER),
                ft.Column(
                    [
                        self.tf_original,
                        ft.ElevatedButton("Acortar Link", on_click=self.acortar_click),
                        self.tf_acortado,
                        # Usamos push_route en lugar de go()
                        ft.ElevatedButton("Volver al Inicio", on_click=lambda _: self.main_page.go("/"))
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    expand=True
                )
            ]
        )
        
        self.main_page = page
        
        

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
                    # self.page ya existe por herencia de ft.View
                    self.page.update()
            except Exception as ex:
                print(f"Error al conectar con el backend: {ex}")