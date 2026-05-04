import dearpygui.dearpygui as dpg
import multiprocessing

MIN_SIZE = [600, 300]
MAX_SIZE = [900, 900]
EVASION_RATE = 1.0 # Коэфициент увеличения размеров главных окон
#TIME_SEC = 1

dpg.create_context()


if __name__ == "__main__":

    multiprocessing.freeze_support()

    queue = multiprocessing.Queue()
# Создание окна для приложения
    with dpg.window(label="Info", tag="main_window", min_size=[int(MIN_SIZE[0]*EVASION_RATE),int(MIN_SIZE[1]*EVASION_RATE)],
                    max_size=[int(MIN_SIZE[0]*EVASION_RATE),int(MIN_SIZE[1]*EVASION_RATE)], horizontal_scrollbar=True):
        dpg.add_text("Information of CPU", tag="info_cpu_text")

    
    
    
# Создание зоны видимости для приложения    
    dpg.create_viewport(title='Mayuri', width=MIN_SIZE[0], height=MIN_SIZE[1], max_height=int(MIN_SIZE[1]*EVASION_RATE),
                        max_width=int(MIN_SIZE[0]*EVASION_RATE))
    
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()