from mauri.models.books import BookRepository
from mauri.models.dtbs import conn_dtbs, create_dtbs
from mauri.parser.terminalparse import TerminalParser
from mauri.parser.parser import Parser
from mauri.utils.logger import setup_logger
from mauri.ui.MainWindow import run_ui, Ui


from mauri.utils.logger_ui import logger
import sys
import logging
import os.path


ENTITY = {
    "books": BookRepository,
    "parse": Parser,
    "ui": Ui
}

if __name__ == "__main__":

    setup_logger()
    # Подключение к базам данных

    logger.info("ОК | Подключение к БД")
    cor = conn_dtbs()
    create_dtbs(cor, "books")
    logger.info("ОК| Успешное подключение")

    # Создание парсера
    main_parser = TerminalParser()

    logger.info("OK | Создался парсер")
    try:
        args = main_parser.parser.parse_args()
    except ValueError:
        logger.error("Error | Ошибка в парсинге данных консоли")
        sys.exit(0)
    cls = ENTITY.get(args.entity)
    obj = cls()
    if(type(obj) == BookRepository):
        method = getattr(obj, args.action, None)
        logger.info("ОК | Метод")
        try:
            method(cor, args)
            logger.info("OK | method")
            cor.close()
            sys.exit(0)
        except ValueError:
            logger.error("Error | Не определен класс")
            cor.close()
            sys.exit(0)

    elif(type(obj) == Parser):
        obj.parse(cor)
        logger.info("OK | Парсинг завершен")
        cor.close()
        logger.info("ОК | Соединение закрыто")
        sys.exit(0)

    elif(type(obj) == Ui):
        cor.close()
        run_ui()
    sys.exit(0)