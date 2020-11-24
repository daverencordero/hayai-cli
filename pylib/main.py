from hayaimenu import HayaiMenu


async def hi(lmao):
    print('test'+lmao)


menu = HayaiMenu('Main Menu')
menu.get_current().add_sub_section('One', sub_sections=['One.One', 'One.Two'])

print(menu.get_current().title)
print(menu.get_current().next(0).print())