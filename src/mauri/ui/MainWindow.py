import threading
import queue
import dearpygui.dearpygui as dpg
import time
import logging
import platform
from pathlib import Path

from mauri.models.dtbs import conn_dtbs
from mauri.models.books import BookRepository
from mauri.parser.parser import Parser
from mauri.utils.logger_ui import logger, log_queue

from mauri.utils.settings import HTML_FILE, FONT_ROBOTO_REGULAR, ICO_FILE, PNG_FILE

from dataclasses import dataclass
from typing import Optional

#setup_logger()
#logger = logging.getLogger(__name__)

WIDTH = 800
HEIGHT = 400
table_queue = queue.Queue() # Для обновления таблицы
logs_buffer = []
dpg.create_context()

class Ui():
    def __init__(self):
        self.a = 1
        pass

@dataclass
class QueryArgs:
    i: Optional[int] = None
    n: Optional[str] = None
    a: Optional[str] = None
    t: Optional[str] = None
    p: Optional[str] = None
    m: Optional[int] = None

def update_table(table_data: list):
    logger.info("Обновление таблицы")

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

def exit(sender):
    dpg.stop_dearpygui()

def output_select_ui(sender, app_data, user_data):
    thread = threading.Thread(target=output_select, args=(user_data,), daemon=True)
    thread.start()

def output_select(args):
    conn = conn_dtbs()
    book = BookRepository()
    rows = book.list_output(conn, args)
    conn.close()
    table_queue.put(rows)

def parser_site(parser):
    logger.info("Начинается парсинг")
    conn = conn_dtbs()
    parser.parse(conn)
    conn.close()

def parser_ui(sender):
    parser = Parser()
    thread = threading.Thread(target=parser_site, args=(parser,), daemon=True)
    thread.start()

def resize_window():
    
    width = dpg.get_viewport_client_width()
    height = dpg.get_viewport_client_height()

    button_height = 50

    content_height = height - button_height - 20

    table_width = int(width * 0.6)
    log_width = int(width * 0.4)

    dpg.configure_item("table_DB", width=table_width, height=content_height)
    dpg.configure_item("text", width=log_width, height=content_height)

def update_ui():
    while not log_queue.empty():
        record = log_queue.get_nowait()
        msg = record.getMessage()
        logs_buffer.append(msg)
        text = "\n".join(logs_buffer[-100:])
        dpg.set_value("line1", text)
    while not table_queue.empty():
        value = table_queue.get_nowait()
        update_table(value)


def run_ui():

    # Назначение шрифта
    with dpg.font_registry():
        with dpg.font(str(FONT_ROBOTO_REGULAR), 18) as default_font:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
        dpg.bind_font(default_font)


    dpg.create_viewport(title='MauriParser', width=WIDTH, height=HEIGHT)

    print(ICO_FILE)
    if(platform.system() == "Windows"):
        dpg.set_viewport_small_icon(str(ICO_FILE))
        dpg.set_viewport_large_icon(str(ICO_FILE))
    else:
        dpg.set_viewport_small_icon(str(PNG_FILE))
        dpg.set_viewport_large_icon(str(PNG_FILE))

    with dpg.window(label="Example") as win:

        with dpg.menu_bar():
            dpg.add_menu_item(label="Exit", callback=exit)
            dpg.add_menu_item(label="Export")
        with dpg.group(horizontal=True):
            
            
            with dpg.table(label="DB", tag="table_DB", width=500, scrollY=True, resizable=True,
                policy=dpg.mvTable_SizingStretchProp):
                dpg.add_table_column(label="id", parent="table_DB", width=5)
                dpg.add_table_column(label="name", parent="table_DB", width=40)
                dpg.add_table_column(label="type", parent="table_DB", width=10)
                dpg.add_table_column(label="author", parent="table_DB", width=40)
                dpg.add_table_column(label="price", parent="table_DB", width=10)
                dpg.add_table_column(label="money", parent="table_DB", width=10)
            dpg.add_child_window(label="Label", tag="text", border=True)
            dpg.add_text("Line", parent="text", tag="line1")
        with dpg.group(horizontal=True):
            args = QueryArgs()
            dpg.add_button(label="Select", callback=output_select_ui, user_data=args)
            dpg.add_button(label="Parse", callback=parser_ui)
        dpg.set_primary_window(win, True)

    dpg.setup_dearpygui()
    dpg.show_viewport()

    while dpg.is_dearpygui_running():
        update_ui()
        resize_window()
        dpg.render_dearpygui_frame()
    #dpg.start_dearpygui()
    dpg.destroy_context()