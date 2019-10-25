from sys import argv
from mural.mod_base.migration import create_tables, create_database, insert_dummy, insert_default_user


if __name__ == '__main__':
    script, command = argv

    if command == 'create-database':
        create_database()

    if command == 'create-tables':
        create_tables()

    if command == 'insert-default-user':
        insert_default_user()

    if command == 'insert-dummy':
        insert_dummy()
