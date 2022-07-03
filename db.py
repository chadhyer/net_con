"""
DB Supporting functions live here.

File can be executed as a script with the following parameters:

-C --create-db      | Creates a new Sqlite3 database named device.db with the device table

-c --column         | Determine what column to use in the WHERE clause of a SELECT query

-v --value          | Determine what value to use in the WHERE clause of a SELECT query

-i --insert         | Change to INSERT mode to insert a new device into the database
                      $1 = label for device
                      $2 = location device is installed
                      $3 = serial identifier for device
                      $4 = host/ip address for device
                      $5 = mac address for device
"""

import sqlite3
import json
from settings import DATABASE_FILE
from sys import exit, argv


def create_table_device() -> None:
    """Create Sqlite3 database file and device table

       Name of database determined by DATABASE_FILE variable in settings.py
    """
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()
    cursor.execute(
        '''
        CREATE TABLE device (
            id INTEGER PRIMARY KEY,
            label TEXT,
            location TEXT,
            serial BLOB,
            host BLOB,
            mac BLOB
        );
        ''')
    connection.close()


def insert_device(label:str, location:str, serial:str, host:str, mac:str) -> None:
    """Insert device into device table of the Sqlite3 file DATABASE_FILE
    
    Parameters
    ----------
    label (str): label for device
    location  (str): location device is installed
    serial  (str): serial identifier for device
    host  (str): host/ip address for device
    mac  (str): mac address for device
    """
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()
    cursor.execute(
        f'''
        INSERT INTO device ( label, location, serial, host, mac )
        VALUES ( '{label}', '{location}', '{serial}', '{host}', '{mac}' );'''
    )
    connection.commit()
    connection.close()


def select_device(column=None, value=None) -> list:
    """Returns SELECT query as a list
    
    Parameters
    ----------
    column (str): Column name for WHERE clause
                  Default = None
    value (str): Value for WHERE clause
                  Defaul = None

    Executes a SELECT query against DATABASE_FILE and returns data into a list
    """
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
    """Script mode"""
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
                host = args[4]
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
                      host=host,
                      mac=mac)


if __name__ == "__main__":
    query = main(argv[1:])