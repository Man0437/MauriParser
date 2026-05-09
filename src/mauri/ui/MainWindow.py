import threading
import queue
import dearpygui.dearpygui as dpg
import time
import logging

from mauri.models.dtbs import conn_dtbs
from mauri.models.books import BookRepository
from mauri.parser.parser import Parser

from mauri.utils.settings import HTML_FILE

from dataclasses import dataclass
from typing import Optional

WIDTH = 800
HEIGHT = 400

add_queue = queue.Queue() # Для обновления add(Можно удалять)
table_queue = queue.Queue() # Для обновления таблицы
logging_queue = queue.Queue() # Для логгов (Добавим позже)

@dataclass
class QueryArgs:
    i: Optional[int] = None
    n: Optional[str] = None
    a: Optional[str] = None
    t: Optional[str] = None
    p: Optional[str] = None
    m: Optional[int] = None

def test_mult(sender, app_data, win):
    print(f"{dpg.get_item_rect_size(win)}")

def update_table(table_data: list):

    table = dpg.get_item_children("table_DB", 1)
    row_count = len(table_data)

    if table:
        for t in table:
            dpg.delete_item(t)

    for row in table_data:
        print(row)
        with dpg.table_row(parent="table_DB"):
            for value in row:
                dpg.add_text(str(value))

def add(data: tuple):
    a: int = 0
    string = ""
    while(a < data[0] + data[1]):
        a += 1
        time.sleep(1)
        string+=f"[INFO]: {a}\n"
        add_queue.put(string)
        print(f"Test a: {a}")

def add_ui(sender, app_data, data: tuple):
    thread = threading.Thread(target = add, args=(data,), daemon=True)
    thread.start()
## Логирование
def output_logging():
    pass

def output_logging_ui():
    pass
##
def output_select_ui(sender, app_data, user_data):
    thread = threading.Thread(target=output_select, args=(user_data,), daemon=True)
    thread.start()

def output_select(args):
    conn = conn_dtbs()
    book = BookRepository()
    rows = book.list_output(conn, args)
    conn.close()
    table_queue.put(rows)
    print(f"Выполнено {len(rows)}")

def parser_site(parser):
    conn = conn_dtbs()
    parser.parse(conn)
    conn.close()

def parser_ui(sender):
    parser = Parser()
    thread = threading.Thread(target=parser_site, args=(parser,), daemon=True)
    thread.start()

def resize_window(sender, app_data, win):
    size = dpg.get_item_rect_size(win)
dpg.create_context()
dpg.create_viewport(title='MauriParser', width=WIDTH, height=HEIGHT)

with dpg.window(label="Example") as win:
    with dpg.menu_bar():
        dpg.add_menu_item(label="Exit")
        dpg.add_menu_item(label="Export")
    with dpg.group(horizontal=True, height=330):
        with dpg.table(label="DB", tag="table_DB", width=500, scrollY=True):
            dpg.add_table_column(label="id", parent="table_DB", width=5)
            dpg.add_table_column(label="name", parent="table_DB", width=40)
            dpg.add_table_column(label="type", parent="table_DB", width=10)
            dpg.add_table_column(label="author", parent="table_DB", width=40)
            dpg.add_table_column(label="price", parent="table_DB", width=10)
            dpg.add_table_column(label="money", parent="table_DB", width=10)
        dpg.add_child_window(label="Label", tag="text")
        dpg.add_text("Line", parent="text", tag="line1")
    with dpg.group(horizontal=True):
        dpg.add_button(label="Add", callback=add_ui, user_data=(20, 1))
        dpg.add_button(label="Click", callback=test_mult, user_data=win)

        args = QueryArgs()
        print(HTML_FILE)
        dpg.add_button(label="Select", callback=output_select_ui, user_data=args)
        dpg.add_button(label="Parse", callback=parser_ui)
    dpg.set_primary_window(win, True)

def update_ui():
    while not add_queue.empty():
        value = add_queue.get_nowait()
        dpg.set_value("line1", value)
    while not table_queue.empty():
        value = table_queue.get_nowait()
        update_table(value)

dpg.setup_dearpygui()
dpg.show_viewport()

while dpg.is_dearpygui_running():
    update_ui()
    dpg.render_dearpygui_frame()
dpg.start_dearpygui()
dpg.destroy_context()