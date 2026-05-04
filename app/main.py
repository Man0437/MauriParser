from books import Books
from dtbs import conn_dtbs, create_dtbs
from terminalparse import TerminalParser
from parser import Parser

import argparse
import sys


ENTITY = {
    "books": Books,
    "parse": Parser
}

if __name__ == "__main__":


    # Подключение к базам данных
    cor = conn_dtbs()
    create_dtbs(cor, "books")
    print("OK | connect")

    # Создание парсера
    main_parser = TerminalParser()

    print("OK | main parser")
    try:
        args = main_parser.parser.parse_args()
    except ValueError:
        print("Error")
        sys.exit(0)
    cls = ENTITY.get(args.entity)

    obj = cls()
    print(obj)
    if(type(obj) == Books):
        method = getattr(obj, args.action, None)
        print(f"action | {method}")
        try:
            method(cor, args)
            print("OK | method")
        except ValueError:
            print("Error")

    else:
        print(obj)
        obj.parse(cor)
        print("OK | parse")

    cor.close()
    sys.exit(0)
    