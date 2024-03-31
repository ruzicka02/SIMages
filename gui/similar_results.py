import nearest

from nicegui import ui, events
from pathlib import Path

close_img: list[tuple[Path, float]] = []

dialog = None
dialog_image_ui = None

def calculate_similar(source_img, join_on):
    print("calculating...")
    global close_img
    if _q == "knn":
        close_img = nearest.knn_query(source_img, _m, int(_limit), join_on, verbose=True)
    elif _q == "range":
        close_img = nearest.range_query(source_img, _m, float(_limit), join_on, verbose=True)

    image_preview.refresh()

# https://github.com/zauberzeug/nicegui/blob/main/examples/lightbox/main.py
def handle_key(event_args: events.KeyEventArguments) -> None:
        if not event_args.action.keydown:
            return
        # if event_args.key.escape:
        #     dialog.close()
        # image_index = close_img.index(dialog_image_ui)
        # if event_args.key.arrow_left and image_index > 0:
        #     self._open(self.image_list[image_index - 1])
        # if event_args.key.arrow_right and image_index < len(self.image_list) - 1:
        #     self._open(self.image_list[image_index + 1])
        dialog.close()

def open_dialog(url: str):
    print("Dialog:", url)
    dialog_image_ui.set_source(url)
    dialog.open()

@ui.refreshable
def image_preview():
    global close_img
    images_not_displayed = 0
    ui.label('You may also like:').style('font-size: 1.5em; font-weight: 300; margin-left: 10%')
    with ui.row().style('display: flex; flex-wrap: wrap; justify-content: left; padding: 0 2%; margin: auto'):
        img_max_display = 30
        if len(close_img) > img_max_display:
            images_not_displayed = len(close_img) - img_max_display
            close_img = close_img[:img_max_display]
        for img, metric in close_img:
            # ui.button("Image 1") ui.button("Image 2", on_click=lambda: open_dialog(image_url_2))
            with ui.button(on_click=lambda local_img=img: open_dialog(local_img)).style('padding: 0px'):
                with ui.card().tight():
                # print("Draw:", img)
                    ui.image(img).style('width: 18vw; vertical-align: middle')
                    with ui.card_section():
                        label = f"{metric:7.3f} % similarity" if _m == "cos" else f"distance {int(metric)}"
                        ui.label(label).style("color: #15141A")
    if images_not_displayed > 0:
        ui.label(f'{images_not_displayed} images not displayed').style('font-size: 1.5em; font-weight: 300; margin-left: 10%')


# === settings ===
_m: str = None
_q: str = None
_limit: str = None

def select_metric(toggle: ui.radio, range_input: ui.input):
    print("Metric:", toggle.value)
    global _m
    _m = toggle.value

    # range values for metrics differ significantly... override
    range_input.value = "0.3" if _m == "cos" else "1000"

def select_query(toggle: ui.radio, knn: ui.input, range: ui.input):
    print("Query type:", toggle.value)
    global _q
    _q = toggle.value

    if _q == "knn":
        select_limit(knn)
        knn.visible = True
        range.visible = False
    elif _q == "range":
        select_limit(range)
        knn.visible = False
        range.visible = True

def select_limit(input: ui.input):
    print("New limit:", input.value)
    global _limit
    _limit = input.value


@ui.page("/similar")
def similar_results(source_img: str, join_on: str = None, m: str = None, q: str = None, limit: str = None):
    source_img = Path(source_img)
    if join_on:
        join_on = Path(join_on)

    global _m
    global _q
    global _limit
    _m = m if m else "cos"
    _q = q if q else "knn"
    _limit = limit
    if not limit:
        _limit = 10 if _q == "knn" else 0.3

    calculate_similar(source_img, join_on)

    global dialog
    global dialog_image_ui
    with ui.dialog().props('maximized') as dialog:
        # ui.keyboard(handle_key)
        dialog_image_ui = ui.image().props('fit=scale-down').on('click', lambda: dialog.close())

    with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center'):
        ui.label('SIMages - Similar results').style('font-size: 3em; font-weight: 300')  # color: #6E93D6;
        ui.space()
        with ui.button(icon="menu"):
            with ui.menu() as menu:
                with ui.row():
                    metric_toggle = ui.radio({"cos": "Cosine similarity", "euclid": "Euclidean distance"}, value=_m,
                                            on_change=lambda: select_metric(metric_toggle, range_input))
                    query_toggle = ui.radio({"knn": "kNN query", "range": "Range query"}, value=_q,
                                            on_change=lambda: select_query(query_toggle, knn_input, range_input))
                    knn_input = ui.input(label="# Nearest neighbors (k)", value=_limit if _q == "knn" else 10, on_change=lambda: select_limit(knn_input))
                    range_input = ui.input(label="Range limit", value=_limit if _q == "range" else 0.3, on_change=lambda: select_limit(range_input))
                ui.button("Refresh", on_click=lambda: calculate_similar(source_img, join_on)).style("margin: 10px")
        ui.button(icon='home', on_click=lambda: ui.navigate.to('/'))
    select_query(query_toggle, knn_input, range_input)
    # ui.image('data/IMG20230803112016.jpg').classes('w-256')

    # source image
    ui.image(source_img).style('width: 80%; margin: auto')

    # similar images
    # https://www.w3schools.com/howto/howto_js_image_grid.asp
    image_preview()