from nicegui import ui
from pathlib import Path
from random import shuffle
import os

from utils import list_subdirs

draw_imgs = []
all_imgs = []
imgs_visible = 0
join_on = None
metric = None
query_type = None
limit = None

def get_url(img: str) -> str:
    url = f"/similar?source_img={img}"
    if join_on:
        url += f"&join_on={join_on}"
    if metric:
        url += f"&m={metric}"
    if query_type:
        url += f"&q={query_type}"
    if limit:
        url += f"&limit={limit}"
    return url

@ui.refreshable
def image_preview():
    # print("Image preview:", draw_imgs)
    print(f"{imgs_visible} visible")
    with ui.row().style('display: flex; flex-wrap: wrap; justify-content: left; padding: 0 4px; margin: auto'):
        for img in draw_imgs:
            with ui.button(on_click=lambda local_img=img: ui.navigate.to(get_url(local_img))).style('padding: 0px'):
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

def select_metric(toggle: ui.radio):
    print("Metric:", toggle.value)
    global metric
    metric = toggle.value

def select_query(toggle: ui.radio, knn: ui.input, range: ui.input):
    print("Query type:", toggle.value)
    global query_type
    query_type = toggle.value

    if query_type == "knn":
        select_limit(knn)
        knn.visible = True
        range.visible = False
    elif query_type == "range":
        select_limit(range)
        knn.visible = False
        range.visible = True

def select_limit(input: ui.input):
    print("New limit:", input.value)
    global limit
    limit = input.value

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
    with ui.row():
        join_toggle = ui.toggle({x: x.name for x in subdirs}, value=subdirs[0], on_change=lambda: select_join(join_toggle))
        ui.space().style("width: 10vw")

        metric_toggle = ui.radio({"cos": "Cosine similarity", "euclid": "Euclidean distance"}, value="cos",
                                 on_change=lambda: select_metric(metric_toggle))
        query_toggle = ui.radio({"knn": "kNN query", "range": "Range query"}, value="knn",
                                on_change=lambda: select_query(query_toggle, knn_input, range_input))
        knn_input = ui.input(label="# Nearest neighbors (k)", value="10", on_change=lambda: select_limit(knn_input))
        range_input = ui.input(label="Range limit", value="0.3", on_change=lambda: select_limit(range_input))

    select_join(join_toggle)
    select_metric(metric_toggle)
    select_query(query_toggle, knn_input, range_input)

    image_preview()

    ui.button("More photos", on_click=more_photos)