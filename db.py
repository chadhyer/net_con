import sqlite3
import json
from settings import DATABASE_FILE
from sys import exit, argv


def create_table_device() -> None:
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()
    cursor.execute(
        '''
        CREATE TABLE device (
            id INTEGER PRIMARY KEY,
            label TEXT,
            location TEXT,
            serial BLOB,
            ip BLOB,
            mac BLOB
        );
        ''')
    connection.close()


def insert_device(label:str, location:str, serial:str, ip:str, mac:str):
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()
    cursor.execute(
        f'''
        INSERT INTO device ( label, location, serial, ip, mac )
        VALUES ( '{label}', '{location}', '{serial}', '{ip}', '{mac}' );'''
    )
    connection.commit()
    connection.close()


def select_device(column=None, value=None) -> list:
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()
    if column != None and value != None:
        query = cursor.execute(
            f'''
            SELECT * FROM device
            WHERE {column}='{value}'
            ;'''
        ).fetchall()
    else:
        query = cursor.execute(
            '''
            SELECT * FROM device;
            '''
        ).fetchall()
    connection.close()

    return query


def main(args):

    action = 'SELECT'
    column = None
    value = None

    while args:
        current_argument = args[0]
        if current_argument in ('-C', '--create-db'):
            create_table_device()
            exit (0)
        if current_argument in ('-c', '--column'):
            column = args[1]
        if current_argument in ('-v', '--value'):
            value = args[1]
        if current_argument in ('-i', '--insert'):
            action = 'INSERT'
            try:
                label = args[1]
                location = args[2]
                serial = args[3]
                ip = args[4]
                mac = args[5]
            except IndexError as error:
                exit(f'Missing positional argument is causing: {error}')
        del args[0]

    if action == 'SELECT':
        query = select_device(column, value)
        for item in query:
            print(item)
    if action == 'INSERT':
        insert_device(label=label,
                      location=location,
                      serial=serial,
                      ip=ip,
                      mac=mac)


if __name__ == "__main__":
    query = main(argv[1:])