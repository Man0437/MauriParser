from books import Books
from dtbs import conn_dtbs

import argparse
import sys

ENTITY = {
    "books": Books
}
class SilentArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError("Error")

class Parsers:
    def __init__(self):
        self.parser = SilentArgumentParser()

        self.pipe = self.parser.add_subparsers(dest="entity", required=True)

        # Books
        books = self.pipe.add_parser("pins")
        books_sub = books.add_subparsers(dest="action", required=True)

        books_add = books_sub.add_parser("add")
        books_add.add_argument("n", required=False)
        books_add.add_argument("t", required=False)
        books_add.add_argument("a", required=False)
        books_add.add_argument("p", required=False)
        books_add.add_argument("m", required=False)

        books_list = books_sub.add_parser("list")

        books_delete = books_sub.add_parser("delete")

        books_check = books_sub.add_parser("check")

        books_help = books_sub.add_parser("help")



    def print_help(self):
        
        print("""Commands:
- help -
- division -
- cadet -
- officer -""")

cor = conn_dtbs()
main_parser = Parsers()
try:
    args = main_parser.parser.parse_args()
except ValueError:
    print("Error")
    sys.exit(0)
cls = ENTITY.get(args.entity)
obj = cls()
if args.action and hasattr(args, "subaction") and args.subaction == "help":
    method = getattr(obj, f"{args.action}_help", None)
    if method:
        method()
    else:
        print("No help available")
    sys.exit(0)

method = getattr(obj, args.action, None)


## проверка на обязательные аргументы
if args.action == "add" and args.entity != "books":
    required_fields = ["n", "t", "a", "p", "m"]
    missing = [field for field in required_fields if getattr(args, field) is None]
    if missing:
        print(f"Error")
        sys.exit(0)
elif args.action == "add" and args.entity == "books":
    if not args.n:
        print(f"Error")
        sys.exit(0)

if args.action == "edit" and args.entity == "books":
    if not args.i and not args.n:
        print(f"Error")
        sys.exit(0)

elif args.action == "edit" and args.entity != "books":
    if not args.i:
        print("Error")
        sys.exit(0)

if not method:
    print("Error")
    sys.exit(0)

try:
    method(cor, args)
except ValueError:
    print("Error")
    sys.exit(0)
cor.close()