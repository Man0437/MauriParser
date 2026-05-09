import logging
import os.path

def setup_logger():

    if not os.path.exists("../logs"):
        os.makedirs("../logs")
        print("Создана папка logs")

    if not os.path.exists("../logs/mauri.log"):    
        with open("../logs/mauri.logs", "w") as f:
            f.write("LOGS FILE")
            print("Создан файл *.logs")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler("../logs/mauri.logs", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )