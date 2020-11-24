from hayaimenu import HayaiMenu


async def hi(lmao):
    print('test'+lmao)


menu = HayaiMenu('Main Menu')
menu.get_current().add_sub_section('One', sub_sections=['One.One', 'One.Two'])

menu.print()
menu.set_current_next(0)
menu.print()