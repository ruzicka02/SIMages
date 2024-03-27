from nicegui import ui
from pathlib import Path
from random import shuffle
import os

draw_imgs = []
all_imgs = []
imgs_visible = 0

@ui.page("/")
def draw_selection():
    os.chdir(Path(__file__).parent)
    print("CWD", os.getcwd())

    subdirs = []
    for path in Path("data").iterdir():
        if path.is_dir():
            subdirs.append(path)

    @ui.refreshable
    def image_preview():
        print("Image preview:", draw_imgs)
        print(f"{imgs_visible} visible")
        with ui.row().style('display: flex; flex-wrap: wrap; justify-content: left; padding: 0 4px; margin: auto'):
            for img in draw_imgs:
                with ui.column():
                    ui.label(img.name)
                    with ui.button(on_click=lambda local_img=img: ui.notify(local_img)).style('padding: 0px'):
                        print("Draw:", img)
                        ui.image(img).style('width: 18vw; vertical-align: middle')

    def select_dir(toggle: ui.toggle):
        global all_imgs
        global draw_imgs
        global imgs_visible
        print("Toggle:", toggle.value)
        with open(toggle.value / "img_order.txt", "r") as f:
            new_imgs = [toggle.value / Path(x) for x in f.read().split()]
            shuffle(new_imgs)
            all_imgs = new_imgs

        imgs_visible = 10
        draw_imgs = all_imgs[:imgs_visible]
        print(draw_imgs)
        image_preview.refresh()

    def more_photos():
        global imgs_visible
        prev = imgs_visible
        imgs_visible += 10
        draw_imgs.extend(all_imgs[prev:imgs_visible])
        image_preview.refresh()


    ui.label('SIMages - selection').style('font-size: 4em; font-weight: 300')  # color: #6E93D6;

    # select_dir(dir_toggle, all_imgs, draw_imgs)
    dir_toggle = ui.toggle({x: str(x) for x in subdirs}, on_change=lambda: select_dir(dir_toggle))

    image_preview()

    ui.button("More photos", on_click=more_photos)


@ui.page("/similar")
def draw_similar(source_img: Path, close_img: list[tuple[Path, float]]):
    dialog_image_ui = None

    def open_dialog(url: str):
        print("Dialog:", url)
        dialog_image_ui.set_source(url)
        dialog.open()


    with ui.dialog() as dialog:
        dialog_image_ui = ui.image().style("width: 100%; height: auto")

    ui.label('SIMages - preview').style('font-size: 4em; font-weight: 300')  # color: #6E93D6;
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
                with ui.button(on_click=lambda local_img=img: open_dialog(local_img)).style('padding: 0px'):
                    print("Draw:", img)
                    ui.image(img).style('width: 15vw; vertical-align: middle')
