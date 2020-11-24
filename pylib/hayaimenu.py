class Section(object):
    def __init__(self, title: str, level: int, **kwargs):
        self.title = title
        self.level = level
        self.sub_sections = []
        self.method = None
        if 'sub_sections' in kwargs:
            self.add_sub_sections(*kwargs['sub_sections'])
        if 'parent' in kwargs:
            self.parent = kwargs['parent']
        if 'method' in kwargs:
            self.method: classmethod = kwargs['method']

    def prev(self):
        return self.parent

    def next(self, index: int):
        return self.sub_sections[index]

    def set_method(self, method):
        self.method = method

    def add_sub_sections(self, *args):
        for menu_title in args:
            self.sub_sections.append(Section(menu_title, self.level+1, parent=self))

    def add_sub_section(self, menu_title, **kwargs):
        kwargs['parent'] = self
        menu = Section(menu_title, self.level + 1, **kwargs)
        self.sub_sections.append(menu)

    def print(self, **kwargs):
        for items in self.sub_sections:
            if 'format' in kwargs:
                print(kwargs['format'].format(items.title))
            else:
                print('> {}'.format(items.title))

    def run(self):
        self.method()


class HayaiMenu:
    def __init__(self, menu_title):
        self.root = Section(menu_title, 0)
        self.current = self.root

    def get_section(self, title: str, level: int):
        focus = self.root
        while focus.sub_sections:
            for section in focus.sub_sections:
                if section.title == title and section.level == level:
                    return section
                else:
                    self.get_section(title, level)

    def next(self, index: int):
        return self.root.next(index)

    def set_current(self, title: str, level: int):
        self.current = self.get_section(title, level)

    def get_current(self):
        return self.current

    def get_root(self):
        return self.root
