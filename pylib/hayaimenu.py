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
            self.sub_sections.append(Section(menu_title, self.level + 1, parent=self))

    def add_sub_section(self, menu_title, **kwargs):
        kwargs['parent'] = self
        menu = Section(menu_title, self.level + 1, **kwargs)
        self.sub_sections.append(menu)

    def print(self, **kwargs):
        for index, section in enumerate(self.sub_sections):
            text_format = '> {}'
            if 'start_index' in kwargs:
                index += kwargs['start_index']
            if 'format' in kwargs:
                text_format = kwargs['format']
                text_format = text_format.replace("#", str(index))
            print(text_format.format(section.title))

    def run(self):
        if self.method is not None:
            self.method()


class HayaiMenu:
    def __init__(self, menu_title, **kwargs):
        self.root = Section(menu_title, 0)
        self.current = self.root
        self.separator_char = "="
        self.separator_width = 50
        if 'separator_char' in kwargs:
            self.char = kwargs['separator_char']
        if 'separator_width' in kwargs:
            self.separator_width = kwargs['separator_width']

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

    def set_current_next(self, index: int):
        self.current = self.root.next(index)

    def set_current(self, title: str, level: int):
        self.current = self.get_section(title, level)

    def get_current(self):
        return self.current

    def get_root(self):
        return self.root

    def print(self, **kwargs):
        Bcolors.print(self.current.title.center(self.separator_width, self.separator_char), Bcolors.OKGREEN)
        self.current.print(**kwargs)

    def run(self):
        self.current.run()


class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def print(text: str, color: str):
        print(color + text + Bcolors.HEADER)
