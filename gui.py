from nicegui import ui
from pathlib import Path
from copy import deepcopy

source = "IMG20230803112016.jpg"
close = ["IMG20230803112019.jpg", "IMG20230802131959.jpg", "IMG20230803112010.jpg", "IMG20230724132147.jpg", "IMG20230803112008.jpg"]

def draw_gui(source_img: Path, close_img: list[tuple[Path, float]]):
     dialog_image_ui = None

     def open_dialog(url: str):
          print("Dialog:", url)
          dialog_image_ui.set_source(url)
          dialog.open()


     with ui.dialog() as dialog:
          dialog_image_ui = ui.image().style("width: 100%; height: auto")

     ui.label('Image similarity prototype').style('font-size: 4em; font-weight: 300')  # color: #6E93D6;
     # ui.image('data/IMG20230803112016.jpg').classes('w-256')

     # source image
     ui.image(source_img).style('width: 80%; margin: auto')

     # similar images
     # https://www.w3schools.com/howto/howto_js_image_grid.asp
     ui.label('You may also like:').style('font-size: 1.5em; font-weight: 300; margin-left: 10%')
     with ui.row().style('display: flex; flex-wrap: wrap; justify-content: space-evenly; padding: 0 4px; margin: auto'):
          for img, similarity in close_img:
               # ui.button("Image 1") ui.button("Image 2", on_click=lambda: open_dialog(image_url_2))
               with ui.column():
                    ui.label(f"{similarity:7.3f} % similarity")
                    with ui.button(on_click=lambda local_img=img: open_dialog(local_img)).style('margin: 0px'):
                         print("Draw:", img)
                         ui.image(img).style('width: 15vw; vertical-align: middle')
