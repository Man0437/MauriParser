import dearpygui.dearpygui as dpg
import multiprocessing

dpg.create_context()
dpg.create_viewport(title='MauriParser', width=600, height=300)

with dpg.window(label="Example") as win:
    with dpg.menu_bar() as menu:
        dpg.menu(label="Выход")
        dpg.menu(label="Экспорт базы данных")
        dpg.menu(label="Настройки")
    with dpg.group(horizontal=True) as g1:
        with dpg.table():
            dpg.add_table_row()
            dpg.add_table_row()
            dpg.add_table_row()
        dpg.add_text(label="Text")
    with dpg.group(horizontal=True) as g2:
        dpg.add_button(label="B1")
        dpg.add_button(label="B2")
        dpg.add_text(label="Подключено")

    dpg.set_primary_window(win, True)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()