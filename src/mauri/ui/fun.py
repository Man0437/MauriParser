from datetime import datetime

def validate_birthdate(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False
    
def pretty_print(entity_name, rows, fields):
    for row in rows:
        inner = ", ".join(
            f"{field}: {value}" for field, value in zip(fields, row)
        )
        print(f"{{{entity_name}: {{{inner}}}}}")