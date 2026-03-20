import flet as ft
from views.acortar_link import ViewAcortarLink as Acortar
from views.conteo_visitas import ViewConteoVisitas as Conteo
from views.redirigir_link import ViewRedirigirLink as Redirigir

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.title = "Sistema de Registro 2026"
    page.width = 1000
    page.height = 1000

    def route_change(e):
        # Limpiamos las vistas existentes
        page.views.clear()
        
        # --- RUTA INICIO ---
        if page.route == "/":
            page.views.append(
                ft.View(
                    route="/",
                    controls=[
                        ft.Column(
                            [
                                ft.Text("¿Qué desea hacer hoy?", size=30, weight="bold"),
                                ft.Row(
                                    [
                                        ft.Container(
                                            content=ft.Column([
                                                ft.Icon(ft.Icons.EDIT_DOCUMENT, size=50, color=ft.Colors.WHITE),
                                                ft.Text("Acortar Link", size=18, weight="bold", color = ft.Colors.WHITE )
                                            ], alignment="center", horizontal_alignment="center"),
                                            width=280, height=220, bgcolor=ft.Colors.PINK_100,
                                            border_radius=20,
                                            on_click=lambda _: page.go("/captura"),
                                            ink=True, border=ft.Border.all(1, ft.Colors.PINK_100)
                                        ),
                                        ft.Container(
                                            content=ft.Column([
                                                ft.Icon(ft.Icons.SEARCH, size=50, color=ft.Colors.WHITE),
                                                ft.Text("Redirigir Link", size=18, weight="bold" , color = ft.Colors.WHITE)
                                            ], alignment="center", horizontal_alignment="center"),
                                            width=280, height=220, bgcolor=ft.Colors.CYAN_400,
                                            border_radius=20,
                                            on_click=lambda _: page.go("/consulta"),
                                            ink=True, border=ft.Border.all(1, ft.Colors.CYAN_400)
                                        ),
                                        ft.Container(
                                            content=ft.Column([
                                                ft.Icon(ft.Icons.DELETE_SWEEP, size=50, color=ft.Colors.WHITE),
                                                ft.Text("Ver Estadísticas", size=18, weight="bold" , color = ft.Colors.WHITE)
                                            ], alignment="center", horizontal_alignment="center"),
                                            width=280, height=220, bgcolor=ft.Colors.ORANGE_400,
                                            border_radius=20,
                                            on_click=lambda _: page.go("/conteo"),
                                            ink=True, border=ft.Border.all(1, ft.Colors.ORANGE_400)
                                        ),
                                    ],
                                    alignment="center", spacing=40
                                )
                            ],
                            alignment="center", horizontal_alignment="center", expand=True
                        )
                    ]
                )
            )

        # --- RUTA CAPTURA ---
        elif page.route == "/captura":
            page.views.append(Acortar(page))

        # --- RUTA CONSULTA ---
        elif page.route == "/consulta":
            page.views.append(Redirigir(page))
        
        # --- RUTA BORRADO ---
        elif page.route == "/conteo":
            page.views.append(Conteo(page))
        
        page.update()

    def view_pop(e):
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)

    # 1. Definimos los manejadores
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    # 2. Forzamos la carga inicial
    page.route = "/" 
    route_change(None) 

if __name__ == "__main__":
    ft.run(main)
