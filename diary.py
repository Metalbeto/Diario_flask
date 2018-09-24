import datetime
import sys
import os
from collections import OrderedDict
from peewee import *

db = SqliteDatabase('diary.db')

class Entry(Model):
    #fecha, timestamp
    #contenido
    content   = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

def add_entry():
    """Registra una entrada en nuestro diario"""
    print("Introduce tu registro. Presiona Ctrl+D cuando termines")
    data = sys.stdin.read().strip()

    if data:
        if input('Guardar entrada? [Yn]').lower() != 'n':
            Entry.create(content=data)
            print('Guardada Exitosamente')
            print('')

def view_entries(search_query=None):
    """Despliega nuestras entradas"""
    entries = Entry.select().order_by(Entry.timestamp.desc())

    if search_query:
        entries = entries.where(Entry.content.contains(search_query))

    for entry in entries:
        clear()
        timestamp = entry.timestamp.strftime( '%A %B %d, %Y %I:%M%p' )
        print(timestamp)
        print('*'*len(timestamp) )
        print(entry.content)
        print('\n\n' + '+'*len(timestamp) + '\n')
        print('n | siguiente entrada')
        print('d | borrar entrada')
        print('q | salir al menu')

        next_action = input('Accion a realizar: [Nq]').lower().strip()

        if next_action == 'q':
            break
        elif next_action == 'd':
            delete_entry(entry)

def delete_entry(entry):
    """Borra un registro"""
    response = input("Estas seguro [yN]").lower()
    if response == 'y':
        entry.delete_instance()
        print('Entrada borrada')

def search_entries():
    """Busca una entrada con cierto texto"""
    view_entries(input('Texto a buscar: '))

menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entries),
    ('s', search_entries),
])


def menu_loop():
    """muestra el menu con las opciones"""
    choice = None

    while choice != 'q':
        clear()
        print("Presiona 'q' para salir")
        for key, value in menu.items():
            print('{} | {}'.format(key, value.__doc__))
        choice = input('Eleccion: ').lower().strip()

        if choice in menu:
            clear()
            menu[choice]()

def initialize():
    db.connect()
    db.create_tables([Entry], safe=True)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == '__main__':
    initialize()
    menu_loop()
