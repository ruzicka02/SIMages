from nicegui import ui
from pathlib import Path
from random import shuffle
import os

from utils import list_subdirs

draw_imgs = []
all_imgs = []
imgs_visible = 0
join_on = None

@ui.refreshable
def image_preview():
    # print("Image preview:", draw_imgs)
    print(f"{imgs_visible} visible")
    with ui.row().style('display: flex; flex-wrap: wrap; justify-content: left; padding: 0 4px; margin: auto'):
        for img in draw_imgs:
            with ui.button(on_click=lambda local_img=img: ui.navigate.to(f"/similar?source_img={local_img}{f"&join_on={join_on}" if join_on else ""}")).style('padding: 0px'):
                with ui.card().tight():
                    # print("Draw:", img)
                    ui.image(img).style('width: 18vw; vertical-align: middle')
                    with ui.card_section():
                        ui.label(img.name).style("color: #15141A")


def select_dir(toggle: ui.toggle, switch_shuffle: ui.switch):
    # print(switch_shuffle.value)

    global all_imgs
    global draw_imgs
    global imgs_visible
    print("Toggle:", toggle.value)
    with open(toggle.value / "img_order.txt", "r") as f:
        new_imgs = [toggle.value / Path(x) for x in f.read().split()]
        if switch_shuffle.value:
            shuffle(new_imgs)
        all_imgs = new_imgs

    imgs_visible = 10
    draw_imgs = all_imgs[:imgs_visible]
    # print(draw_imgs)
    image_preview.refresh()

def select_join(toggle: ui.toggle):
    print("Join toggle:", toggle.value)
    global join_on
    join_on = toggle.value

def more_photos():
    global imgs_visible
    prev = imgs_visible
    imgs_visible += 10
    draw_imgs.extend(all_imgs[prev:imgs_visible])
    image_preview.refresh()

@ui.page("/")
def key_select():
    subdirs = list_subdirs()

    with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
        ui.label('SIMages - key image selection').style('font-size: 3em; font-weight: 300')  # color: #6E93D6;

    ui.label('Key image directory:')
    with ui.row():
        dir_toggle = ui.toggle({x: x.name for x in subdirs}, value=subdirs[0], on_change=lambda: select_dir(dir_toggle, dir_shuffle))
        dir_shuffle = ui.switch("Shuffle", on_change=lambda: select_dir(dir_toggle, dir_shuffle))
    select_dir(dir_toggle, dir_shuffle)

    ui.label('Join on:')
    join_toggle = ui.toggle({x: x.name for x in subdirs}, value=subdirs[0], on_change=lambda: select_join(join_toggle))
    select_join(join_toggle)

    image_preview()

    ui.button("More photos", on_click=more_photos)