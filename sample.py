from pylib.hayai_menu import HayaiMenu


def print_about():
    print('This is a simple calculator app made with the HayaiMenu library')


def add():
    x = int(input("x: "))
    y = int(input("y: "))
    print("x + y = " + str(x+y))


def subtract():
    x = int(input("x: "))
    y = int(input("y: "))
    print("x - y = " + str(x-y))


def multiply():
    x = int(input("x: "))
    y = int(input("y: "))
    print("x * y = " + str(x*y))


def divide():
    x = int(input("x: "))
    y = int(input("y: "))
    print("x / y = " + str(x/y))


menu_tree = {
    'Calculator': {
        'sub_sections': {
            'Operate': {
                'sub_sections': {
                    'Add': {
                        'method': add
                    },
                    'Subtract': {
                        'method': subtract
                    },
                    'Multiply': {
                        'method': multiply
                    },
                    'Divide': {
                        'method': divide
                    }
                }
            },
            'About': {
                'method': print_about
            },
            'Exit': {
            }
        }
    }
}

menu = HayaiMenu.make_menu_from_tree(menu_tree)

menu.select()
menu.select()
menu.select()