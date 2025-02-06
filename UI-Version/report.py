import flet as ft
#alright, after multiple interactions GPT helped a lot with this

class SimpleReportApp:
    def __init__(self):
        pass

    def start(self, info_str: str, long_text: str):
        # This function parses the info string (e.g., "Distractions=3, Stress=75%, Focus=30")
        def parse_info(s):
            data = {}
            parts = s.split(",")
            for p in parts:
                key_val = p.strip().split("=")
                if len(key_val) == 2:
                    key = key_val[0].lower()
                    val = key_val[1]
                    if "distractions" in key:
                        data["distractions"] = int(val)
                    elif "stress" in key:
                        data["stress"] = int(val.replace("%", "")) 
                    elif "focus" in key:
                        data["focus"] = int(val)
            return data

        # This is the main function Flet will call
        def main(page: ft.Page):
            page.title = "Report: Studdy Buddy"
            page.window.full_screen = True
            page.update()
            # Parse the string
            data = parse_info(info_str)

            # Add text elements
            page.add(
                ft.Text("Report: Study Buddy", size=30, weight=ft.FontWeight.BOLD),
                ft.Text(f"Number of Distractions: {data.get('distractions', 'N/A')}", weight=ft.FontWeight.BOLD),
                ft.Text(f"Stress Level: {data.get('stress', 'N/A')}%", weight=ft.FontWeight.BOLD),
                ft.Text(f"Focus Level %: {data.get('focus', 'N/A')}", weight=ft.FontWeight.BOLD),
            )

            # Add a simple bar chart
            page.add(
                ft.BarChart(
                    bar_groups=[
                        ft.BarChartGroup(
                            x=0,
                            bar_rods=[
                                ft.BarChartRod(
                                    from_y=0,
                                    to_y=data.get("distractions", 0),
                                    width=40,
                                    color=ft.colors.AMBER,
                                    tooltip="Distractions"
                                )
                            ],
                        ),
                        ft.BarChartGroup(
                            x=1,
                            bar_rods=[
                                ft.BarChartRod(
                                    from_y=0,
                                    to_y=data.get("stress", 0),
                                    width=40,
                                    color=ft.colors.BLUE,
                                    tooltip="Stress"
                                )
                            ],
                        ),
                        ft.BarChartGroup(
                            x=2,
                            bar_rods=[
                                ft.BarChartRod(
                                    from_y=0,
                                    to_y=data.get("focus", 0),
                                    width=40,
                                    color=ft.colors.RED,
                                    tooltip="Focus"
                                )
                            ],
                        ),
                    ],
                    bottom_axis=ft.ChartAxis(
                        labels=[
                            ft.ChartAxisLabel(value=0, label=ft.Text("Distractions")),
                            ft.ChartAxisLabel(value=1, label=ft.Text("Stress")),
                            ft.ChartAxisLabel(value=2, label=ft.Text("Focus")),
                        ]
                    ),
                    min_y=0,
                    max_y=100
                )
            )
            # Add a long text area below the graph
            page.add(
                ft.Container(
                    content=ft.Text(long_text, size=16),
                    margin=ft.margin.only(top=20),
                    padding=10,
                    bgcolor=ft.colors.BLUE_50,
                    border_radius=ft.border_radius.all(10),
                )
            )
            page.update()

        # Launch the Flet app
        ft.app(target=main)


''' Example usage:
app = SimpleReportApp()
app.start("Distractions=3, Stress=75%, Focus=30", "something long")
'''