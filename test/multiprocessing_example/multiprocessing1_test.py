import threading
import queue
import dearpygui.dearpygui as dpg
import time


WIDTH = 600
HEIGHT = 300


queue = queue.Queue()

def test_mult(sender, app_data, data):
    print(f"{data}")

def add(data: tuple):
    a: int = 0
    string = ""
    while(a < data[0] + data[1]):
        a += 1
        time.sleep(1)
        string+=f"[INFO]: {a}\n"
        queue.put(string)
        print(f"Test a: {a}")

def add_ui(sender, app_data, data: tuple):
    thread = threading.Thread(target = add, args=(data,), daemon=True)
    thread.start()

dpg.create_context()
dpg.create_viewport(title='MauriParser', width=WIDTH, height=HEIGHT)

with dpg.window(label="Example") as win:
    with dpg.menu_bar():
        dpg.add_menu_item(label="Exit")
        dpg.add_menu_item(label="Export")
    with dpg.group(horizontal=True, height=250):
        with dpg.table(label="DB", tag="table_DB", width=200):
            dpg.add_table_column(label="id", parent="table_DB", width=10)
            dpg.add_table_column(label="name", parent="table_DB", width=10)
        dpg.add_child_window(label="Label", tag="text")
        dpg.add_text("Line", parent="text", tag="line1")
    with dpg.group(horizontal=True):
        dpg.add_button(label="Add", callback=add_ui, user_data=(20, 1))
        dpg.add_button(label="Click", callback=test_mult, user_data="Hello")
    dpg.set_primary_window(win, True)



def update_ui():
    while not queue.empty():
        value = queue.get_nowait()
        dpg.set_value("line1", value)

dpg.setup_dearpygui()
dpg.show_viewport()

while dpg.is_dearpygui_running():
    update_ui()
    dpg.render_dearpygui_frame()
dpg.start_dearpygui()
dpg.destroy_context()