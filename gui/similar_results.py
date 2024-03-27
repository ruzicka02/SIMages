import nearest

from nicegui import ui
from pathlib import Path

@ui.page("/similar")
def similar_results(source_img: str, join_on: str = None):
    source_img = Path(source_img)
    if join_on:
        join_on = Path(join_on)

    close_img: list[tuple[Path, float]] = nearest.knn_query(source_img, 10, join_on, verbose=True)

    dialog_image_ui = None

    def open_dialog(url: str):
        print("Dialog:", url)
        dialog_image_ui.set_source(url)
        dialog.open()


    with ui.dialog() as dialog:
        dialog_image_ui = ui.image().style("width: 100%; height: auto")

    with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
        ui.label('SIMages - Similar results').style('font-size: 4em; font-weight: 300')  # color: #6E93D6;
        ui.button(icon='home', on_click=lambda: ui.navigate.to('/'))
    # ui.image('data/IMG20230803112016.jpg').classes('w-256')

    # source image
    ui.image(source_img).style('width: 80%; margin: auto')

    # similar images
    # https://www.w3schools.com/howto/howto_js_image_grid.asp
    ui.label('You may also like:').style('font-size: 1.5em; font-weight: 300; margin-left: 10%')
    with ui.row().style('display: flex; flex-wrap: wrap; justify-content: space-evenly; padding: 0 4px; margin: auto'):
        for img, similarity in close_img:
            # ui.button("Image 1") ui.button("Image 2", on_click=lambda: open_dialog(image_url_2))
            with ui.button(on_click=lambda local_img=img: open_dialog(local_img)).style('padding: 0px'):
                with ui.card().tight():
                # print("Draw:", img)
                    ui.image(img).style('width: 18vw; vertical-align: middle')
                    with ui.card_section():
                        ui.label(f"{similarity:7.3f} % similarity").style("color: #15141A")
