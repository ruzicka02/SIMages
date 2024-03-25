from nicegui import ui

source = "IMG20230803112016.jpg"
close = ["IMG20230803112019.jpg", "IMG20230802131959.jpg", "IMG20230803112010.jpg", "IMG20230724132147.jpg", "IMG20230803112008.jpg"]

def open_dialog(url: str):
     dialog_image_ui.set_source(url)
     dialog.open()
with ui.dialog() as dialog:
     dialog_image_ui = ui.image().style("max-width: none")

ui.label('Image similarity prototype').style('font-size: 4em; font-weight: 300')  # color: #6E93D6;
# ui.image('data/IMG20230803112016.jpg').classes('w-256')

# source image
ui.image('data/' + source).style('width: 80%; margin: auto')

# similar images
# https://www.w3schools.com/howto/howto_js_image_grid.asp
ui.label('You may also like:').style('font-size: 1.5em; font-weight: 300; margin-left: 10%')
with ui.row().style('display: flex; flex-wrap: wrap; padding: 0 4px; margin: auto'):
    for i in close:
        # ui.button("Image 1") ui.button("Image 2", on_click=lambda: open_dialog(image_url_2))
        with ui.button(on_click=lambda: open_dialog('data/' + i)).style('margin: 0px'):
            ui.image('data/' + i).style('flex: 18%; width: 256px; vertical-align: middle')


ui.run()
