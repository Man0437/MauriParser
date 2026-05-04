from models.books import BookRepository
from models.dtbs import conn_dtbs, create_dtbs
from parser.terminalparse import TerminalParser
from parser.parser import Parser

import argparse
import sys
import logging
from logger import setup_logger


ENTITY = {
    "books": BookRepository,
    "parse": Parser
}

if __name__ == "__main__":

    setup_logger()
    # Подключение к базам данных
    logger = logging.getLogger(__name__)

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
        except ValueError:
            logger.error("Error | Не определен класс")

    else:
        obj.parse(cor)
        logger.info("OK | Парсинг завершен")
    cor.close()
    logger.info("ОК | Соединение закрыто")
    sys.exit(0)
    