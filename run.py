from sys import argv
from mural.mod_base.migration import migrate_database, create_database


if __name__ == '__main__':
    script, command = argv

    if command == 'create-database':
        create_database()

    if command == 'migrate-database':
        migrate_database()
